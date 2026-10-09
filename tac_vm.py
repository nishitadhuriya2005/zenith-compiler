"""
Zenith Programming Language - TAC Virtual Machine & Execution Engine
Executes Three-Address Code quadruples directly, managing runtime environments,
the execution call stack, activation records, and dynamic evaluation.
"""

from typing import List, Dict, Any, Optional
from .tac import Quadruple


class RuntimeErrorZenith(Exception):
    """Exception raised during TAC execution."""
    def __init__(self, message: str, line: int = 0):
        super().__init__(f"[Runtime Error at L{line}] {message}")
        self.message = message
        self.line = line


class StackFrame:
    """Activation record for function execution."""
    def __init__(self, fn_name: str, return_ip: int, return_target: Optional[str] = None):
        self.fn_name = fn_name
        self.return_ip = return_ip
        self.return_target = return_target
        self.locals: Dict[str, Any] = {}

    def __repr__(self):
        return f"<Frame {self.fn_name} locals={self.locals}>"


class TACVirtualMachine:
    """
    Virtual Machine that interprets and executes Three-Address Code (TAC).
    """

    def __init__(self, max_steps: int = 100000):
        self.max_steps = max_steps
        self.globals: Dict[str, Any] = {}
        self.call_stack: List[StackFrame] = []
        self.param_buffer: List[Any] = []
        self.output_buffer: List[str] = []
        self.ip = 0
        self.step_count = 0

    def reset(self):
        """Resets VM state."""
        self.globals.clear()
        self.call_stack.clear()
        self.param_buffer.clear()
        self.output_buffer.clear()
        self.ip = 0
        self.step_count = 0

    def _resolve(self, arg: Any) -> Any:
        """Resolves an argument to its runtime value (constant or variable)."""
        if arg is None:
            return None
        # Literals (int, float, bool, str)
        if isinstance(arg, (int, float, bool)):
            return arg
        if isinstance(arg, str):
            # Check if it's a string literal or variable
            if (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'")):
                return arg[1:-1]
            if arg == "true":
                return True
            if arg == "false":
                return False
            # Check local scope first (if in function frame)
            if self.call_stack:
                if arg in self.call_stack[-1].locals:
                    return self.call_stack[-1].locals[arg]
            # Check globals
            if arg in self.globals:
                return self.globals[arg]
            # If not found yet and it looks like a variable/temp, return 0 or default
            return arg
        return arg

    def _store(self, target: str, value: Any):
        """Stores a value into the active environment."""
        if not target:
            return
        if self.call_stack:
            self.call_stack[-1].locals[target] = value
        else:
            self.globals[target] = value

    def execute(self, instructions: List[Quadruple], echo: bool = True) -> str:
        """
        Executes the TAC instruction sequence.
        Returns the combined program output as a string.
        """
        self.reset()
        if not instructions:
            return ""

        # Precompute label locations
        labels: Dict[str, int] = {}
        for idx, quad in enumerate(instructions):
            if quad.op == "LABEL":
                labels[str(quad.result)] = idx

        self.ip = 0
        self.step_count = 0
        num_instructions = len(instructions)

        while self.ip < num_instructions:
            self.step_count += 1
            if self.step_count > self.max_steps:
                raise RuntimeErrorZenith("Execution step limit exceeded (infinite loop protection).", instructions[self.ip].line)

            quad = instructions[self.ip]
            op = quad.op

            if op == "ASSIGN":
                val = self._resolve(quad.arg1)
                self._store(str(quad.result), val)
                self.ip += 1

            elif op in ("+", "-", "*", "/", "%"):
                v1 = self._resolve(quad.arg1)
                v2 = self._resolve(quad.arg2)
                res = None
                try:
                    if op == "+":
                        if isinstance(v1, str) or isinstance(v2, str):
                            res = str(v1) + str(v2)
                        else:
                            res = v1 + v2
                    elif op == "-":
                        res = v1 - v2
                    elif op == "*":
                        res = v1 * v2
                    elif op == "/":
                        if v2 == 0:
                            raise RuntimeErrorZenith("Division by zero", quad.line)
                        if isinstance(v1, int) and isinstance(v2, int):
                            res = v1 // v2
                        else:
                            res = v1 / v2
                    elif op == "%":
                        if v2 == 0:
                            raise RuntimeErrorZenith("Modulo by zero", quad.line)
                        res = v1 % v2
                except TypeError as ex:
                    raise RuntimeErrorZenith(f"Invalid operation '{op}' between '{v1}' and '{v2}': {ex}", quad.line)

                self._store(str(quad.result), res)
                self.ip += 1

            elif op in ("==", "!=", "<", "<=", ">", ">="):
                v1 = self._resolve(quad.arg1)
                v2 = self._resolve(quad.arg2)
                if op == "==":
                    res = (v1 == v2)
                elif op == "!=":
                    res = (v1 != v2)
                elif op == "<":
                    res = (v1 < v2)
                elif op == "<=":
                    res = (v1 <= v2)
                elif op == ">":
                    res = (v1 > v2)
                elif op == ">=":
                    res = (v1 >= v2)
                self._store(str(quad.result), res)
                self.ip += 1

            elif op in ("&&", "||"):
                v1 = bool(self._resolve(quad.arg1))
                v2 = bool(self._resolve(quad.arg2))
                res = (v1 and v2) if op == "&&" else (v1 or v2)
                self._store(str(quad.result), res)
                self.ip += 1

            elif op == "NEG":
                v = self._resolve(quad.arg1)
                self._store(str(quad.result), -v)
                self.ip += 1

            elif op == "NOT":
                v = self._resolve(quad.arg1)
                self._store(str(quad.result), not bool(v))
                self.ip += 1

            elif op == "LABEL":
                self.ip += 1

            elif op == "JUMP":
                target = str(quad.result)
                if target in labels:
                    self.ip = labels[target]
                else:
                    raise RuntimeErrorZenith(f"Jump to unknown label '{target}'", quad.line)

            elif op == "JUMP_IF_TRUE":
                cond = bool(self._resolve(quad.arg1))
                target = str(quad.result)
                if cond:
                    if target in labels:
                        self.ip = labels[target]
                    else:
                        raise RuntimeErrorZenith(f"Jump to unknown label '{target}'", quad.line)
                else:
                    self.ip += 1

            elif op == "JUMP_IF_FALSE":
                cond = bool(self._resolve(quad.arg1))
                target = str(quad.result)
                if not cond:
                    if target in labels:
                        self.ip = labels[target]
                    else:
                        raise RuntimeErrorZenith(f"Jump to unknown label '{target}'", quad.line)
                else:
                    self.ip += 1

            elif op == "PARAM":
                val = self._resolve(quad.arg1)
                self.param_buffer.append(val)
                self.ip += 1

            elif op == "PARAM_RECEIVE":
                param_name = str(quad.arg1)
                if self.param_buffer:
                    val = self.param_buffer.pop(0)
                    self._store(param_name, val)
                self.ip += 1

            elif op == "CALL":
                fn_name = str(quad.arg1)
                fn_label = f"fn_{fn_name}"
                if fn_label not in labels:
                    raise RuntimeErrorZenith(f"Undefined function label '{fn_label}'", quad.line)

                # Push stack frame
                frame = StackFrame(
                    fn_name=fn_name,
                    return_ip=self.ip + 1,
                    return_target=str(quad.result) if quad.result else None
                )
                self.call_stack.append(frame)
                self.ip = labels[fn_label]

            elif op == "RETURN":
                ret_val = self._resolve(quad.arg1)
                if self.call_stack:
                    frame = self.call_stack.pop()
                    if frame.return_target:
                        self._store(frame.return_target, ret_val)
                    self.ip = frame.return_ip
                else:
                    # Return from top-level script terminates execution
                    self.ip = num_instructions

            elif op == "PRINT":
                val = self._resolve(quad.arg1)
                out_str = str(val)
                self.output_buffer.append(out_str)
                if echo:
                    print(out_str)
                self.ip += 1

            elif op in ("FN_START", "FN_END"):
                self.ip += 1

            else:
                self.ip += 1

        return "\n".join(self.output_buffer)
