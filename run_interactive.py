#!/usr/bin/env python3
"""
Zenith Compiler - User Interactive Input Checker
Allows users to type or paste custom Zenith code directly in the terminal
and immediately see the Lexer tokens, AST syntax tree, and Scoped Symbol Table.
"""

import sys
import os

# Set up imports from src
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from src.lexer import Lexer
from src.parser import Parser
from src.symbol_table import SymbolTableBuilder
from src.printer import ASTPrinter, format_tokens, format_symbol_table


def analyze_user_input(code: str):
    print("\n" + "=" * 75)
    print("                      COMPILATION ANALYSIS RESULT                        ")
    print("=" * 75)

    # 1. Lexical Analysis
    print("\n[STEP 1: LEXICAL ANALYSIS (SCANNER)]")
    lexer = Lexer(code, filename="<user_input>")
    tokens = lexer.tokenize()

    if lexer.errors:
        print("❌ Lexical Errors Found:")
        for err in lexer.errors:
            print(f"   • {err}")
        return

    print("Tokens Table:")
    print(format_tokens(tokens))

    # 2. Syntax Analysis (Parsing & AST)
    print("\n[STEP 2: SYNTAX ANALYSIS & ABSTRACT SYNTAX TREE]")
    parser = Parser(tokens, filename="<user_input>")
    ast_root = parser.parse()

    if parser.errors:
        print("❌ Syntax Errors Found:")
        for err in parser.errors:
            print(f"   • {err}")
        return

    print("Abstract Syntax Tree (AST):")
    printer = ASTPrinter()
    print(printer.print_tree(ast_root))

    # 3. Scoped Symbol Table
    print("\n[STEP 3: SCOPED SYMBOL TABLE]")
    builder = SymbolTableBuilder()
    symtab = builder.build(ast_root)
    print(format_symbol_table(symtab))

    if symtab.errors:
        print("\n⚠️ Scope / Semantic Warnings:")
        for err in symtab.errors:
            print(f"   • {err}")
    else:
        print("\n✅ Verification Successful: All tokens valid, grammar matched, and symbols scoped!")


def main():
    print("=" * 75)
    print("            ZENITH COMPILER - INTERACTIVE CODE CHECKER                  ")
    print("=" * 75)
    print("Enter or paste your Zenith code.")
    print("To finish your input and analyze, type 'RUN' on a new line (or press Enter twice).")
    print("To exit, type 'exit'.")
    print("-" * 75)

    while True:
        lines = []
        try:
            print("\nType Zenith code below:")
            while True:
                prompt = "... " if lines else "zenith> "
                line = input(prompt)
                
                # Check for exit
                if not lines and line.strip().lower() in ("exit", "quit"):
                    print("Exiting Zenith Interactive Checker. Goodbye!")
                    return

                # Check for submission triggers
                if line.strip().upper() == "RUN":
                    break
                if not line.strip() and lines and not lines[-1].strip():
                    # Two consecutive empty lines
                    lines.pop() # remove extra empty line
                    break

                lines.append(line)

            source = "\n".join(lines).strip()
            if not source:
                print("No code entered. Try again.")
                continue

            analyze_user_input(source)

        except (EOFError, KeyboardInterrupt):
            print("\nExiting Zenith Interactive Checker.")
            break


if __name__ == "__main__":
    main()
