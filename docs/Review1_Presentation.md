# Zenith Compiler - Review 1 Presentation Slides Outline

Use this slide structure when presenting **Review 1 (Phase 1)** to faculty evaluators. It directly maps to the 20-mark evaluation rubric.

---

## Slide 1: Title Slide
- **Project Title:** Zenith: A Strongly-Typed Procedural Language Compiler with AST Visualization, Scoped Symbol Table, and Intermediate Three-Address Code (TAC) Generation
- **Course:** Compiler Design Laboratory
- **Candidate:** Individual Project Submission
- **Review:** Review 1 – Project Proposal and System Design (20 Marks)

---

## Slide 2: Problem Statement & Motivation (3 Marks)
- **Problem Statement:**
  - Modern dynamically-typed scripting languages defer type and scoping bugs to runtime.
  - Production industrial compilers (GCC, LLVM) are monolithic black boxes, obscuring AST construction and intermediate representations.
- **Project Motivation:**
  - Build a transparent, multi-pass compiler for a safe procedural language that explicitly models every classical compiler phase.
  - Provide visual AST diagnostics, hierarchical symbol tables, and clear Three-Address Code (TAC) emission.

---

## Slide 3: Project Objectives & Scope (2 Marks)
- **Primary Objectives:**
  1. Define an unambiguous EBNF Context-Free Grammar.
  2. Implement an LL(1) Recursive Descent Parser with precedence climbing.
  3. Construct a strongly-typed Abstract Syntax Tree (AST).
  4. Build a Scoped Symbol Table supporting nested lexical blocks and immutability (`let` vs `const`).
  5. Prepare a clear roadmap for Phase 2 (Type Checking & TAC) and Phase 3 (Optimization & VM Execution).
- **Scope:** Primitive types (`int`, `float`, `bool`, `string`), control flow (`if-elif-else`, `while`, `for`), and functions (`fn`).

---

## Slide 4: Compiler Design Concepts Applied (3 Marks)
- **Lexical Analysis:** Deterministic Finite Automata (DFA) pattern recognition, lookahead, coordinate tracking (`line:col`).
- **Syntax Analysis:** Context-Free Grammar (CFG), LL(1) recursive descent parser, panic-mode error recovery.
- **Operator Precedence:** Operator precedence climbing handling 7 priority levels (Logical $\to$ Equality $\to$ Relational $\to$ Additive $\to$ Multiplicative $\to$ Unary).
- **Abstract Syntax Tree (AST):** Object-oriented hierarchical representation eliminating syntactic noise.
- **Symbol Table:** Lexical scoping with parent pointer chaining and duplicate declaration detection.

---

## Slide 5: System Architecture & Data Flow (4 Marks)
- **Multi-Pass Pipeline:**
  ```
  Source Code (.zen)
          │
          ▼
  [Lexical Analyzer] ──► Token Stream
          │
          ▼
  [Recursive Descent Parser] ──► Abstract Syntax Tree (AST)
          │
          ▼
  [Scoped Symbol Table Manager] ──► Scoped Environments
          │
          ▼
  [Visualizer & CLI Driver] ──► Formatted AST & Tables
  ```
- Modular decoupling: Front-end (Lexer/Parser) is cleanly isolated from middle-end (Symbol Table/Type Checker) and back-end (TAC/VM).

---

## Slide 6: Language Specification & Formal Grammar
- **Keywords:** `let`, `const`, `int`, `float`, `bool`, `string`, `void`, `if`, `elif`, `else`, `while`, `for`, `fn`, `return`, `print`
- **Grammar Sample:**
  ```ebnf
  var_decl    ::= ("let" | "const") IDENTIFIER ":" type [ "=" expression ] ";"
  fn_decl     ::= "fn" IDENTIFIER "(" [ param_list ] ")" [ "->" type ] block
  if_stmt     ::= "if" "(" expression ")" block { "elif" "(" expression ")" block } [ "else" block ]
  ```
- Clear distinction between mutable variables (`let`) and immutable constants (`const`).

---

## Slide 7: Innovation & Originality (2 Marks)
1. **Compile-Time Immutability:** Explicit compile-time tracking of `const` vs `let` prevents accidental mutations before code ever runs.
2. **Pedagogical AST Tree Visualizer:** Emits human-readable ASCII syntax trees directly in terminal for debugging and validation.
3. **Panic-Mode Synchronization:** Recovers gracefully from syntax errors, detecting multiple errors in a single compiler pass.

---

## Slide 8: Working Prototype & Live Demonstration (3 Marks)
- **Demo 1:** `python3 src/main.py tests/01_basic_math.zen --all` (Token table, AST tree, and Symbol table).
- **Demo 2:** `python3 src/main.py tests/02_control_flow.zen --ast` (Nested conditional branches and loops in AST).
- **Demo 3:** `python3 src/main.py tests/03_functions.zen --symtab` (Global vs function local scopes).
- **Demo 4:** `python3 src/main.py tests/04_syntax_error.zen` (Line and column error reporting).
- **Demo 5:** `python3 src/main.py --repl` (Live interactive prompt).

---

## Slide 9: Roadmap for Phase 2 and Phase 3
- **Phase 2 (Core Implementation):**
  - Semantic analyzer & static type checker.
  - Three-Address Code (TAC) quadruple generation.
- **Phase 3 (Optimization & Final System):**
  - Machine-independent TAC optimizations (Constant folding, dead code elimination).
  - Virtual machine / TAC execution engine.
  - Final test suites and project report.

---

## Slide 10: Conclusion & References
- **Summary:** Phase 1 successfully completed on schedule with all required deliverables and working prototype.
- **References:**
  - Aho, Lam, Sethi, Ullman (The Dragon Book)
  - Cooper & Torczon (Engineering a Compiler)
  - Louden (Compiler Construction: Principles and Practice)
