"""
Zenith Programming Language - Scoped Symbol Table Management
Implements hierarchical lexical scoping, symbol insertion, scope resolution,
duplicate declaration detection, and data type tracking.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, List, Any
from .ast_nodes import (
    Program, Statement, VarDecl, Assignment, IfStmt, WhileStmt,
    ForStmt, FnDecl, Block, ReturnStmt, PrintStmt, ExprStmt,
    Expression, BinaryExpr, UnaryExpr, LiteralExpr, IdentifierExpr, CallExpr
)


class SemanticError(Exception):
    """Exception raised when a semantic/scoping rule is violated."""
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"[Semantic Error at {line}:{column}] {message}")
        self.message = message
        self.line = line
        self.column = column


@dataclass
class Symbol:
    """Represents an identifier entry in the symbol table."""
    name: str
    type_name: str
    is_const: bool
    scope_level: int
    line: int
    column: int
    is_function: bool = False
    param_types: List[str] = field(default_factory=list)
    return_type: Optional[str] = None

    def __repr__(self) -> str:
        const_tag = "const " if self.is_const else ""
        if self.is_function:
            params = ", ".join(self.param_types)
            return f"<Symbol fn {self.name}({params}) -> {self.return_type} [L{self.line}]>"
        return f"<Symbol {const_tag}{self.name}: {self.type_name} (scope={self.scope_level}) [L{self.line}]>"


class Scope:
    """Represents an individual lexical environment with an optional parent pointer."""

    def __init__(self, name: str, level: int, parent: Optional['Scope'] = None):
        self.name = name
        self.level = level
        self.parent = parent
        self.symbols: Dict[str, Symbol] = {}

    def insert(self, symbol: Symbol) -> bool:
        """Inserts a symbol into the current scope. Returns False if already declared in this scope."""
        if symbol.name in self.symbols:
            return False
        self.symbols[symbol.name] = symbol
        return True

    def lookup_local(self, name: str) -> Optional[Symbol]:
        """Looks up a symbol in this scope only."""
        return self.symbols.get(name)

    def lookup(self, name: str) -> Optional[Symbol]:
        """Looks up a symbol hierarchically from this scope up through ancestors."""
        if name in self.symbols:
            return self.symbols[name]
        if self.parent is not None:
            return self.parent.lookup(name)
        return None


class SymbolTable:
    """
    Manages the stack of scopes and provides global/local symbol tracking.
    """

    def __init__(self):
        self.global_scope = Scope(name="global", level=0, parent=None)
        self.current_scope = self.global_scope
        self.scope_history: List[Scope] = [self.global_scope]
        self.errors: List[SemanticError] = []

    def enter_scope(self, name: str) -> Scope:
        """Pushes a new lexical scope."""
        new_scope = Scope(name=name, level=self.current_scope.level + 1, parent=self.current_scope)
        self.current_scope = new_scope
        self.scope_history.append(new_scope)
        return new_scope

    def exit_scope(self) -> Optional[Scope]:
        """Pops the current lexical scope back to the parent."""
        if self.current_scope.parent is not None:
            self.current_scope = self.current_scope.parent
        return self.current_scope

    def insert(self, symbol: Symbol) -> bool:
        """Inserts a symbol into the currently active scope."""
        success = self.current_scope.insert(symbol)
        if not success:
            prev = self.current_scope.lookup_local(symbol.name)
            prev_line = prev.line if prev else "unknown"
            err = SemanticError(
                f"Redeclaration of identifier '{symbol.name}' in the same scope. Originally declared at line {prev_line}.",
                symbol.line,
                symbol.column
            )
            self.errors.append(err)
        return success

    def lookup(self, name: str) -> Optional[Symbol]:
        """Performs hierarchical lookup from current scope outwards."""
        return self.current_scope.lookup(name)


class SymbolTableBuilder:
    """
    Traverses the Abstract Syntax Tree (AST) to populate and validate the symbol table.
    """

    def __init__(self):
        self.symtab = SymbolTable()

    def build(self, program: Program) -> SymbolTable:
        """Visits all statements in the program AST."""
        for stmt in program.statements:
            self._visit_statement(stmt)
        return self.symtab

    def _visit_statement(self, stmt: Statement):
        if isinstance(stmt, VarDecl):
            sym = Symbol(
                name=stmt.name,
                type_name=stmt.type_name,
                is_const=stmt.is_const,
                scope_level=self.symtab.current_scope.level,
                line=stmt.line,
                column=stmt.column
            )
            self.symtab.insert(sym)
            if stmt.initializer:
                self._visit_expression(stmt.initializer)

        elif isinstance(stmt, Assignment):
            sym = self.symtab.lookup(stmt.target)
            if sym is None:
                err = SemanticError(f"Use of undeclared variable '{stmt.target}'", stmt.line, stmt.column)
                self.symtab.errors.append(err)
            elif sym.is_const:
                err = SemanticError(f"Cannot reassign to constant variable '{stmt.target}'", stmt.line, stmt.column)
                self.symtab.errors.append(err)
            self._visit_expression(stmt.value)

        elif isinstance(stmt, FnDecl):
            # Insert function symbol into current enclosing scope
            param_types = [p.type_name for p in stmt.params]
            fn_sym = Symbol(
                name=stmt.name,
                type_name="function",
                is_const=True,
                scope_level=self.symtab.current_scope.level,
                line=stmt.line,
                column=stmt.column,
                is_function=True,
                param_types=param_types,
                return_type=stmt.return_type
            )
            self.symtab.insert(fn_sym)

            # Create new scope for function body
            self.symtab.enter_scope(f"fn_{stmt.name}")
            for param in stmt.params:
                p_sym = Symbol(
                    name=param.name,
                    type_name=param.type_name,
                    is_const=False,
                    scope_level=self.symtab.current_scope.level,
                    line=param.line,
                    column=param.column
                )
                self.symtab.insert(p_sym)

            for s in stmt.body.statements:
                self._visit_statement(s)
            self.symtab.exit_scope()

        elif isinstance(stmt, IfStmt):
            self._visit_expression(stmt.condition)
            self.symtab.enter_scope("if_branch")
            for s in stmt.then_branch.statements:
                self._visit_statement(s)
            self.symtab.exit_scope()

            for cond, elif_body in stmt.elif_branches:
                self._visit_expression(cond)
                self.symtab.enter_scope("elif_branch")
                for s in elif_body.statements:
                    self._visit_statement(s)
                self.symtab.exit_scope()

            if stmt.else_branch:
                self.symtab.enter_scope("else_branch")
                for s in stmt.else_branch.statements:
                    self._visit_statement(s)
                self.symtab.exit_scope()

        elif isinstance(stmt, WhileStmt):
            self._visit_expression(stmt.condition)
            self.symtab.enter_scope("while_body")
            for s in stmt.body.statements:
                self._visit_statement(s)
            self.symtab.exit_scope()

        elif isinstance(stmt, ForStmt):
            self.symtab.enter_scope("for_loop")
            if stmt.init:
                self._visit_statement(stmt.init)
            if stmt.condition:
                self._visit_expression(stmt.condition)
            if stmt.step:
                self._visit_statement(stmt.step)
            for s in stmt.body.statements:
                self._visit_statement(s)
            self.symtab.exit_scope()

        elif isinstance(stmt, Block):
            self.symtab.enter_scope("block")
            for s in stmt.statements:
                self._visit_statement(s)
            self.symtab.exit_scope()

        elif isinstance(stmt, ReturnStmt):
            if stmt.value:
                self._visit_expression(stmt.value)

        elif isinstance(stmt, PrintStmt):
            for expr in stmt.expressions:
                self._visit_expression(expr)

        elif isinstance(stmt, ExprStmt):
            self._visit_expression(stmt.expr)

    def _visit_expression(self, expr: Expression):
        if isinstance(expr, IdentifierExpr):
            sym = self.symtab.lookup(expr.name)
            if sym is None:
                err = SemanticError(f"Use of undeclared variable '{expr.name}'", expr.line, expr.column)
                self.symtab.errors.append(err)
        elif isinstance(expr, BinaryExpr):
            self._visit_expression(expr.left)
            self._visit_expression(expr.right)
        elif isinstance(expr, UnaryExpr):
            self._visit_expression(expr.operand)
        elif isinstance(expr, CallExpr):
            sym = self.symtab.lookup(expr.callee)
            if sym is None:
                err = SemanticError(f"Call to undefined function '{expr.callee}'", expr.line, expr.column)
                self.symtab.errors.append(err)
            for arg in expr.args:
                self._visit_expression(arg)
