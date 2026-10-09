#!/usr/bin/env python3
"""
Zenith Compiler - Phase 2 Interactive Code Checker & Execution Engine
Allows users to type or paste arbitrary Zenith code directly in the terminal
and immediately see:
  1. Lexer Token Stream
  2. Abstract Syntax Tree (AST)
  3. Scoped Symbol Table
  4. Semantic Analysis & Type Verification
  5. Three-Address Code (TAC) Quadruples
  6. Runtime Execution Output (TAC Virtual Machine)
"""

import sys
import os

# Set up imports from src
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer
from src.tac import TACGenerator, format_tac_table, format_tac_instructions
from src.tac_vm import TACVirtualMachine, RuntimeErrorZenith
from src.printer import ASTPrinter, format_tokens, format_symbol_table


def analyze_and_run_user_input(code: str):
    print("\n" + "=" * 75)
    print("               PHASE 2 COMPILATION & EXECUTION PIPELINE                  ")
    print("=" * 75)

    # 1. Lexical Analysis
    print("\n[STEP 1: LEXICAL ANALYSIS (SCANNER)]")
    lexer = Lexer(code, filename="<interactive_input>")
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
    parser = Parser(tokens, filename="<interactive_input>")
    ast_root = parser.parse()

    if parser.errors:
        print("❌ Syntax Errors Found:")
        for err in parser.errors:
            print(f"   • {err}")
        return

    print("Abstract Syntax Tree (AST):")
    printer = ASTPrinter()
    print(printer.print_tree(ast_root))

    # 3. Scoped Symbol Table & Semantic Analysis
    print("\n[STEP 3: SCOPED SYMBOL TABLE & SEMANTIC ANALYSIS]")
    analyzer = SemanticAnalyzer()
    symtab = analyzer.analyze(ast_root)
    print(format_symbol_table(symtab))

    if analyzer.errors:
        print(f"\n❌ Semantic Errors Found ({len(analyzer.errors)}):")
        for err in analyzer.errors:
            print(f"   • {err}")
        return
    else:
        print("\n✅ Semantic Analysis Passed: Type consistency and variable scopes verified!")

    # 4. Intermediate Code Generation (TAC & Quadruples)
    print("\n[STEP 4: INTERMEDIATE CODE GENERATION (THREE-ADDRESS CODE)]")
    tac_gen = TACGenerator()
    instructions = tac_gen.generate(ast_root)
    print("Quadruples Table (Op, Arg1, Arg2, Result):")
    print(format_tac_table(instructions))
    print("\nLinear Three-Address Code:")
    print(format_tac_instructions(instructions))

    # 5. TAC Virtual Machine Execution
    print("\n[STEP 5: TAC VIRTUAL MACHINE EXECUTION]")
    print("-" * 50)
    vm = TACVirtualMachine()
    try:
        vm.execute(instructions, echo=True)
        print("-" * 50)
        print("✅ Program Executed Successfully.")
    except RuntimeErrorZenith as ex:
        print("-" * 50)
        print(f"❌ Runtime Execution Error: {ex}")


def main():
    print("=" * 75)
    print("      ZENITH COMPILER - PHASE 2 INTERACTIVE RUNNER & REPL ENGINE        ")
    print("=" * 75)
    print("Enter or paste arbitrary Zenith code to compile and execute.")
    print("To compile and run your code, type 'RUN' on a new line (or press Enter twice).")
    print("To exit, type 'exit' or press Ctrl+D.")
    print("-" * 75)

    while True:
        lines = []
        try:
            print("\nEnter Zenith code:")
            while True:
                prompt = "... " if lines else "zenith> "
                line = input(prompt)
                
                # Check for exit
                if not lines and line.strip().lower() in ("exit", "quit"):
                    print("Exiting Zenith Interactive Runner. Goodbye!")
                    return

                # Check for submission triggers
                if line.strip().upper() == "RUN":
                    break
                if not line.strip() and lines and not lines[-1].strip():
                    lines.pop()
                    break

                lines.append(line)

            source = "\n".join(lines).strip()
            if not source:
                print("No code entered. Try again.")
                continue

            analyze_and_run_user_input(source)

        except (EOFError, KeyboardInterrupt):
            print("\nExiting Zenith Interactive Runner.")
            break


if __name__ == "__main__":
    main()
