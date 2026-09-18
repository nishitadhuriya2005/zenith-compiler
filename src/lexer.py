"""
Zenith Programming Language - Lexical Analyzer (Lexer)
Performs lexical analysis, token classification, position tracking, and lexical error reporting.
"""

from typing import List, Optional
from .tokens import Token, TokenType, KEYWORDS


class LexerError(Exception):
    """Exception raised when an invalid character or unterminated token is encountered."""
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"[Lexer Error at {line}:{column}] {message}")
        self.message = message
        self.line = line
        self.column = column


class Lexer:
    """
    Lexical analyzer for the Zenith programming language.
    Transforms raw source code string into a sequence of classified Tokens.
    """

    def __init__(self, source: str, filename: str = "<stdin>"):
        self.source = source
        self.filename = filename
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        self.errors: List[LexerError] = []

    def _peek(self, offset: int = 0) -> Optional[str]:
        target = self.pos + offset
        if target < len(self.source):
            return self.source[target]
        return None

    def _advance(self) -> Optional[str]:
        if self.pos >= len(self.source):
            return None
        ch = self.source[self.pos]
        self.pos += 1
        if ch == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def _match(self, expected: str) -> bool:
        if self._peek() == expected:
            self._advance()
            return True
        return False

    def tokenize(self) -> List[Token]:
        """Scans the entire source code and returns the list of recognized tokens."""
        while self.pos < len(self.source):
            ch = self._peek()

            # Skip whitespace
            if ch in (' ', '\t', '\r'):
                self._advance()
                continue
            if ch == '\n':
                self._advance()
                continue

            # Comments
            if ch == '/':
                if self._peek(1) == '/':
                    # Single-line comment
                    while self._peek() is not None and self._peek() != '\n':
                        self._advance()
                    continue
                elif self._peek(1) == '*':
                    # Multi-line comment
                    start_line, start_col = self.line, self.column
                    self._advance()  # /
                    self._advance()  # *
                    closed = False
                    while self._peek() is not None:
                        if self._peek() == '*' and self._peek(1) == '/':
                            self._advance()
                            self._advance()
                            closed = True
                            break
                        self._advance()
                    if not closed:
                        err = LexerError("Unterminated multi-line comment", start_line, start_col)
                        self.errors.append(err)
                    continue

            # Start of a new token
            tok_line = self.line
            tok_col = self.column

            # Numbers (Integer or Float)
            if ch.isdigit():
                self.tokens.append(self._number(tok_line, tok_col))
                continue

            # Identifiers and Keywords
            if ch.isalpha() or ch == '_':
                self.tokens.append(self._identifier(tok_line, tok_col))
                continue

            # String Literals
            if ch == '"':
                self.tokens.append(self._string(tok_line, tok_col))
                continue

            # Operators and Delimiters
            self._advance()  # consume character

            if ch == '+':
                self.tokens.append(Token(TokenType.PLUS, "+", None, tok_line, tok_col))
            elif ch == '-':
                if self._match('>'):
                    self.tokens.append(Token(TokenType.ARROW, "->", None, tok_line, tok_col))
                else:
                    self.tokens.append(Token(TokenType.MINUS, "-", None, tok_line, tok_col))
            elif ch == '*':
                self.tokens.append(Token(TokenType.STAR, "*", None, tok_line, tok_col))
            elif ch == '/':
                self.tokens.append(Token(TokenType.SLASH, "/", None, tok_line, tok_col))
            elif ch == '%':
                self.tokens.append(Token(TokenType.PERCENT, "%", None, tok_line, tok_col))
            elif ch == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, ";", None, tok_line, tok_col))
            elif ch == ',':
                self.tokens.append(Token(TokenType.COMMA, ",", None, tok_line, tok_col))
            elif ch == ':':
                self.tokens.append(Token(TokenType.COLON, ":", None, tok_line, tok_col))
            elif ch == '(':
                self.tokens.append(Token(TokenType.LPAREN, "(", None, tok_line, tok_col))
            elif ch == ')':
                self.tokens.append(Token(TokenType.RPAREN, ")", None, tok_line, tok_col))
            elif ch == '{':
                self.tokens.append(Token(TokenType.LBRACE, "{", None, tok_line, tok_col))
            elif ch == '}':
                self.tokens.append(Token(TokenType.RBRACE, "}", None, tok_line, tok_col))
            elif ch == '[':
                self.tokens.append(Token(TokenType.LBRACKET, "[", None, tok_line, tok_col))
            elif ch == ']':
                self.tokens.append(Token(TokenType.RBRACKET, "]", None, tok_line, tok_col))
            elif ch == '=':
                if self._match('='):
                    self.tokens.append(Token(TokenType.EQ_EQ, "==", None, tok_line, tok_col))
                else:
                    self.tokens.append(Token(TokenType.ASSIGN, "=", None, tok_line, tok_col))
            elif ch == '!':
                if self._match('='):
                    self.tokens.append(Token(TokenType.BANG_EQ, "!=", None, tok_line, tok_col))
                else:
                    self.tokens.append(Token(TokenType.BANG, "!", None, tok_line, tok_col))
            elif ch == '<':
                if self._match('='):
                    self.tokens.append(Token(TokenType.LESS_EQ, "<=", None, tok_line, tok_col))
                else:
                    self.tokens.append(Token(TokenType.LESS, "<", None, tok_line, tok_col))
            elif ch == '>':
                if self._match('='):
                    self.tokens.append(Token(TokenType.GREATER_EQ, ">=", None, tok_line, tok_col))
                else:
                    self.tokens.append(Token(TokenType.GREATER, ">", None, tok_line, tok_col))
            elif ch == '&':
                if self._match('&'):
                    self.tokens.append(Token(TokenType.AND, "&&", None, tok_line, tok_col))
                else:
                    err = LexerError(f"Unexpected character '&', did you mean '&&'?", tok_line, tok_col)
                    self.errors.append(err)
                    self.tokens.append(Token(TokenType.ILLEGAL, "&", None, tok_line, tok_col))
            elif ch == '|':
                if self._match('|'):
                    self.tokens.append(Token(TokenType.OR, "||", None, tok_line, tok_col))
                else:
                    err = LexerError(f"Unexpected character '|', did you mean '||'?", tok_line, tok_col)
                    self.errors.append(err)
                    self.tokens.append(Token(TokenType.ILLEGAL, "|", None, tok_line, tok_col))
            else:
                err = LexerError(f"Unrecognized character: '{ch}'", tok_line, tok_col)
                self.errors.append(err)
                self.tokens.append(Token(TokenType.ILLEGAL, ch, None, tok_line, tok_col))

        self.tokens.append(Token(TokenType.EOF, "", None, self.line, self.column))
        return self.tokens

    def _number(self, line: int, col: int) -> Token:
        start_pos = self.pos
        is_float = False

        while self._peek() is not None and self._peek().isdigit():
            self._advance()

        # Check for decimal point followed by digits
        if self._peek() == '.' and self._peek(1) is not None and self._peek(1).isdigit():
            is_float = True
            self._advance()  # consume '.'
            while self._peek() is not None and self._peek().isdigit():
                self._advance()

        lexeme = self.source[start_pos:self.pos]
        if is_float:
            return Token(TokenType.FLOAT_LIT, lexeme, float(lexeme), line, col)
        else:
            return Token(TokenType.INT_LIT, lexeme, int(lexeme), line, col)

    def _identifier(self, line: int, col: int) -> Token:
        start_pos = self.pos
        while self._peek() is not None and (self._peek().isalnum() or self._peek() == '_'):
            self._advance()

        lexeme = self.source[start_pos:self.pos]
        token_type = KEYWORDS.get(lexeme, TokenType.IDENTIFIER)

        val = None
        if token_type == TokenType.BOOLEAN_LIT:
            val = (lexeme == "true")

        return Token(token_type, lexeme, val, line, col)

    def _string(self, line: int, col: int) -> Token:
        self._advance()  # consume opening quote "
        chars = []
        closed = False

        while self._peek() is not None:
            ch = self._peek()
            if ch == '"':
                self._advance()
                closed = True
                break
            elif ch == '\\':
                self._advance()
                escaped = self._advance()
                if escaped == 'n':
                    chars.append('\n')
                elif escaped == 't':
                    chars.append('\t')
                elif escaped == '"':
                    chars.append('"')
                elif escaped == '\\':
                    chars.append('\\')
                else:
                    chars.append(escaped or '')
            elif ch == '\n':
                err = LexerError("Multi-line strings without escape are not permitted", line, col)
                self.errors.append(err)
                break
            else:
                chars.append(self._advance())

        if not closed:
            err = LexerError("Unterminated string literal", line, col)
            self.errors.append(err)

        lexeme = "".join(chars)
        return Token(TokenType.STRING_LIT, f'"{lexeme}"', lexeme, line, col)
