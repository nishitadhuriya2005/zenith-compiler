#!/usr/bin/env python3
"""
Zenith Programming Language - Compiler Front-End CLI & Driver
Phase 1 Prototype: Lexical Analysis, Parsing, AST Construction, and Scoped Symbol Table Management.
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
from src.symbol_table import SymbolTableBuilder
from src.printer import ASTPrinter, format_tokens, format_symbol_table


def process_source(source_code: str, filename: str = "<stdin>", show_tokens: bool = False, show_ast: bool = True, show_symtab: bool = False) -> int:
    """Processes Zenith source code through Phase 1 front-end stages."""
    print("=" * 70)
    print(f" COMPILING SOURCE: {filename}")
    print("=" * 70)

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

    # 3. Symbol Table Construction & Initial Scoping Check
    builder = SymbolTableBuilder()
    symtab = builder.build(ast_root)

    if show_symtab:
        print("\n[STAGE 3] SCOPED SYMBOL TABLE:")
        print(format_symbol_table(symtab))

    if symtab.errors:
        print("\n⚠️  SEMANTIC WARNINGS / ERRORS:")
        for err in symtab.errors:
            print(f"  • {err}")

    print("\n✅ Phase 1 Front-End Pass Completed Successfully.")
    return 0


def repl_mode():
    """Interactive Read-Eval-Print Loop for testing snippets."""
    print("=" * 70)
    print(" Zenith Interactive REPL (Phase 1 Front-End Shell)")
    print(" Enter Zenith statements. Type 'exit' or Ctrl+D to quit.")
    print(" Commands: :tokens, :ast, :symtab to toggle views.")
    print("=" * 70)

    show_toks = False
    show_ast = True
    show_sym = True

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

            process_source(line, filename="<repl>", show_tokens=show_toks, show_ast=show_ast, show_symtab=show_sym)
        except (EOFError, KeyboardInterrupt):
            print("\nExiting Zenith REPL.")
            break


def main():
    parser = argparse.ArgumentParser(
        description="Zenith Compiler Front-End Driver (Phase 1 Prototype)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python3 src/main.py tests/01_basic_math.zen --all
  python3 src/main.py tests/02_control_flow.zen --ast --symtab
  python3 src/main.py --repl"""
    )
    parser.add_argument("file", nargs="?", help="Zenith source file to compile (.zen)")
    parser.add_argument("--tokens", action="store_true", help="Display token stream table")
    parser.add_argument("--ast", action="store_true", help="Display ASCII Abstract Syntax Tree")
    parser.add_argument("--symtab", action="store_true", help="Display Scoped Symbol Table")
    parser.add_argument("--all", action="store_true", help="Display all stages (Tokens, AST, Symbol Table)")
    parser.add_argument("--repl", action="store_true", help="Launch interactive REPL mode")

    args = parser.parse_args()

    if args.repl or (args.file is None and sys.stdin.isatty()):
        repl_mode()
        return 0

    if args.file is None:
        source = sys.stdin.read()
        filename = "<stdin>"
    else:
        if not os.path.isfile(args.file):
            print(f"Error: File '{args.file}' not found.", file=sys.stderr)
            return 1
        with open(args.file, "r", encoding="utf-8") as f:
            source = f.read()
        filename = args.file

    show_tokens = args.tokens or args.all
    show_ast = args.ast or args.all or (not args.tokens and not args.symtab)
    show_symtab = args.symtab or args.all

    return process_source(source, filename, show_tokens, show_ast, show_symtab)


if __name__ == "__main__":
    sys.exit(main())
