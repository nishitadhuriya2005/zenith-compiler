# Zenith Compiler - Review 1 Viva Defense & Technical Q&A Guide

This guide prepares you to answer theoretical, architectural, and code-level questions during your **Review 1 (Phase 1)** project evaluation.

---

## 1. Project Relevance & Core Concepts

### Q1: What is the core objective of the Zenith compiler project?
**Answer:**
"The objective of Zenith is to design and implement a strongly-typed, procedural compiled language with an explicit multi-pass compiler pipeline. It demonstrates the complete compiler lifecycle: Lexical analysis, LL(1) recursive descent parsing, Abstract Syntax Tree (AST) construction, scoped symbol table management, intermediate Three-Address Code (TAC) generation, and execution via a virtual machine. In Phase 1, we have implemented the front-end scanning, parsing, AST generation, and scoped symbol table."

### Q2: Why choose a Recursive Descent Parser instead of Lex/Yacc or Flex/Bison?
**Answer:**
1. **Transparency & Maintainability:** Hand-written recursive descent mirrors the grammar productions directly in code. Every function in `parser.py` corresponds to an EBNF non-terminal (e.g., `_statement()`, `_var_decl()`, `_if_stmt()`), making it intuitive to debug, explain, and modify during reviews.
2. **Superior Error Diagnostics:** Table-driven LALR parsers (like Yacc/Bison) generate cryptic syntax error messages unless heavily customized. With recursive descent, we have exact source line and column numbers and implement panic-mode recovery to continue parsing after errors.
3. **No External Dependencies:** Eliminates toolchain compatibility issues, making the compiler portable across platforms.

### Q3: What is the difference between a Concrete Parse Tree (CST) and an Abstract Syntax Tree (AST)?
**Answer:**
"A Concrete Parse Tree (CST) contains every terminal and non-terminal from the grammar derivation, including punctuation such as parentheses, semicolons, and commas. An Abstract Syntax Tree (AST) condenses this representation to retain only the semantic structure and operators. For example, in an assignment like `let x: int = 10 + 20;`, the CST contains nodes for `let`, `:`, `int`, `=`, `;`, whereas the AST stores a single `VarDecl` node containing `name='x'`, `type='int'`, and an initializer pointing to a `BinaryExpr(+)` with children `Literal(10)` and `Literal(20)`."

---

## 2. Lexical Analysis (Lexer)

### Q4: How does the Lexer distinguish between an Identifier and a Keyword?
**Answer:**
"When the lexer encounters an alphabetic character or underscore, it scans ahead while characters are alphanumeric or underscores to extract the full lexeme. It then performs an $O(1)$ hash table lookup in `KEYWORDS`:
```python
token_type = KEYWORDS.get(lexeme, TokenType.IDENTIFIER)
```
If the lexeme exists in the dictionary (e.g., `'let'`, `'if'`, `'while'`), it is classified as that keyword's `TokenType`. If not found, it defaults to `TokenType.IDENTIFIER`."

### Q5: How does the Lexer handle multi-character operators like `==`, `<=`, and `->`?
**Answer:**
"Using lookahead with the `_match()` helper method. When the scanner encounters `=`, it peeks at the next character. If the next character is `=`, it consumes both and produces `TokenType.EQ_EQ` (`==`). If not, it produces `TokenType.ASSIGN` (`=`). The same lookahead logic handles `-` vs `->`, `<` vs `<=`, and `!` vs `!=`."

### Q6: How does the Lexer track source coordinates for error reporting?
**Answer:**
"The Lexer maintains two state counters: `line` (starting at 1) and `column` (starting at 1). Whenever a newline character `\n` is encountered, `line` is incremented and `column` is reset to 1. For every other character consumed, `column` is incremented. When constructing a `Token`, the snapshot of `line` and `column` at the start of the token is saved into the token dataclass."

---

## 3. Syntax Analysis (Parser)

