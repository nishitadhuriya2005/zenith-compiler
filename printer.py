"""
Zenith Programming Language - AST & Symbol Table Visualizer
Renders hierarchical ASCII tree representations of the AST and formatted tables for tokens and symbols.
"""

from typing import List
from .ast_nodes import (
    ASTNode, Program, Block, VarDecl, Assignment, IfStmt, WhileStmt,
    ForStmt, FnDecl, ReturnStmt, PrintStmt, ExprStmt,
    BinaryExpr, UnaryExpr, LiteralExpr, IdentifierExpr, CallExpr
)
from .tokens import Token
from .symbol_table import SymbolTable, Scope


class ASTPrinter:
    """Visualizes the AST using ASCII tree branches."""

    def print_tree(self, node: ASTNode, prefix: str = "", is_last: bool = True) -> str:
        lines: List[str] = []
        connector = "└── " if is_last else "├── "
        child_prefix = prefix + ("    " if is_last else "│   ")

        node_repr = self._node_label(node)
        lines.append(f"{prefix}{connector}{node_repr}")

        children = self._get_children(node)
        for i, child in enumerate(children):
            last = (i == len(children) - 1)
            lines.append(self.print_tree(child, child_prefix, last))

        return "\n".join(lines)

    def _node_label(self, node: ASTNode) -> str:
        loc = f"[L{node.line}:C{node.column}]"
        if isinstance(node, Program):
            return f"Program {loc}"
        elif isinstance(node, VarDecl):
            const_tag = "const" if node.is_const else "let"
            return f"VarDecl: {const_tag} {node.name}: {node.type_name} {loc}"
        elif isinstance(node, Assignment):
            return f"Assignment: {node.target} = {loc}"
        elif isinstance(node, Block):
            return f"Block ({len(node.statements)} stmts) {loc}"
        elif isinstance(node, IfStmt):
            return f"IfStmt {loc}"
        elif isinstance(node, WhileStmt):
            return f"WhileStmt {loc}"
        elif isinstance(node, ForStmt):
            return f"ForStmt {loc}"
        elif isinstance(node, FnDecl):
            params_str = ", ".join(f"{p.name}: {p.type_name}" for p in node.params)
            return f"FnDecl: {node.name}({params_str}) -> {node.return_type} {loc}"
        elif isinstance(node, ReturnStmt):
            return f"ReturnStmt {loc}"
        elif isinstance(node, PrintStmt):
            return f"PrintStmt {loc}"
        elif isinstance(node, ExprStmt):
            return f"ExprStmt {loc}"
        elif isinstance(node, BinaryExpr):
            return f"BinaryExpr: ({node.operator}) {loc}"
        elif isinstance(node, UnaryExpr):
            return f"UnaryExpr: ({node.operator}) {loc}"
        elif isinstance(node, LiteralExpr):
            return f"Literal: {repr(node.value)} ({node.type_name}) {loc}"
        elif isinstance(node, IdentifierExpr):
            return f"Identifier: {node.name} {loc}"
        elif isinstance(node, CallExpr):
            return f"CallExpr: {node.callee}() {loc}"
        return f"{type(node).__name__} {loc}"

    def _get_children(self, node: ASTNode) -> List[ASTNode]:
        if isinstance(node, Program):
            return list(node.statements)
        elif isinstance(node, Block):
            return list(node.statements)
        elif isinstance(node, VarDecl):
            return [node.initializer] if node.initializer else []
        elif isinstance(node, Assignment):
            return [node.value]
        elif isinstance(node, IfStmt):
            res = [node.condition, node.then_branch]
            for cond, body in node.elif_branches:
                res.extend([cond, body])
            if node.else_branch:
                res.append(node.else_branch)
            return res
        elif isinstance(node, WhileStmt):
            return [node.condition, node.body]
        elif isinstance(node, ForStmt):
            res = []
            if node.init:
                res.append(node.init)
            if node.condition:
                res.append(node.condition)
            if node.step:
                res.append(node.step)
            res.append(node.body)
            return res
        elif isinstance(node, FnDecl):
            return list(node.params) + [node.body]
        elif isinstance(node, ReturnStmt):
            return [node.value] if node.value else []
        elif isinstance(node, PrintStmt):
            return list(node.expressions)
        elif isinstance(node, ExprStmt):
            return [node.expr]
        elif isinstance(node, BinaryExpr):
            return [node.left, node.right]
        elif isinstance(node, UnaryExpr):
            return [node.operand]
        elif isinstance(node, CallExpr):
            return list(node.args)
        return []


def format_tokens(tokens: List[Token]) -> str:
    """Formats a list of tokens into an aligned tabular view."""
    lines = [
        "┌──────┬──────┬─────────────────┬────────────────────────────┬──────────────────┐",
        "│ Line │ Col  │ Token Type      │ Lexeme                     │ Value            │",
        "├──────┼──────┼─────────────────┼────────────────────────────┼──────────────────┤",
    ]
    for tok in tokens:
        val_str = str(tok.value) if tok.value is not None else "-"
        lexeme_disp = tok.lexeme.replace("\n", "\\n").replace("\t", "\\t")
        if len(lexeme_disp) > 24:
            lexeme_disp = lexeme_disp[:21] + "..."
        lines.append(
            f"│ {tok.line:<4} │ {tok.column:<4} │ {tok.type.name:<15} │ {lexeme_disp:<26} │ {val_str:<16} │"
        )
    lines.append("└──────┴──────┴─────────────────┴────────────────────────────┴──────────────────┘")
    return "\n".join(lines)


def format_symbol_table(symtab: SymbolTable) -> str:
    """Formats the symbol table scopes and symbols into an aligned tabular view."""
    lines = []
    lines.append("=" * 80)
    lines.append("                         ZENITH SCOPED SYMBOL TABLE                             ")
    lines.append("=" * 80)

    for scope in symtab.scope_history:
        parent_name = scope.parent.name if scope.parent else "None"
        lines.append(f"\n[Scope: '{scope.name}'] (Level: {scope.level}, Parent: '{parent_name}')")
        if not scope.symbols:
            lines.append("  (No local symbols declared)")
            continue

        lines.append("  ┌──────────────────────┬─────────────┬───────────┬──────────────┬───────────────┐")
        lines.append("  │ Name                 │ Type        │ Category  │ Defined At   │ Details       │")
        lines.append("  ├──────────────────────┼─────────────┼───────────┼──────────────┼───────────────┤")
        for sym in scope.symbols.values():
            category = "function" if sym.is_function else ("const" if sym.is_const else "let (var)")
            defined_at = f"L{sym.line}:C{sym.column}"
            details = f"args=({', '.join(sym.param_types)})" if sym.is_function else f"scope_lvl={sym.scope_level}"
            lines.append(
                f"  │ {sym.name:<20} │ {sym.type_name:<11} │ {category:<9} │ {defined_at:<12} │ {details:<13} │"
            )
        lines.append("  └──────────────────────┴─────────────┴───────────┴──────────────┴───────────────┘")

    if symtab.errors:
        lines.append("\n" + "!" * 40 + " SCOPE / SEMANTIC ERRORS " + "!" * 40)
        for err in symtab.errors:
            lines.append(f"  * {err.message}")

    return "\n".join(lines)
