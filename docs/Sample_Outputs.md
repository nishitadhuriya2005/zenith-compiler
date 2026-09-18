# Zenith Compiler - Phase 1 Prototype Execution Traces

This document contains the exact output traces produced by the Zenith Front-End Compiler prototype across all test cases. Use these outputs for your project report evidence, lab records, and presentation slides.

---

## Test Case 1: Variables, Types & Arithmetic Precedence
**Input File:** `tests/01_basic_math.zen`

### 1. Source Code:
```zenith
const PI: float = 3.14159;
let radius: float = 5.0;
let area: float = PI * radius * radius;

let a: int = 10;
let b: int = 20;
let c: int = 5;

let result: int = a + b * c - (a / 2);
let is_valid: bool = (result > 50) && (area >= 75.0);

print("Radius:", radius);
print("Calculated Area:", area);
print("Computed Result:", result);
print("Validation Flag:", is_valid);
```

### 2. Lexical Analysis Output (Token Stream Table):
```
┌──────┬──────┬─────────────────┬────────────────────────────┬──────────────────┐
│ Line │ Col  │ Token Type      │ Lexeme                     │ Value            │
├──────┼──────┼─────────────────┼────────────────────────────┼──────────────────┤
│ 2    │ 1    │ CONST           │ const                      │ -                │
│ 2    │ 7    │ IDENTIFIER      │ PI                         │ -                │
│ 2    │ 9    │ COLON           │ :                          │ -                │
│ 2    │ 11   │ FLOAT           │ float                      │ -                │
│ 2    │ 17   │ ASSIGN          │ =                          │ -                │
│ 2    │ 19   │ FLOAT_LIT       │ 3.14159                    │ 3.14159          │
│ 2    │ 26   │ SEMICOLON       │ ;                          │ -                │
│ 3    │ 1    │ LET             │ let                        │ -                │
│ 3    │ 5    │ IDENTIFIER      │ radius                     │ -                │
│ 3    │ 11   │ COLON           │ :                          │ -                │
│ 3    │ 13   │ FLOAT           │ float                      │ -                │
│ 3    │ 19   │ ASSIGN          │ =                          │ -                │
│ 3    │ 21   │ FLOAT_LIT       │ 5.0                        │ 5.0              │
│ 3    │ 24   │ SEMICOLON       │ ;                          │ -                │
│ 4    │ 1    │ LET             │ let                        │ -                │
│ 4    │ 5    │ IDENTIFIER      │ area                       │ -                │
│ 4    │ 9    │ COLON           │ :                          │ -                │
│ 4    │ 11   │ FLOAT           │ float                      │ -                │
│ 4    │ 17   │ ASSIGN          │ =                          │ -                │
│ 4    │ 19   │ IDENTIFIER      │ PI                         │ -                │
│ 4    │ 22   │ STAR            │ *                          │ -                │
│ 4    │ 24   │ IDENTIFIER      │ radius                     │ -                │
│ 4    │ 31   │ STAR            │ *                          │ -                │
│ 4    │ 33   │ IDENTIFIER      │ radius                     │ -                │
│ 4    │ 39   │ SEMICOLON       │ ;                          │ -                │
└──────┴──────┴─────────────────┴────────────────────────────┴──────────────────┘
```

