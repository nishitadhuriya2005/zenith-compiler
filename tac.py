"""
Zenith Programming Language - Intermediate Code Generator (Three-Address Code & Quadruples)
Translates the validated Abstract Syntax Tree into linear Three-Address Code (TAC)
and structured Quadruples (Op, Arg1, Arg2, Result).
"""

from dataclasses import dataclass
from typing import List, Optional, Any, Tuple
from .ast_nodes import (
    ASTNode, Program, Statement, Block, VarDecl, Assignment,
    IfStmt, WhileStmt, ForStmt, FnDecl, ReturnStmt, PrintStmt, ExprStmt,
    Expression, BinaryExpr, UnaryExpr, LiteralExpr, IdentifierExpr, CallExpr
)


@dataclass
class Quadruple:
    """
    Standard Quadruple record representing a single 3-Address Code instruction:
    (Op, Arg1, Arg2, Result)
    """
    op: str
    arg1: Optional[Any] = None
    arg2: Optional[Any] = None
    result: Optional[Any] = None
    line: int = 0

    def to_tac_string(self) -> str:
        """Converts quadruple into human-readable 3-address assembly-like instruction."""
        op = self.op
        if op == "ASSIGN":
            return f"{self.result} = {self.arg1}"
        elif op in ("+", "-", "*", "/", "%"):
            return f"{self.result} = {self.arg1} {op} {self.arg2}"
        elif op in ("==", "!=", "<", "<=", ">", ">="):
            return f"{self.result} = {self.arg1} {op} {self.arg2}"
        elif op in ("&&", "||"):
            return f"{self.result} = {self.arg1} {op} {self.arg2}"
        elif op == "NEG":
            return f"{self.result} = -{self.arg1}"
        elif op == "NOT":
            return f"{self.result} = !{self.arg1}"
        elif op == "LABEL":
            return f"{self.result}:"
        elif op == "JUMP":
            return f"goto {self.result}"
        elif op == "JUMP_IF_TRUE":
            return f"if {self.arg1} goto {self.result}"
        elif op == "JUMP_IF_FALSE":
            return f"if_false {self.arg1} goto {self.result}"
        elif op == "PARAM":
            return f"param {self.arg1}"
        elif op == "PARAM_RECEIVE":
            return f"param_recv {self.arg1}"
        elif op == "CALL":
            if self.result:
                return f"{self.result} = call {self.arg1}, {self.arg2}"
            return f"call {self.arg1}, {self.arg2}"
        elif op == "RETURN":
            if self.arg1 is not None:
                return f"return {self.arg1}"
            return "return"
        elif op == "PRINT":
            return f"print {self.arg1}"
        elif op == "FN_START":
            return f"begin_fn {self.arg1}"
        elif op == "FN_END":
            return f"end_fn {self.arg1}"
        else:
            return f"{op} {self.arg1}, {self.arg2}, {self.result}"

    def __repr__(self) -> str:
        a1 = str(self.arg1) if self.arg1 is not None else "-"
        a2 = str(self.arg2) if self.arg2 is not None else "-"
        res = str(self.result) if self.result is not None else "-"
        return f"({self.op:<12}, {a1:<12}, {a2:<12}, {res:<12})"


