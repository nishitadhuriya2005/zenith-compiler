"""
Zenith Programming Language - Semantic Analyzer & Type Checker
Performs comprehensive static semantic analysis, type inference,
type compatibility verification, immutability enforcement, and scope validation.
"""

from typing import List, Optional, Dict, Any, Set
from .ast_nodes import (
    ASTNode, Program, Statement, Block, VarDecl, Assignment,
    IfStmt, WhileStmt, ForStmt, FnDecl, ReturnStmt, PrintStmt, ExprStmt,
    Expression, BinaryExpr, UnaryExpr, LiteralExpr, IdentifierExpr, CallExpr
)
from .symbol_table import SymbolTable, Symbol, Scope, SemanticError


class SemanticAnalyzer:
    """
    Two-pass / deep AST visitor for semantic validation:
    1. Scoping and declaration checking
    2. Static type checking and type inference
    3. Immutability validation (const safety)
    4. Function signature and return type verification
    """

    PRIMITIVE_TYPES = {"int", "float", "bool", "string", "void"}

    def __init__(self):
        self.symtab = SymbolTable()
        self.errors: List[SemanticError] = []
        self.current_function: Optional[Symbol] = None
        # Track annotated expression types: id(expr) -> type_name
        self.expr_types: Dict[int, str] = {}

    def analyze(self, program: Program) -> SymbolTable:
        """Runs full semantic analysis pass on the AST."""
        for stmt in program.statements:
            self._analyze_statement(stmt)
        return self.symtab

    def _error(self, message: str, line: int, column: int):
        err = SemanticError(message, line, column)
        self.errors.append(err)
        self.symtab.errors.append(err)

    def _analyze_statement(self, stmt: Statement):
        if isinstance(stmt, VarDecl):
            self._analyze_var_decl(stmt)
        elif isinstance(stmt, Assignment):
            self._analyze_assignment(stmt)
        elif isinstance(stmt, IfStmt):
            self._analyze_if_stmt(stmt)
        elif isinstance(stmt, WhileStmt):
            self._analyze_while_stmt(stmt)
        elif isinstance(stmt, ForStmt):
            self._analyze_for_stmt(stmt)
        elif isinstance(stmt, FnDecl):
            self._analyze_fn_decl(stmt)
        elif isinstance(stmt, ReturnStmt):
            self._analyze_return_stmt(stmt)
        elif isinstance(stmt, PrintStmt):
            self._analyze_print_stmt(stmt)
        elif isinstance(stmt, ExprStmt):
            self._analyze_expression(stmt.expr)
        elif isinstance(stmt, Block):
            self.symtab.enter_scope("block")
            for s in stmt.statements:
                self._analyze_statement(s)
            self.symtab.exit_scope()

    def _analyze_var_decl(self, decl: VarDecl):
        # Validate type name
        if decl.type_name not in self.PRIMITIVE_TYPES:
            self._error(f"Unknown type '{decl.type_name}' in declaration of '{decl.name}'", decl.line, decl.column)
        elif decl.type_name == "void":
            self._error(f"Variable '{decl.name}' cannot be declared with type 'void'", decl.line, decl.column)

        # Check for duplicate in current scope
        if self.symtab.current_scope.lookup_local(decl.name) is not None:
            prev = self.symtab.current_scope.lookup_local(decl.name)
            prev_line = prev.line if prev else "unknown"
            self._error(
                f"Redeclaration of identifier '{decl.name}' in the same scope. Originally declared at line {prev_line}.",
                decl.line, decl.column
            )
            return

        # Check initializer if present
        if decl.initializer:
            init_type = self._analyze_expression(decl.initializer)
            if init_type and not self._types_compatible(decl.type_name, init_type):
                self._error(
                    f"Type mismatch in declaration of '{decl.name}': cannot assign '{init_type}' to variable of type '{decl.type_name}'",
                    decl.line, decl.column
                )
        elif decl.is_const:
            self._error(f"Constant '{decl.name}' must be initialized upon declaration", decl.line, decl.column)

        # Insert symbol into symbol table
        sym = Symbol(
            name=decl.name,
            type_name=decl.type_name,
            is_const=decl.is_const,
            scope_level=self.symtab.current_scope.level,
            line=decl.line,
            column=decl.column
        )
        self.symtab.insert(sym)

    def _analyze_assignment(self, assign: Assignment):
        sym = self.symtab.lookup(assign.target)
        val_type = self._analyze_expression(assign.value)

        if sym is None:
            self._error(f"Use of undeclared variable '{assign.target}'", assign.line, assign.column)
            return

        if sym.is_const:
            self._error(f"Cannot reassign to constant variable '{assign.target}'", assign.line, assign.column)
            return

        if sym.is_function:
            self._error(f"Cannot assign to function identifier '{assign.target}'", assign.line, assign.column)
            return

        if val_type and not self._types_compatible(sym.type_name, val_type):
            self._error(
                f"Type mismatch in assignment to '{assign.target}': cannot assign value of type '{val_type}' to '{sym.type_name}'",
                assign.line, assign.column
            )

    def _analyze_if_stmt(self, if_stmt: IfStmt):
        cond_type = self._analyze_expression(if_stmt.condition)
        if cond_type and cond_type != "bool":
            self._error(f"Condition in 'if' statement must evaluate to 'bool', got '{cond_type}'", if_stmt.condition.line, if_stmt.condition.column)

        self.symtab.enter_scope("if_then")
        for s in if_stmt.then_branch.statements:
            self._analyze_statement(s)
        self.symtab.exit_scope()

        for cond, elif_block in if_stmt.elif_branches:
            elif_cond_type = self._analyze_expression(cond)
            if elif_cond_type and elif_cond_type != "bool":
                self._error(f"Condition in 'elif' statement must evaluate to 'bool', got '{elif_cond_type}'", cond.line, cond.column)
            self.symtab.enter_scope("elif_body")
            for s in elif_block.statements:
                self._analyze_statement(s)
            self.symtab.exit_scope()

        if if_stmt.else_branch:
            self.symtab.enter_scope("else_body")
            for s in if_stmt.else_branch.statements:
                self._analyze_statement(s)
            self.symtab.exit_scope()

    def _analyze_while_stmt(self, while_stmt: WhileStmt):
        cond_type = self._analyze_expression(while_stmt.condition)
        if cond_type and cond_type != "bool":
            self._error(f"Condition in 'while' loop must evaluate to 'bool', got '{cond_type}'", while_stmt.condition.line, while_stmt.condition.column)

        self.symtab.enter_scope("while_body")
        for s in while_stmt.body.statements:
            self._analyze_statement(s)
        self.symtab.exit_scope()

    def _analyze_for_stmt(self, for_stmt: ForStmt):
        self.symtab.enter_scope("for_loop")
        if for_stmt.init:
            self._analyze_statement(for_stmt.init)
        if for_stmt.condition:
            cond_type = self._analyze_expression(for_stmt.condition)
            if cond_type and cond_type != "bool":
                self._error(f"Condition in 'for' loop must evaluate to 'bool', got '{cond_type}'", for_stmt.condition.line, for_stmt.condition.column)
        if for_stmt.step:
            self._analyze_statement(for_stmt.step)
        for s in for_stmt.body.statements:
            self._analyze_statement(s)
        self.symtab.exit_scope()

    def _analyze_fn_decl(self, fn: FnDecl):
        # Validate return type
        if fn.return_type not in self.PRIMITIVE_TYPES:
            self._error(f"Unknown return type '{fn.return_type}' for function '{fn.name}'", fn.line, fn.column)

        # Check if function name already exists in current scope
        if self.symtab.current_scope.lookup_local(fn.name) is not None:
            self._error(f"Redeclaration of function '{fn.name}' in the same scope", fn.line, fn.column)
            return

        param_names: Set[str] = set()
        param_types: List[str] = []
        for p in fn.params:
            if p.name in param_names:
                self._error(f"Duplicate parameter name '{p.name}' in function '{fn.name}'", p.line, p.column)
            param_names.add(p.name)
            if p.type_name not in self.PRIMITIVE_TYPES or p.type_name == "void":
                self._error(f"Invalid parameter type '{p.type_name}' for parameter '{p.name}'", p.line, p.column)
            param_types.append(p.type_name)

        fn_sym = Symbol(
            name=fn.name,
            type_name="function",
            is_const=True,
            scope_level=self.symtab.current_scope.level,
            line=fn.line,
            column=fn.column,
            is_function=True,
            param_types=param_types,
            return_type=fn.return_type
        )
        self.symtab.insert(fn_sym)

        # Enter function body scope
        prev_fn = self.current_function
        self.current_function = fn_sym
        self.symtab.enter_scope(f"fn_{fn.name}")

        for p in fn.params:
            p_sym = Symbol(
                name=p.name,
                type_name=p.type_name,
                is_const=False,
                scope_level=self.symtab.current_scope.level,
                line=p.line,
                column=p.column
            )
            self.symtab.insert(p_sym)

        for s in fn.body.statements:
            self._analyze_statement(s)

        self.symtab.exit_scope()
        self.current_function = prev_fn

        # Check if non-void function guarantees a return
        if fn.return_type != "void":
            guaranteed = any(self._statement_guarantees_return(s) for s in fn.body.statements)
            if not guaranteed:
                self._error(f"Function '{fn.name}' with return type '{fn.return_type}' may be missing a return statement", fn.line, fn.column)

    def _statement_guarantees_return(self, stmt: Statement) -> bool:
        if isinstance(stmt, ReturnStmt):
            return True
        if isinstance(stmt, Block):
            return any(self._statement_guarantees_return(s) for s in stmt.statements)
        if isinstance(stmt, IfStmt):
            if stmt.else_branch is None:
                return False
            then_ret = self._statement_guarantees_return(stmt.then_branch)
            else_ret = self._statement_guarantees_return(stmt.else_branch)
            elifs_ret = all(self._statement_guarantees_return(b) for _, b in stmt.elif_branches)
            return then_ret and else_ret and elifs_ret
        return False

    def _analyze_return_stmt(self, ret: ReturnStmt):
        if self.current_function is None:
            self._error("'return' statement outside function body", ret.line, ret.column)
            return

        expected_type = self.current_function.return_type
        if ret.value is not None:
            actual_type = self._analyze_expression(ret.value)
            if expected_type == "void":
                self._error(f"Function '{self.current_function.name}' is declared 'void' and cannot return a value", ret.line, ret.column)
            elif actual_type and not self._types_compatible(expected_type, actual_type):
                self._error(
                    f"Return type mismatch in function '{self.current_function.name}': expected '{expected_type}', got '{actual_type}'",
                    ret.line, ret.column
                )
        else:
            if expected_type != "void":
                self._error(f"Function '{self.current_function.name}' must return a value of type '{expected_type}'", ret.line, ret.column)

    def _analyze_print_stmt(self, print_stmt: PrintStmt):
        for expr in print_stmt.expressions:
            self._analyze_expression(expr)

    # --- Expression Analysis & Type Inference ---

    def _analyze_expression(self, expr: Expression) -> Optional[str]:
        """Infers and validates the static type of an expression."""
        t: Optional[str] = None

        if isinstance(expr, LiteralExpr):
            t = expr.type_name

        elif isinstance(expr, IdentifierExpr):
            sym = self.symtab.lookup(expr.name)
            if sym is None:
                self._error(f"Use of undeclared variable '{expr.name}'", expr.line, expr.column)
                t = None
            elif sym.is_function:
                self._error(f"Identifier '{expr.name}' refers to a function, not a variable", expr.line, expr.column)
                t = "function"
            else:
                t = sym.type_name

        elif isinstance(expr, UnaryExpr):
            operand_type = self._analyze_expression(expr.operand)
            if operand_type is None:
                t = None
            elif expr.operator == "-":
                if operand_type in ("int", "float"):
                    t = operand_type
                else:
                    self._error(f"Unary operator '-' requires numeric operand, got '{operand_type}'", expr.line, expr.column)
                    t = None
            elif expr.operator == "!":
                if operand_type == "bool":
                    t = "bool"
                else:
                    self._error(f"Unary operator '!' requires boolean operand, got '{operand_type}'", expr.line, expr.column)
                    t = "bool"
            else:
                self._error(f"Unknown unary operator '{expr.operator}'", expr.line, expr.column)

        elif isinstance(expr, BinaryExpr):
            left_type = self._analyze_expression(expr.left)
            right_type = self._analyze_expression(expr.right)
            t = self._check_binary_operation(expr.operator, left_type, right_type, expr.line, expr.column)

        elif isinstance(expr, CallExpr):
            t = self._analyze_call_expr(expr)

        if t is not None:
            self.expr_types[id(expr)] = t
        return t

    def _check_binary_operation(self, op: str, left: Optional[str], right: Optional[str], line: int, col: int) -> Optional[str]:
        if left is None or right is None:
            return None

        # Arithmetic operators
        if op in ("+", "-", "*", "/", "%"):
            if op == "+" and left == "string" and right == "string":
                return "string"
            if left == "int" and right == "int":
                if op == "/":
                    return "int"  # integer division in Zenith
                return "int"
            if (left in ("int", "float")) and (right in ("int", "float")):
                return "float"
            self._error(f"Operator '{op}' cannot be applied to operands of type '{left}' and '{right}'", line, col)
            return None

        # Relational operators
        if op in ("<", "<=", ">", ">="):
            if (left in ("int", "float")) and (right in ("int", "float")):
                return "bool"
            self._error(f"Relational operator '{op}' requires numeric operands, got '{left}' and '{right}'", line, col)
            return "bool"

        # Equality operators
        if op in ("==", "!="):
            if left == right:
                return "bool"
            if (left in ("int", "float")) and (right in ("int", "float")):
                return "bool"
            self._error(f"Comparison '{op}' between incompatible types '{left}' and '{right}'", line, col)
            return "bool"

        # Logical operators
        if op in ("&&", "||"):
            if left == "bool" and right == "bool":
                return "bool"
            self._error(f"Logical operator '{op}' requires boolean operands, got '{left}' and '{right}'", line, col)
            return "bool"

        self._error(f"Unknown binary operator '{op}'", line, col)
        return None

    def _analyze_call_expr(self, call: CallExpr) -> Optional[str]:
        sym = self.symtab.lookup(call.callee)
        if sym is None:
            self._error(f"Call to undefined function '{call.callee}'", call.line, call.column)
            return None

        if not sym.is_function:
            self._error(f"Identifier '{call.callee}' is not a callable function", call.line, call.column)
            return None

        if len(call.args) != len(sym.param_types):
            self._error(
                f"Function '{call.callee}' expects {len(sym.param_types)} arguments, got {len(call.args)}",
                call.line, call.column
            )
            return sym.return_type

        for i, (arg, expected_t) in enumerate(zip(call.args, sym.param_types)):
            actual_t = self._analyze_expression(arg)
            if actual_t and not self._types_compatible(expected_t, actual_t):
                self._error(
                    f"Argument {i+1} to function '{call.callee}' expects '{expected_t}', got '{actual_t}'",
                    arg.line, arg.column
                )

        return sym.return_type

    def _types_compatible(self, expected: str, actual: str) -> bool:
        if expected == actual:
            return True
        # Implicit promotion: int -> float
        if expected == "float" and actual == "int":
            return True
        return False