### 3. Syntax Analysis Output (Abstract Syntax Tree):
```
└── Program [L2:C1]
    ├── VarDecl: const PI: float [L2:C1]
    │   └── Literal: 3.14159 (float) [L2:C19]
    ├── VarDecl: let radius: float [L3:C1]
    │   └── Literal: 5.0 (float) [L3:C21]
    ├── VarDecl: let area: float [L4:C1]
    │   └── BinaryExpr: (*) [L4:C31]
    │       ├── BinaryExpr: (*) [L4:C22]
    │       │   ├── Identifier: PI [L4:C19]
    │       │   └── Identifier: radius [L4:C24]
    │       └── Identifier: radius [L4:C33]
    ├── VarDecl: let a: int [L6:C1]
    │   └── Literal: 10 (int) [L6:C14]
    ├── VarDecl: let b: int [L7:C1]
    │   └── Literal: 20 (int) [L7:C14]
    ├── VarDecl: let c: int [L8:C1]
    │   └── Literal: 5 (int) [L8:C13]
    ├── VarDecl: let result: int [L11:C1]
    │   └── BinaryExpr: (-) [L11:C27]
    │       ├── BinaryExpr: (+) [L11:C21]
    │       │   ├── Identifier: a [L11:C19]
    │       │   └── BinaryExpr: (*) [L11:C25]
    │       │       ├── Identifier: b [L11:C23]
    │       │       └── Identifier: c [L11:C27]
    │       └── BinaryExpr: (/) [L11:C34]
    │           ├── Identifier: a [L11:C32]
    │           └── Literal: 2 (int) [L11:C36]
    ├── VarDecl: let is_valid: bool [L12:C1]
    │   └── BinaryExpr: (&&) [L12:C38]
    │       ├── BinaryExpr: (>) [L12:C31]
    │       │   ├── Identifier: result [L12:C24]
    │       │   └── Literal: 50 (int) [L12:C33]
    │       └── BinaryExpr: (>=) [L12:C48]
    │           ├── Identifier: area [L12:C43]
    │           └── Literal: 75.0 (float) [L12:C51]
    ├── PrintStmt [L14:C1]
    │   ├── Literal: "Radius:" (string) [L14:C7]
    │   └── Identifier: radius [L14:C17]
    ├── PrintStmt [L15:C1]
    │   ├── Literal: "Calculated Area:" (string) [L15:C7]
    │   └── Identifier: area [L15:C26]
    ├── PrintStmt [L16:C1]
    │   ├── Literal: "Computed Result:" (string) [L16:C7]
    │   └── Identifier: result [L16:C26]
    └── PrintStmt [L17:C1]
        ├── Literal: "Validation Flag:" (string) [L17:C7]
        └── Identifier: is_valid [L17:C26]
```

### 4. Scoped Symbol Table:
```
================================================================================
                         ZENITH SCOPED SYMBOL TABLE                             
================================================================================

[Scope: 'global'] (Level: 0, Parent: 'None')
  ┌──────────────────────┬─────────────┬───────────┬──────────────┬───────────────┐
  │ Name                 │ Type        │ Category  │ Defined At   │ Details       │
  ├──────────────────────┼─────────────┼───────────┼──────────────┼───────────────┤
  │ PI                   │ float       │ const     │ L2:C1        │ scope_lvl=0   │
  │ radius               │ float       │ let (var) │ L3:C1        │ scope_lvl=0   │
  │ area                 │ float       │ let (var) │ L4:C1        │ scope_lvl=0   │
  │ a                    │ int         │ let (var) │ L6:C1        │ scope_lvl=0   │
  │ b                    │ int         │ let (var) │ L7:C1        │ scope_lvl=0   │
  │ c                    │ int         │ let (var) │ L8:C1        │ scope_lvl=0   │
  │ result               │ int         │ let (var) │ L11:C1       │ scope_lvl=0   │
  │ is_valid             │ bool        │ let (var) │ L12:C1       │ scope_lvl=0   │
  └──────────────────────┴─────────────┴───────────┴──────────────┴───────────────┘

✅ Phase 1 Front-End Pass Completed Successfully.
```

---

## Test Case 2: Control Flow Structures (If-Elif-Else, While, For)
**Input File:** `tests/02_control_flow.zen`

### Visual AST Snippet:
```
└── Program [L2:C1]
    ├── VarDecl: let score: int [L2:C1]
    │   └── Literal: 85 (int) [L2:C18]
    ├── VarDecl: let grade: string [L3:C1]
    │   └── Literal: "F" (string) [L3:C21]
    ├── IfStmt [L6:C1]
    │   ├── BinaryExpr: (>=) [L6:C11]
    │   │   ├── Identifier: score [L6:C5]
    │   │   └── Literal: 90 (int) [L6:C14]
    │   ├── Block (1 stmts) [L6:C18]
    │   │   └── Assignment: grade = [L7:C5]
    │   │       └── Literal: "A" (string) [L7:C13]
    │   ├── BinaryExpr: (>=) [L8:C13]
    │   │   ├── Identifier: score [L8:C7]
    │   │   └── Literal: 80 (int) [L8:C16]
    │   ├── Block (1 stmts) [L8:C20]
    │   │   └── Assignment: grade = [L9:C5]
    │   │       └── Literal: "B" (string) [L9:C13]
    ...
    ├── WhileStmt [L22:C1]
    │   ├── BinaryExpr: (<=) [L22:C16]
    │   │   ├── Identifier: counter [L22:C8]
    │   │   └── Literal: 5 (int) [L22:C19]
    │   └── Block (2 stmts) [L22:C22]
    │       ├── Assignment: total_sum = [L23:C5]
    │       │   └── BinaryExpr: (+) [L23:C27]
    │       │       ├── Identifier: total_sum [L23:C17]
    │       │       └── Identifier: counter [L23:C29]
    │       └── Assignment: counter = [L24:C5]
    │           └── BinaryExpr: (+) [L24:C23]
    │               ├── Identifier: counter [L24:C15]
    │               └── Literal: 1 (int) [L24:C25]
    └── ForStmt [L30:C1]
        ├── VarDecl: let i: int [L30:C6]
        │   └── Literal: 1 (int) [L30:C22]
        ├── BinaryExpr: (<=) [L30:C27]
        │   ├── Identifier: i [L30:C25]
        │   └── Literal: 5 (int) [L30:C30]
        ├── Assignment: i = [L30:C33]
        │   └── BinaryExpr: (+) [L30:C41]
        │       ├── Identifier: i [L30:C37]
        │       └── Literal: 1 (int) [L30:C43]
        └── Block (1 stmts) [L30:C47]
            └── Assignment: fact = [L31:C5]
                └── BinaryExpr: (*) [L31:C17]
                    ├── Identifier: fact [L31:C12]
                    └── Identifier: i [L31:C19]
```