class TACGenerator:
    """
    AST visitor that emits a linear stream of Quadruples (Three-Address Code).
    """

    def __init__(self):
        self.instructions: List[Quadruple] = []
        self._temp_counter = 0
        self._label_counter = 0

    def new_temp(self) -> str:
        """Generates a fresh temporary variable identifier: t0, t1, t2..."""
        t = f"t{self._temp_counter}"
        self._temp_counter += 1
        return t

    def new_label(self, hint: str = "L") -> str:
        """Generates a fresh jump label: L0, L1, L2..."""
        lbl = f"{hint}{self._label_counter}"
        self._label_counter += 1
        return lbl

    def emit(self, op: str, arg1: Any = None, arg2: Any = None, result: Any = None, line: int = 0) -> Quadruple:
        """Appends a new quadruple to the instruction buffer."""
        quad = Quadruple(op=op, arg1=arg1, arg2=arg2, result=result, line=line)
        self.instructions.append(quad)
        return quad

    def generate(self, program: Program) -> List[Quadruple]:
        """Translates the AST root into Three-Address Code."""
        self.instructions.clear()
        self._temp_counter = 0
        self._label_counter = 0

        for stmt in program.statements:
            self._gen_statement(stmt)
        return self.instructions

    def _gen_statement(self, stmt: Statement):
        if isinstance(stmt, VarDecl):
            if stmt.initializer:
                val = self._gen_expression(stmt.initializer)
                self.emit("ASSIGN", arg1=val, result=stmt.name, line=stmt.line)

        elif isinstance(stmt, Assignment):
            val = self._gen_expression(stmt.value)
            self.emit("ASSIGN", arg1=val, result=stmt.target, line=stmt.line)

        elif isinstance(stmt, IfStmt):
            self._gen_if(stmt)

        elif isinstance(stmt, WhileStmt):
            self._gen_while(stmt)

        elif isinstance(stmt, ForStmt):
            self._gen_for(stmt)

        elif isinstance(stmt, FnDecl):
            self._gen_fn_decl(stmt)

        elif isinstance(stmt, ReturnStmt):
            ret_val = None
            if stmt.value:
                ret_val = self._gen_expression(stmt.value)
            self.emit("RETURN", arg1=ret_val, line=stmt.line)

        elif isinstance(stmt, PrintStmt):
            for expr in stmt.expressions:
                val = self._gen_expression(expr)
                self.emit("PRINT", arg1=val, line=stmt.line)

        elif isinstance(stmt, ExprStmt):
            self._gen_expression(stmt.expr)

        elif isinstance(stmt, Block):
            for s in stmt.statements:
                self._gen_statement(s)

    def _gen_if(self, stmt: IfStmt):
        label_end = self.new_label("L_endif_")
        
        # Condition check for main 'if'
        cond_val = self._gen_expression(stmt.condition)
        next_label = self.new_label("L_elif_") if stmt.elif_branches else (self.new_label("L_else_") if stmt.else_branch else label_end)
        self.emit("JUMP_IF_FALSE", arg1=cond_val, result=next_label, line=stmt.condition.line)

        # Then branch
        for s in stmt.then_branch.statements:
            self._gen_statement(s)
        self.emit("JUMP", result=label_end, line=stmt.line)

        # Elif branches
        curr_label = next_label
        for i, (elif_cond, elif_body) in enumerate(stmt.elif_branches):
            self.emit("LABEL", result=curr_label, line=elif_cond.line)
            is_last_elif = (i == len(stmt.elif_branches) - 1)
            next_label = self.new_label("L_else_") if (is_last_elif and stmt.else_branch) else (self.new_label("L_elif_") if not is_last_elif else label_end)
            
            elif_cond_val = self._gen_expression(elif_cond)
            self.emit("JUMP_IF_FALSE", arg1=elif_cond_val, result=next_label, line=elif_cond.line)
            for s in elif_body.statements:
                self._gen_statement(s)
            self.emit("JUMP", result=label_end, line=stmt.line)
            curr_label = next_label

        # Else branch
        if stmt.else_branch:
            self.emit("LABEL", result=curr_label, line=stmt.else_branch.line)
            for s in stmt.else_branch.statements:
                self._gen_statement(s)

        self.emit("LABEL", result=label_end, line=stmt.line)

    def _gen_while(self, stmt: WhileStmt):
        label_start = self.new_label("L_while_start_")
        label_end = self.new_label("L_while_end_")

        self.emit("LABEL", result=label_start, line=stmt.line)
        cond_val = self._gen_expression(stmt.condition)
        self.emit("JUMP_IF_FALSE", arg1=cond_val, result=label_end, line=stmt.condition.line)

        for s in stmt.body.statements:
            self._gen_statement(s)

        self.emit("JUMP", result=label_start, line=stmt.line)
        self.emit("LABEL", result=label_end, line=stmt.line)

    def _gen_for(self, stmt: ForStmt):
        label_start = self.new_label("L_for_start_")
        label_end = self.new_label("L_for_end_")

        if stmt.init:
            self._gen_statement(stmt.init)

        self.emit("LABEL", result=label_start, line=stmt.line)
        if stmt.condition:
            cond_val = self._gen_expression(stmt.condition)
            self.emit("JUMP_IF_FALSE", arg1=cond_val, result=label_end, line=stmt.condition.line)

        for s in stmt.body.statements:
            self._gen_statement(s)

        if stmt.step:
            self._gen_statement(stmt.step)

        self.emit("JUMP", result=label_start, line=stmt.line)
        self.emit("LABEL", result=label_end, line=stmt.line)

    def _gen_fn_decl(self, stmt: FnDecl):
        # Jump over function definition during linear execution
        label_skip = self.new_label(f"L_skip_fn_{stmt.name}_")
        self.emit("JUMP", result=label_skip, line=stmt.line)

        self.emit("FN_START", arg1=stmt.name, line=stmt.line)
        self.emit("LABEL", result=f"fn_{stmt.name}", line=stmt.line)

        # Receive parameters
        for p in stmt.params:
            self.emit("PARAM_RECEIVE", arg1=p.name, line=p.line)

        for s in stmt.body.statements:
            self._gen_statement(s)

        self.emit("FN_END", arg1=stmt.name, line=stmt.line)
        self.emit("LABEL", result=label_skip, line=stmt.line)

    def _gen_expression(self, expr: Expression) -> Any:
        """Generates TAC for an expression and returns its temporary name or value literal."""
        if isinstance(expr, LiteralExpr):
            return expr.value

        elif isinstance(expr, IdentifierExpr):
            return expr.name

        elif isinstance(expr, UnaryExpr):
            operand_val = self._gen_expression(expr.operand)
            temp = self.new_temp()
            op = "NEG" if expr.operator == "-" else ("NOT" if expr.operator == "!" else expr.operator)
            self.emit(op, arg1=operand_val, result=temp, line=expr.line)
            return temp

        elif isinstance(expr, BinaryExpr):
            left_val = self._gen_expression(expr.left)
            right_val = self._gen_expression(expr.right)
            temp = self.new_temp()
            self.emit(expr.operator, arg1=left_val, arg2=right_val, result=temp, line=expr.line)
            return temp

        elif isinstance(expr, CallExpr):
            # Evaluate all arguments and emit PARAM instructions
            arg_vals = [self._gen_expression(arg) for arg in expr.args]
            for val in arg_vals:
                self.emit("PARAM", arg1=val, line=expr.line)
            temp = self.new_temp()
            self.emit("CALL", arg1=expr.callee, arg2=len(arg_vals), result=temp, line=expr.line)
            return temp

        return None


def format_tac_table(instructions: List[Quadruple]) -> str:
    """Formats the list of Quadruples into an academic table representation."""
    header = f"{'Idx':<5} | {'Op':<14} | {'Arg1':<12} | {'Arg2':<12} | {'Result':<12} | {'Linear 3-Address Code':<28}"
    sep = "-" * len(header)
    rows = [header, sep]

    for idx, q in enumerate(instructions):
        a1 = str(q.arg1) if q.arg1 is not None else "-"
        a2 = str(q.arg2) if q.arg2 is not None else "-"
        res = str(q.result) if q.result is not None else "-"
        tac_code = q.to_tac_string()
        rows.append(f"{idx:<5} | {q.op:<14} | {a1:<12} | {a2:<12} | {res:<12} | {tac_code:<28}")

    return "\n".join(rows)


def format_tac_instructions(instructions: List[Quadruple]) -> str:
    """Outputs the readable assembly-like Three-Address Code listing."""
    lines = []
    indent = "    "
    for q in instructions:
        tac_str = q.to_tac_string()
        if q.op in ("LABEL", "FN_START", "FN_END"):
            lines.append(tac_str)
        else:
            lines.append(f"{indent}{tac_str}")
    return "\n".join(lines)
