"""
Zenith Programming Language - Recursive Descent Parser
Implements syntax analysis, grammar enforcement, operator precedence parsing,
and AST construction with panic-mode error recovery.
"""

from typing import List, Optional, Tuple
from .tokens import Token, TokenType
from .ast_nodes import (
    Program, Statement, Block, VarDecl, Assignment, IfStmt, WhileStmt,
    ForStmt, FnDecl, ReturnStmt, PrintStmt, ExprStmt,
    Expression, BinaryExpr, UnaryExpr, LiteralExpr, IdentifierExpr, CallExpr, Param
)


class ParserError(Exception):
    """Exception raised for syntax errors during parsing."""
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"[Syntax Error at {line}:{column}] {message}")
        self.message = message
        self.line = line
        self.column = column


class Parser:
    """
    LL(1) Recursive Descent Parser with operator precedence climbing.
    Transforms a stream of Tokens into an Abstract Syntax Tree (AST).
    """

    def __init__(self, tokens: List[Token], filename: str = "<stdin>"):
        self.tokens = tokens
        self.filename = filename
        self.current = 0
        self.errors: List[ParserError] = []

    # --- Helper methods ---

    def _peek(self, offset: int = 0) -> Token:
        pos = self.current + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]  # Return EOF

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._peek().type == token_type

    def _match(self, *types: TokenType) -> bool:
        for t in types:
            if self._check(t):
                self._advance()
                return True
        return False

    def _consume(self, token_type: TokenType, error_message: str) -> Token:
        if self._check(token_type):
            return self._advance()
        tok = self._peek()
        err = ParserError(f"{error_message}. Got '{tok.lexeme}' ({tok.type.name})", tok.line, tok.column)
        self.errors.append(err)
        raise err

    def _synchronize(self):
        """Panic-mode recovery to resynchronize parser at the next statement boundary."""
        self._advance()
        while not self._is_at_end():
            if self._previous().type == TokenType.SEMICOLON:
                return
            if self._peek().type in (
                TokenType.LET, TokenType.CONST, TokenType.IF,
                TokenType.WHILE, TokenType.FOR, TokenType.FN,
                TokenType.RETURN, TokenType.PRINT, TokenType.RBRACE
            ):
                return
            self._advance()

    # --- Entry point ---

    def parse(self) -> Program:
        """Parses the entire token stream into a Program AST node."""
        statements: List[Statement] = []
        start_line = self._peek().line
        start_col = self._peek().column

        while not self._is_at_end():
            try:
                stmt = self._statement()
                if stmt:
                    statements.append(stmt)
            except ParserError:
                self._synchronize()

        return Program(line=start_line, column=start_col, statements=statements)

    # --- Statement Parsers ---

    def _statement(self) -> Optional[Statement]:
        if self._match(TokenType.LET, TokenType.CONST):
            return self._var_decl()
        if self._match(TokenType.IF):
            return self._if_stmt()
        if self._match(TokenType.WHILE):
            return self._while_stmt()
        if self._match(TokenType.FOR):
            return self._for_stmt()
        if self._match(TokenType.FN):
            return self._fn_decl()
        if self._match(TokenType.RETURN):
            return self._return_stmt()
        if self._match(TokenType.PRINT):
            return self._print_stmt()
        if self._match(TokenType.LBRACE):
            return self._block()

        # Check for assignment: identifier '='
        if self._check(TokenType.IDENTIFIER) and self._peek(1).type == TokenType.ASSIGN:
            return self._assignment()

        return self._expr_stmt()

    def _var_decl(self) -> VarDecl:
        kw_token = self._previous()
        is_const = (kw_token.type == TokenType.CONST)

        name_tok = self._consume(TokenType.IDENTIFIER, "Expected variable name after declaration keyword")
        self._consume(TokenType.COLON, "Expected ':' after variable name to specify type")
        
        type_tok = self._advance()
        if type_tok.type not in (TokenType.INT, TokenType.FLOAT, TokenType.BOOL, TokenType.STRING, TokenType.VOID):
            err = ParserError(f"Expected valid type name (int, float, bool, string), got '{type_tok.lexeme}'", type_tok.line, type_tok.column)
            self.errors.append(err)
            raise err

        initializer = None
        if self._match(TokenType.ASSIGN):
            initializer = self._expression()

        self._consume(TokenType.SEMICOLON, "Expected ';' after variable declaration")
        return VarDecl(
            line=kw_token.line,
            column=kw_token.column,
            name=name_tok.lexeme,
            type_name=type_tok.lexeme,
            is_const=is_const,
            initializer=initializer
        )

    def _assignment(self) -> Assignment:
        name_tok = self._advance()  # IDENTIFIER
        self._consume(TokenType.ASSIGN, "Expected '=' in assignment")
        val = self._expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after assignment expression")
        return Assignment(line=name_tok.line, column=name_tok.column, target=name_tok.lexeme, value=val)

    def _block(self) -> Block:
        brace_tok = self._previous()
        statements: List[Statement] = []
        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            stmt = self._statement()
            if stmt:
                statements.append(stmt)
        self._consume(TokenType.RBRACE, "Expected '}' to close block")
        return Block(line=brace_tok.line, column=brace_tok.column, statements=statements)

    def _if_stmt(self) -> IfStmt:
        if_tok = self._previous()
        self._consume(TokenType.LPAREN, "Expected '(' after 'if'")
        condition = self._expression()
        self._consume(TokenType.RPAREN, "Expected ')' after if condition")

        self._consume(TokenType.LBRACE, "Expected '{' to start if branch body")
        then_branch = self._block()

        elif_branches: List[Tuple[Expression, Block]] = []
        while self._match(TokenType.ELIF):
            self._consume(TokenType.LPAREN, "Expected '(' after 'elif'")
            elif_cond = self._expression()
            self._consume(TokenType.RPAREN, "Expected ')' after elif condition")
            self._consume(TokenType.LBRACE, "Expected '{' to start elif branch body")
            elif_body = self._block()
            elif_branches.append((elif_cond, elif_body))

        else_branch = None
        if self._match(TokenType.ELSE):
            self._consume(TokenType.LBRACE, "Expected '{' to start else branch body")
            else_branch = self._block()

        return IfStmt(
            line=if_tok.line,
            column=if_tok.column,
            condition=condition,
            then_branch=then_branch,
            elif_branches=elif_branches,
            else_branch=else_branch
        )

    def _while_stmt(self) -> WhileStmt:
        while_tok = self._previous()
        self._consume(TokenType.LPAREN, "Expected '(' after 'while'")
        condition = self._expression()
        self._consume(TokenType.RPAREN, "Expected ')' after while condition")
        self._consume(TokenType.LBRACE, "Expected '{' to start while body")
        body = self._block()
        return WhileStmt(line=while_tok.line, column=while_tok.column, condition=condition, body=body)

    def _for_stmt(self) -> ForStmt:
        for_tok = self._previous()
        self._consume(TokenType.LPAREN, "Expected '(' after 'for'")

        # Init
        init = None
        if self._match(TokenType.LET, TokenType.CONST):
            init = self._var_decl()
        elif not self._match(TokenType.SEMICOLON):
            # Assignment or expression in init
            pass

        # Condition
        condition = None
        if not self._check(TokenType.SEMICOLON):
            condition = self._expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after for loop condition")

        # Step
        step = None
        if not self._check(TokenType.RPAREN):
            if self._check(TokenType.IDENTIFIER) and self._peek(1).type == TokenType.ASSIGN:
                id_tok = self._advance()
                self._consume(TokenType.ASSIGN, "Expected '=' in for loop step")
                step_val = self._expression()
                step = Assignment(line=id_tok.line, column=id_tok.column, target=id_tok.lexeme, value=step_val)
            else:
                self._expression()

        self._consume(TokenType.RPAREN, "Expected ')' after for loop clauses")
        self._consume(TokenType.LBRACE, "Expected '{' to start for loop body")
        body = self._block()
        return ForStmt(line=for_tok.line, column=for_tok.column, init=init, condition=condition, step=step, body=body)

    def _fn_decl(self) -> FnDecl:
        fn_tok = self._previous()
        name_tok = self._consume(TokenType.IDENTIFIER, "Expected function name after 'fn'")
        self._consume(TokenType.LPAREN, "Expected '(' after function name")

        params: List[Param] = []
        if not self._check(TokenType.RPAREN):
            while True:
                p_name = self._consume(TokenType.IDENTIFIER, "Expected parameter name")
                self._consume(TokenType.COLON, "Expected ':' after parameter name")
                p_type = self._advance()
                params.append(Param(line=p_name.line, column=p_name.column, name=p_name.lexeme, type_name=p_type.lexeme))
                if not self._match(TokenType.COMMA):
                    break

        self._consume(TokenType.RPAREN, "Expected ')' after parameters")

        return_type = "void"
        if self._match(TokenType.ARROW):
            ret_tok = self._advance()
            return_type = ret_tok.lexeme

        self._consume(TokenType.LBRACE, "Expected '{' to start function body")
        body = self._block()
        return FnDecl(
            line=fn_tok.line,
            column=fn_tok.column,
            name=name_tok.lexeme,
            params=params,
            return_type=return_type,
            body=body
        )

    def _return_stmt(self) -> ReturnStmt:
        ret_tok = self._previous()
        value = None
        if not self._check(TokenType.SEMICOLON):
            value = self._expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after return statement")
        return ReturnStmt(line=ret_tok.line, column=ret_tok.column, value=value)

    def _print_stmt(self) -> PrintStmt:
        print_tok = self._previous()
        self._consume(TokenType.LPAREN, "Expected '(' after 'print'")
        exprs: List[Expression] = []
        if not self._check(TokenType.RPAREN):
            while True:
                exprs.append(self._expression())
                if not self._match(TokenType.COMMA):
                    break
        self._consume(TokenType.RPAREN, "Expected ')' after print arguments")
        self._consume(TokenType.SEMICOLON, "Expected ';' after print statement")
        return PrintStmt(line=print_tok.line, column=print_tok.column, expressions=exprs)

    def _expr_stmt(self) -> ExprStmt:
        expr = self._expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after expression")
        return ExprStmt(line=expr.line, column=expr.column, expr=expr)

    # --- Expression Parsers (Precedence Hierarchy) ---

    def _expression(self) -> Expression:
        return self._logical_or()

    def _logical_or(self) -> Expression:
        expr = self._logical_and()
        while self._match(TokenType.OR):
            op_tok = self._previous()
            right = self._logical_and()
            expr = BinaryExpr(line=op_tok.line, column=op_tok.column, left=expr, operator=op_tok.lexeme, right=right)
        return expr

    def _logical_and(self) -> Expression:
        expr = self._equality()
        while self._match(TokenType.AND):
            op_tok = self._previous()
            right = self._equality()
            expr = BinaryExpr(line=op_tok.line, column=op_tok.column, left=expr, operator=op_tok.lexeme, right=right)
        return expr

    def _equality(self) -> Expression:
        expr = self._relational()
        while self._match(TokenType.EQ_EQ, TokenType.BANG_EQ):
            op_tok = self._previous()
            right = self._relational()
            expr = BinaryExpr(line=op_tok.line, column=op_tok.column, left=expr, operator=op_tok.lexeme, right=right)
        return expr

    def _relational(self) -> Expression:
        expr = self._additive()
        while self._match(TokenType.LESS, TokenType.LESS_EQ, TokenType.GREATER, TokenType.GREATER_EQ):
            op_tok = self._previous()
            right = self._additive()
            expr = BinaryExpr(line=op_tok.line, column=op_tok.column, left=expr, operator=op_tok.lexeme, right=right)
        return expr

    def _additive(self) -> Expression:
        expr = self._multiplicative()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            op_tok = self._previous()
            right = self._multiplicative()
            expr = BinaryExpr(line=op_tok.line, column=op_tok.column, left=expr, operator=op_tok.lexeme, right=right)
        return expr

    def _multiplicative(self) -> Expression:
        expr = self._unary()
        while self._match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op_tok = self._previous()
            right = self._unary()
            expr = BinaryExpr(line=op_tok.line, column=op_tok.column, left=expr, operator=op_tok.lexeme, right=right)
        return expr

    def _unary(self) -> Expression:
        if self._match(TokenType.MINUS, TokenType.BANG):
            op_tok = self._previous()
            operand = self._unary()
            return UnaryExpr(line=op_tok.line, column=op_tok.column, operator=op_tok.lexeme, operand=operand)
        return self._primary()

    def _primary(self) -> Expression:
        tok = self._peek()

        if self._match(TokenType.INT_LIT):
            return LiteralExpr(line=tok.line, column=tok.column, value=tok.value, type_name="int")

        if self._match(TokenType.FLOAT_LIT):
            return LiteralExpr(line=tok.line, column=tok.column, value=tok.value, type_name="float")

        if self._match(TokenType.STRING_LIT):
            return LiteralExpr(line=tok.line, column=tok.column, value=tok.value, type_name="string")

        if self._match(TokenType.BOOLEAN_LIT):
            return LiteralExpr(line=tok.line, column=tok.column, value=tok.value, type_name="bool")

        if self._match(TokenType.IDENTIFIER):
            name = tok.lexeme
            # Function Call: identifier '('
            if self._match(TokenType.LPAREN):
                args: List[Expression] = []
                if not self._check(TokenType.RPAREN):
                    while True:
                        args.append(self._expression())
                        if not self._match(TokenType.COMMA):
                            break
                self._consume(TokenType.RPAREN, "Expected ')' after function arguments")
                return CallExpr(line=tok.line, column=tok.column, callee=name, args=args)
            return IdentifierExpr(line=tok.line, column=tok.column, name=name)

        if self._match(TokenType.LPAREN):
            expr = self._expression()
            self._consume(TokenType.RPAREN, "Expected ')' after grouping expression")
            return expr

        err = ParserError(f"Unexpected token in expression: '{tok.lexeme}' ({tok.type.name})", tok.line, tok.column)
        self.errors.append(err)
        raise err
