"""
Zenith Programming Language - Token Definitions
Defines all token types, keywords, and the Token data structure for lexical analysis.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Optional


class TokenType(Enum):
    # End of File / Special
    EOF = auto()
    ILLEGAL = auto()

    # Literals
    INT_LIT = auto()        # e.g., 42
    FLOAT_LIT = auto()      # e.g., 3.14
    STRING_LIT = auto()     # e.g., "hello"
    BOOLEAN_LIT = auto()    # true, false

    # Identifiers & Keywords
    IDENTIFIER = auto()     # e.g., total_count, calculate_sum
    LET = auto()            # let (mutable)
    CONST = auto()          # const (immutable)
    INT = auto()            # int
    FLOAT = auto()          # float
    BOOL = auto()           # bool
    STRING = auto()         # string
    VOID = auto()           # void

    # Control Flow Keywords
    IF = auto()             # if
    ELIF = auto()           # elif
    ELSE = auto()           # else
    WHILE = auto()          # while
    FOR = auto()            # for
    FN = auto()             # fn (function declaration)
    RETURN = auto()         # return
    PRINT = auto()          # print (built-in I/O)

    # Arithmetic Operators
    PLUS = auto()           # +
    MINUS = auto()          # -
    STAR = auto()           # *
    SLASH = auto()          # /
    PERCENT = auto()        # %

    # Relational & Equality Operators
    EQ_EQ = auto()          # ==
    BANG_EQ = auto()        # !=
    LESS = auto()           # <
    LESS_EQ = auto()        # <=
    GREATER = auto()        # >
    GREATER_EQ = auto()     # >=

    # Logical Operators
    AND = auto()            # &&
    OR = auto()             # ||
    BANG = auto()           # !

    # Assignment & Punctuation
    ASSIGN = auto()         # =
    SEMICOLON = auto()      # ;
    COMMA = auto()          # ,
    COLON = auto()          # :
    ARROW = auto()          # ->
    LPAREN = auto()         # (
    RPAREN = auto()         # )
    LBRACE = auto()         # {
    RBRACE = auto()         # }
    LBRACKET = auto()       # [
    RBRACKET = auto()       # ]


# Keyword Mapping Table
KEYWORDS = {
    "let": TokenType.LET,
    "const": TokenType.CONST,
    "int": TokenType.INT,
    "float": TokenType.FLOAT,
    "bool": TokenType.BOOL,
    "string": TokenType.STRING,
    "void": TokenType.VOID,
    "if": TokenType.IF,
    "elif": TokenType.ELIF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "fn": TokenType.FN,
    "return": TokenType.RETURN,
    "print": TokenType.PRINT,
    "true": TokenType.BOOLEAN_LIT,
    "false": TokenType.BOOLEAN_LIT,
}


@dataclass(frozen=True)
class Token:
    """Represents a lexical token with source code position metadata."""
    type: TokenType
    lexeme: str
    value: Any
    line: int
    column: int

    def __repr__(self) -> str:
        val_str = f"({self.value})" if self.value is not None else ""
        return f"Token({self.type.name}, '{self.lexeme}'{val_str}, L{self.line}:C{self.column})"
