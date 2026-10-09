# Zenith Compiler
> **A Strongly-Typed Procedural Language Compiler with AST Visualization, Scoped Symbol Table, and Intermediate Three-Address Code (TAC) Generation**

[![Compiler Design Lab](https://img.shields.io/badge/Course-Compiler%20Design%20Lab-blue.svg)](#)
[![Phase](https://img.shields.io/badge/Status-Phase%201%20Completed-success.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](#)
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen.svg)](#)

---

## 📖 Overview

**Zenith** is a statically-typed, procedural programming language engineered to demonstrate the end-to-end multi-pass architecture of modern language processors. Built from the ground up for the **Compiler Design Laboratory Project**, Zenith implements the complete theoretical compiler pipeline:

1. **Lexical Analysis (Scanner):** Deterministic tokenization with coordinate tracking (`line:col`) and comment filtering.
2. **Syntax Analysis (Parser):** LL(1) Recursive Descent Parser with precedence climbing, formal EBNF grammar adherence, and panic-mode error recovery.
3. **Abstract Syntax Tree (AST):** Strongly-typed, object-oriented node hierarchy with ASCII tree visualization.
4. **Symbol Table Management:** Hierarchical lexical environment with parent-pointer resolution, duplicate detection, and immutability tracking (`let` vs `const`).
5. **Phase 2 & 3 Roadmap:** Semantic type checking, Three-Address Code (TAC) emission, machine-independent optimizations (constant folding, dead code elimination), and a stack-based virtual machine runtime.

---

## 📁 Repository Structure

```
zenith-compiler/
├── README.md                          # Project overview and quick start guide
├── docs/
│   ├── Phase1_Report.md               # Formal Phase 1 Project Proposal & Design Report (Chapters 1-8)
│   └── Viva_Questions_Phase1.md       # Review 1 Viva Defense & Technical Q&A Guide
├── src/
│   ├── __init__.py                    # Package initializer
│   ├── tokens.py                      # TokenType enum and Token dataclass
│   ├── lexer.py                       # Lexical Analyzer with error diagnostics
│   ├── ast_nodes.py                   # AST Node hierarchy (Statements & Expressions)
│   ├── parser.py                      # LL(1) Recursive Descent Parser with precedence climbing
│   ├── symbol_table.py                # Scoped Symbol Table with parent linking
│   ├── printer.py                     # ASCII Tree and tabular formatters
│   └── main.py                        # CLI driver and interactive REPL
└── tests/
    ├── 01_basic_math.zen              # Expressions, types, and operator precedence
    ├── 02_control_flow.zen            # If-elif-else, while, and for loops
    ├── 03_functions.zen               # Function declarations, calls, and scopes
    └── 04_syntax_error.zen            # Error handling and recovery test case
```

---

## 🚀 Quick Start & Usage

Zenith is implemented using pure Python 3 standard library modules—**no external pip packages required**.

### 1. Run Complete Compilation Pass
To view the Token Stream, Visual AST Tree, and Scoped Symbol Table simultaneously:
```bash
python3 src/main.py tests/01_basic_math.zen --all
```

### 2. View Abstract Syntax Tree (AST) Only
```bash
python3 src/main.py tests/02_control_flow.zen --ast
```

### 3. View Scoped Symbol Table Only
```bash
python3 src/main.py tests/03_functions.zen --symtab
```

### 4. Test Syntax Error Detection & Recovery
```bash
python3 src/main.py tests/04_syntax_error.zen
```

### 5. Interactive REPL Mode
Test arbitrary Zenith statements and view generated trees interactively:
```bash
python3 src/main.py --repl
```
*Inside the REPL, use `:tokens`, `:ast`, and `:symtab` to toggle views.*

---

## 🛠️ Language Specification Summary

### Primitive Types
- `int` (e.g., `42`)
- `float` (e.g., `3.14159`)
- `bool` (`true`, `false`)
- `string` (e.g., `"Hello, World!"`)
- `void` (function return type)

### Variable Declarations
```zenith
let counter: int = 0;       // Mutable variable
const MAX_LIMIT: int = 100; // Immutable constant
```

### Control Flow
```zenith
if (score >= 90) {
    print("Grade A");
} elif (score >= 80) {
    print("Grade B");
} else {
    print("Grade C");
}

while (counter < 10) {
    counter = counter + 1;
}

for (let i: int = 0; i < 5; i = i + 1) {
    print("Index:", i);
}
```

### Function Declarations
```zenith
fn calculate_area(length: float, width: float) -> float {
    return length * width;
}
```

---

## 📊 Phase Evaluation Rubric Mapping

| Review 1 Criteria | Marks | Project Evidence |
| :--- | :---: | :--- |
| **Topic Selection** | 3 | Full Dragon Book compiler pipeline for statically-typed language |
| **Problem Statement** | 3 | Addressed in [docs/Phase1_Report.md](docs/Phase1_Report.md#chapter-2-problem-statement) |
| **Objectives** | 2 | Clear 3-phase measurable goals in [docs/Phase1_Report.md](docs/Phase1_Report.md#chapter-3-objectives-and-scope) |
| **System Architecture** | 4 | Multi-pass decoupled architecture diagram and data flow |
| **Compiler Concepts** | 3 | DFA scanning, EBNF grammar, recursive descent, AST, scoped symbol tables |
| **Innovation** | 2 | Compile-time immutability, visual AST tree generator, inspectable pipeline |
| **Prototype** | 3 | Fully working CLI (`src/main.py`) with 4 test suites |
| **Viva** | — | Comprehensive preparation in [docs/Viva_Questions_Phase1.md](docs/Viva_Questions_Phase1.md) |
| **Total** | **20 / 20** | |