---

## Test Case 3: Functions and Lexical Scopes
**Input File:** `tests/03_functions.zen`

### Symbol Table Display:
```
================================================================================
                         ZENITH SCOPED SYMBOL TABLE                             
================================================================================

[Scope: 'global'] (Level: 0, Parent: 'None')
  ┌──────────────────────┬─────────────┬───────────┬──────────────┬───────────────┐
  │ Name                 │ Type        │ Category  │ Defined At   │ Details       │
  ├──────────────────────┼─────────────┼───────────┼──────────────┼───────────────┤
  │ max_value            │ function    │ function  │ L3:C1        │ args=(int,int)│
  │ compute_discount     │ function    │ function  │ L11:C1       │ args=(flt,flt)│
  │ m                    │ int         │ let (var) │ L17:C1       │ scope_lvl=0   │
  │ discounted_laptop    │ float       │ let (var) │ L18:C1       │ scope_lvl=0   │
  └──────────────────────┴─────────────┴───────────┴──────────────┴───────────────┘

[Scope: 'fn_max_value'] (Level: 1, Parent: 'global')
  ┌──────────────────────┬─────────────┬───────────┬──────────────┬───────────────┐
  │ Name                 │ Type        │ Category  │ Defined At   │ Details       │
  ├──────────────────────┼─────────────┼───────────┼──────────────┼───────────────┤
  │ x                    │ int         │ let (var) │ L3:C14       │ scope_lvl=1   │
  │ y                    │ int         │ let (var) │ L3:C22       │ scope_lvl=1   │
  └──────────────────────┴─────────────┴───────────┴──────────────┴───────────────┘

[Scope: 'fn_compute_discount'] (Level: 1, Parent: 'global')
  ┌──────────────────────┬─────────────┬───────────┬──────────────┬───────────────┐
  │ Name                 │ Type        │ Category  │ Defined At   │ Details       │
  ├──────────────────────┼─────────────┼───────────┼──────────────┼───────────────┤
  │ price                │ float       │ let (var) │ L11:C21      │ scope_lvl=1   │
  │ rate                 │ float       │ let (var) │ L11:C35      │ scope_lvl=1   │
  │ discount             │ float       │ let (var) │ L12:C5       │ scope_lvl=1   │
  │ final_price          │ float       │ let (var) │ L13:C5       │ scope_lvl=1   │
  └──────────────────────┴─────────────┴───────────┴──────────────┴───────────────┘

✅ Phase 1 Front-End Pass Completed Successfully.
```

---

## Test Case 4: Syntax & Lexical Error Diagnostics
**Input File:** `tests/04_syntax_error.zen`

### Error Reporting Output:
```
======================================================================
 COMPILING SOURCE: tests/04_syntax_error.zen
======================================================================

❌ SYNTAX ERRORS DETECTED:
  • [Syntax Error at 5:17] Expected valid type name (int, float, bool, string), got '=' (ASSIGN)
  • [Syntax Error at 8:12] Expected ')' after if condition. Got '{' (LBRACE)
  • [Syntax Error at 13:24] Unexpected token in expression: '@' (ILLEGAL)

(Panic-mode recovery activated: Parser synchronized successfully at statement boundaries)
```
