#!/usr/bin/env python3
"""
Zenith Programming Language - Compiler Front-End & Execution CLI Driver
Phase 2: Lexical Analysis, Parsing, AST Construction, Scoped Symbol Table,
Semantic Analysis & Type Checking, Three-Address Code (TAC), and TAC VM Execution.
"""

import sys
import os
import argparse

# Ensure src directory is importable
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer
from src.tac import TACGenerator, format_tac_table, format_tac_instructions
from src.tac_vm import TACVirtualMachine, RuntimeErrorZenith
from src.printer import ASTPrinter, format_tokens, format_symbol_table


def process_source(
    source_code: str,
    filename: str = "<stdin>",
    show_tokens: bool = False,
    show_ast: bool = False,
    show_symtab: bool = False,
    show_semantic: bool = False,
    show_tac: bool = False,
    run_vm: bool = True
) -> int:
    """Processes Zenith source code through Phase 2 compiler & execution pipeline."""
    print("=" * 75)
    print(f" COMPILING SOURCE: {filename}")
    print("=" * 75)

    # 1. Lexical Analysis
    lexer = Lexer(source_code, filename=filename)
    tokens = lexer.tokenize()

    if lexer.errors:
        print("\n❌ LEXICAL ERRORS DETECTED:")
        for err in lexer.errors:
            print(f"  • {err}")
        return 1

    if show_tokens:
        print("\n[STAGE 1] TOKEN STREAM:")
        print(format_tokens(tokens))

    # 2. Syntax Analysis (Recursive Descent Parsing)
    parser = Parser(tokens, filename=filename)
    ast_root = parser.parse()

    if parser.errors:
        print("\n❌ SYNTAX ERRORS DETECTED:")
        for err in parser.errors:
            print(f"  • {err}")
        return 1

    if show_ast:
        print("\n[STAGE 2] ABSTRACT SYNTAX TREE (AST):")
        printer = ASTPrinter()
        print(printer.print_tree(ast_root))

    # 3. Semantic Analysis & Type Checking
    analyzer = SemanticAnalyzer()
    symtab = analyzer.analyze(ast_root)

    if show_symtab:
        print("\n[STAGE 3] SCOPED SYMBOL TABLE:")
        print(format_symbol_table(symtab))

    if analyzer.errors:
        print(f"\n❌ SEMANTIC ERRORS DETECTED ({len(analyzer.errors)} error(s)):")
        for err in analyzer.errors:
            print(f"  • {err}")
        return 1
    elif show_semantic:
        print("\n[STAGE 4] SEMANTIC VALIDATION:")
        print("  ✓ All variable declarations valid")
        print("  ✓ Strict type compatibility verified")
        print("  ✓ Immutability (const safety) enforced")
        print("  ✓ Function signatures and return types validated")
        print("  ✓ Scopes resolved successfully with 0 errors")

    # 4. Intermediate Code Generation (Three-Address Code & Quadruples)
    tac_gen = TACGenerator()
    instructions = tac_gen.generate(ast_root)

    if show_tac:
        print("\n[STAGE 5] THREE-ADDRESS CODE (TAC) QUADRUPLES:")
        print(format_tac_table(instructions))
        print("\n[STAGE 5.1] READABLE THREE-ADDRESS CODE:")
        print(format_tac_instructions(instructions))

    # 5. Execution Engine (TAC Virtual Machine)
    if run_vm:
        print("\n[STAGE 6] PROGRAM EXECUTION OUTPUT (TAC VM):")
        print("-" * 45)
        vm = TACVirtualMachine()
        try:
            vm.execute(instructions, echo=True)
            print("-" * 45)
            print(" Execution completed successfully.")
        except RuntimeErrorZenith as ex:
            print("-" * 45)
            print(f"\n❌ RUNTIME ERROR: {ex}")
            return 1

    print("\n✅ Phase 2 Compilation & Execution Pipeline Completed Successfully.")
    return 0


