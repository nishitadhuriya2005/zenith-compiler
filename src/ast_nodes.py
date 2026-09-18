"""
Zenith Programming Language - Abstract Syntax Tree (AST) Node Hierarchy
Defines the strongly-typed structural representation of the parsed program.
"""

from dataclasses import dataclass
from typing import List, Optional, Any, Tuple


@dataclass
class ASTNode:
    """Base class for all Abstract Syntax Tree nodes."""
    line: int
    column: int


# --- Statements ---

@dataclass
class Statement(ASTNode):
    """Base class for all statement nodes."""
    pass


@dataclass
class Program(ASTNode):
    """Root node of the Abstract Syntax Tree."""
    statements: List[Statement]


@dataclass
class Block(Statement):
    """A sequence of statements enclosed in curly braces creating a local scope."""
    statements: List[Statement]


@dataclass
class VarDecl(Statement):
    """Variable declaration: let/const x: int = 10;"""
    name: str
    type_name: str
    is_const: bool
    initializer: Optional['Expression']


@dataclass
class Assignment(Statement):
    """Variable assignment: x = 20;"""
    target: str
    value: 'Expression'


@dataclass
class IfStmt(Statement):
    """Conditional statement with optional elif and else branches."""
    condition: 'Expression'
    then_branch: Block
    elif_branches: List[Tuple['Expression', Block]]
    else_branch: Optional[Block]


@dataclass
class WhileStmt(Statement):
    """While loop statement: while (condition) { ... }"""
    condition: 'Expression'
    body: Block


@dataclass
class ForStmt(Statement):
    """For loop statement: for (let i: int = 0; i < 10; i = i + 1) { ... }"""
    init: Optional[VarDecl]
    condition: Optional['Expression']
    step: Optional[Assignment]
    body: Block


@dataclass
class Param(ASTNode):
    """Function formal parameter: name: type"""
    name: str
    type_name: str


@dataclass
class FnDecl(Statement):
    """Function declaration: fn add(a: int, b: int) -> int { return a + b; }"""
    name: str
    params: List[Param]
    return_type: str
    body: Block


@dataclass
class ReturnStmt(Statement):
    """Return statement: return expr;"""
    value: Optional['Expression']


@dataclass
class PrintStmt(Statement):
    """Built-in I/O print statement: print(a, b, c);"""
    expressions: List['Expression']


@dataclass
class ExprStmt(Statement):
    """An expression evaluated as a statement: func_call();"""
    expr: 'Expression'


# --- Expressions ---

@dataclass
class Expression(ASTNode):
    """Base class for all expression nodes that evaluate to a value."""
    pass


@dataclass
class BinaryExpr(Expression):
    """Binary operation: left op right (e.g., a + b, x > y, p && q)"""
    left: Expression
    operator: str
    right: Expression


@dataclass
class UnaryExpr(Expression):
    """Unary operation: -a, !flag"""
    operator: str
    operand: Expression


@dataclass
class LiteralExpr(Expression):
    """Constant literal: 42, 3.14, "hello", true"""
    value: Any
    type_name: str


@dataclass
class IdentifierExpr(Expression):
    """Variable or identifier reference: x, total"""
    name: str


@dataclass
class CallExpr(Expression):
    """Function invocation: calc(10, 20)"""
    callee: str
    args: List[Expression]