### Q7: How does your parser eliminate left recursion and handle operator precedence?
**Answer:**
"Left recursion is eliminated by formulating the grammar using iterative loops (EBNF `{ ... }`) and using a **precedence hierarchy (operator precedence climbing)**.
Each precedence tier has its own parsing method calling the next higher tier:
1. `_expression()` $\to$ `_logical_or()` (`||`)
2. `_logical_and()` (`&&`)
3. `_equality()` (`==`, `!=`)
4. `_relational()` (`<`, `<=`, `>`, `>=`)
5. `_additive()` (`+`, `-`)
6. `_multiplicative()` (`*`, `/`, `%`)
7. `_unary()` (`-`, `!`)
8. `_primary()` (Literals, Identifiers, Parenthesized subexpressions)

Because multiplicative operators are lower in the call stack than additive operators, `a + b * c` parses `b * c` first, correctly binding `*` tighter than `+`."

### Q8: What is panic-mode error recovery and how is it implemented?
**Answer:**
"When a syntax error occurs (e.g., missing semicolon or mismatched parenthesis), the parser raises a `ParserError`. Rather than terminating the entire compiler run, the error is logged into `self.errors`, and the parser invokes `_synchronize()`. The synchronizer discards tokens until it encounters either a statement boundary (`TokenType.SEMICOLON`) or a statement-starting keyword (`let`, `if`, `while`, `fn`, etc.). This allows the parser to recover and continue scanning for subsequent syntax errors in the file."

---

## 4. Symbol Table Management

### Q9: How is the scoped symbol table organized?
**Answer:**
"The symbol table is organized as an **environment tree with parent links**.
Each `Scope` object contains:
- `name`: Identifier for the scope (e.g., `'global'`, `'fn_max_value'`, `'if_branch'`).
- `level`: The nesting depth integer ($0$ for global, $1+$ for nested).
- `symbols`: A hash map of `name -> Symbol`.
- `parent`: A reference pointer to the enclosing outer scope.

When entering a function or code block, `symtab.enter_scope()` creates a new `Scope` whose parent points to `current_scope`. When exiting, `symtab.exit_scope()` restores `current_scope = current_scope.parent`."

### Q10: How does identifier lookup work across nested scopes?
**Answer:**
"Lookup follows lexical scoping rules:
```python
def lookup(self, name: str) -> Optional[Symbol]:
    if name in self.symbols:
        return self.symbols[name]
    if self.parent is not None:
        return self.parent.lookup(name)
    return None
```
It first inspects the local scope's dictionary. If not found, it recursively searches the parent scope until it either finds the declaration or reaches the global scope (returning `None` for undeclared identifiers)."

### Q11: How do you enforce the distinction between `let` and `const`?
**Answer:**
"During variable declaration parsing, the keyword is checked: `let` sets `is_const = False`, whereas `const` sets `is_const = True`. In the symbol table, the `Symbol` records this `is_const` flag. Whenever an `Assignment` statement (`x = ...`) is parsed or validated, the compiler looks up `x` in the symbol table. If `sym.is_const == True`, a semantic error is raised: *'Cannot reassign to constant variable'*, preventing mutation at compile-time."

---

## 5. Demonstration & Live Commands

### How to execute and demonstrate the prototype during Review 1:
```bash
# Navigate to compiler folder
cd /Users/apple/.gemini/antigravity/scratch/zenith-compiler

# 1. Run full compilation pass on basic math test program (Tokens, AST, and Symbol Table)
python3 src/main.py tests/01_basic_math.zen --all

# 2. Run control flow test program displaying the ASCII Abstract Syntax Tree
python3 src/main.py tests/02_control_flow.zen --ast

# 3. Run functions test program displaying the hierarchical Scoped Symbol Table
python3 src/main.py tests/03_functions.zen --symtab

# 4. Demonstrate syntax error recovery and diagnostic reporting
python3 src/main.py tests/04_syntax_error.zen

# 5. Launch interactive REPL for live demonstration with the evaluators
python3 src/main.py --repl
```