def repl_mode():
    """Interactive Read-Eval-Print Loop for testing arbitrary Zenith snippets."""
    print("=" * 75)
    print(" Zenith Interactive REPL (Phase 2 Core Implementation Shell)")
    print(" Supports arbitrary user input with full Lexing, Parsing, TAC & Execution.")
    print(" Commands:")
    print("   :tokens   - Toggle token stream display")
    print("   :ast      - Toggle AST tree display")
    print("   :symtab   - Toggle symbol table display")
    print("   :tac      - Toggle Three-Address Code display")
    print("   exit/quit - Exit shell")
    print("=" * 75)

    show_toks = False
    show_ast = False
    show_sym = False
    show_tac = True

    while True:
        try:
            line = input("zenith> ").strip()
            if not line:
                continue
            if line in ("exit", "quit"):
                break
            if line == ":tokens":
                show_toks = not show_toks
                print(f"Tokens display: {show_toks}")
                continue
            if line == ":ast":
                show_ast = not show_ast
                print(f"AST display: {show_ast}")
                continue
            if line == ":symtab":
                show_sym = not show_sym
                print(f"Symbol table display: {show_sym}")
                continue
            if line == ":tac":
                show_tac = not show_tac
                print(f"TAC display: {show_tac}")
                continue

            process_source(
                line,
                filename="<repl>",
                show_tokens=show_toks,
                show_ast=show_ast,
                show_symtab=show_sym,
                show_semantic=True,
                show_tac=show_tac,
                run_vm=True
            )
        except (EOFError, KeyboardInterrupt):
            print("\nExiting Zenith REPL.")
            break


def main():
    parser = argparse.ArgumentParser(
        description="Zenith Compiler & Execution Engine Driver (Phase 2 Deliverable)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python3 src/main.py tests/01_basic_math.zen --all
  python3 src/main.py tests/02_control_flow.zen --tac --exec
  python3 src/main.py -c "let x: int = 10; print(x * 5);"
  python3 src/main.py --repl"""
    )
    parser.add_argument("file", nargs="?", help="Zenith source file to compile (.zen)")
    parser.add_argument("-c", "--code", type=str, help="Execute inline Zenith code string directly")
    parser.add_argument("--tokens", action="store_true", help="Display token stream table")
    parser.add_argument("--ast", action="store_true", help="Display ASCII Abstract Syntax Tree")
    parser.add_argument("--symtab", action="store_true", help="Display Scoped Symbol Table")
    parser.add_argument("--semantic", action="store_true", help="Display Semantic Analysis report")
    parser.add_argument("--tac", action="store_true", help="Display Three-Address Code Quadruples")
    parser.add_argument("--exec", action="store_true", help="Execute generated TAC on VM (default on)")
    parser.add_argument("--no-exec", action="store_true", help="Disable TAC execution")
    parser.add_argument("--all", action="store_true", help="Display all stages from Lexing to Execution")
    parser.add_argument("--repl", action="store_true", help="Launch interactive REPL shell")

    args = parser.parse_args()

    if args.repl or (args.file is None and args.code is None and sys.stdin.isatty()):
        repl_mode()
        return 0

    if args.code is not None:
        source = args.code
        filename = "<inline>"
    elif args.file is not None:
        if not os.path.isfile(args.file):
            print(f"Error: File '{args.file}' not found.", file=sys.stderr)
            return 1
        with open(args.file, "r", encoding="utf-8") as f:
            source = f.read()
        filename = args.file
    else:
        source = sys.stdin.read()
        filename = "<stdin>"

    show_tokens = args.tokens or args.all
    show_ast = args.ast or args.all
    show_symtab = args.symtab or args.all
    show_semantic = args.semantic or args.all
    show_tac = args.tac or args.all
    run_vm = not args.no_exec or args.exec or args.all

    # If user ran without specific flags, show TAC and VM execution by default
    if not (args.tokens or args.ast or args.symtab or args.semantic or args.tac or args.all):
        show_tac = True
        run_vm = True

    return process_source(
        source_code=source,
        filename=filename,
        show_tokens=show_tokens,
        show_ast=show_ast,
        show_symtab=show_symtab,
        show_semantic=show_semantic,
        show_tac=show_tac,
        run_vm=run_vm
    )


if __name__ == "__main__":
    sys.exit(main())
