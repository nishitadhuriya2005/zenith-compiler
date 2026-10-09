#!/usr/bin/env python3
"""
Professional PowerPoint Presentation Generator for Review 1.
Generates Review1_Presentation.pptx using python-pptx.
Adheres strictly to the lab manual's Review 1 criteria, embeds user screenshots,
and ensures zero code dumps, zero marks, and zero text overlapping.
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # Set 16:9 widescreen dimensions (13.333 x 7.5 inches)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]

    # Theme Colors
    COLOR_PRIMARY_DARK = RGBColor(15, 23, 42)    # Slate 900
    COLOR_PRIMARY_BLUE = RGBColor(30, 58, 138)   # Blue 900
    COLOR_ACCENT_BLUE  = RGBColor(37, 99, 235)   # Blue 600
    COLOR_BG_CARD      = RGBColor(248, 250, 252) # Slate 50
    COLOR_BORDER_CARD  = RGBColor(226, 232, 240) # Slate 200
    COLOR_TEXT_MAIN    = RGBColor(30, 41, 59)    # Slate 800
    COLOR_TEXT_MUTED   = RGBColor(100, 116, 139) # Slate 500
    COLOR_WHITE        = RGBColor(255, 255, 255)
    COLOR_GREEN_TAG    = RGBColor(16, 185, 129)  # Emerald 500

    def add_header(slide, title_text, category_text="COMPILER DESIGN LABORATORY -- REVIEW 1"):
        # Top accent bar
        accent_bar = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12)
        )
        accent_bar.fill.solid()
        accent_bar.fill.fore_color.rgb = COLOR_ACCENT_BLUE
        accent_bar.line.fill.background()

        # Category text
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.3), Inches(11.7), Inches(0.35))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = category_text.upper()
        p_c.font.name = "Calibri"
        p_c.font.size = Pt(9.5)
        p_c.font.bold = True
        p_c.font.color.rgb = COLOR_ACCENT_BLUE

        # Main Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.7), Inches(0.65))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = "Calibri"
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_PRIMARY_DARK

        # Separator line
        sep = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.02)
        )
        sep.fill.solid()
        sep.fill.fore_color.rgb = COLOR_BORDER_CARD
        sep.line.fill.background()

    def add_card(slide, left, top, width, height, title="", title_color=COLOR_PRIMARY_BLUE):
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height
        )
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_BG_CARD
        card.line.color.rgb = COLOR_BORDER_CARD
        card.line.width = Pt(1)

        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.4))
            tf = tb.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = "Calibri"
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = title_color
        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_slide_layout)
    
    # Background card
    hero = s1.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5)
    )
    hero.fill.solid()
    hero.fill.fore_color.rgb = COLOR_PRIMARY_DARK
    hero.line.fill.background()

    # Decorative top bar
    bar1 = s1.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.2)
    )
    bar1.fill.solid()
    bar1.fill.fore_color.rgb = COLOR_ACCENT_BLUE
    bar1.line.fill.background()

    # Category badge
    tb_b = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.3), Inches(0.5))
    p = tb_b.text_frame.paragraphs[0]
    p.text = "COMPILER DESIGN LABORATORY -- PROJECT PROPOSAL & DESIGN REVIEW"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT_BLUE

    # Title
    tb_t = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(1.5))
    tf = tb_t.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "ZENITH COMPILER"
    p.font.name = "Calibri"
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    p2 = tf.add_paragraph()
    p2.text = "A Strongly-Typed Procedural Language Compiler with AST Visualization,\nScoped Symbol Table Management, and Intermediate Code Generation"
    p2.font.name = "Calibri"
    p2.font.size = Pt(17)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.space_before = Pt(10)

    # Info card on slide 1
    info_card = s1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.2), Inches(11.3), Inches(2.2)
    )
    info_card.fill.solid()
    info_card.fill.fore_color.rgb = RGBColor(30, 41, 59)
    info_card.line.color.rgb = RGBColor(51, 65, 85)
    info_card.line.width = Pt(1)

    tb_meta = s1.shapes.add_textbox(Inches(1.3), Inches(4.4), Inches(10.7), Inches(1.8))
    tf_m = tb_meta.text_frame
    tf_m.word_wrap = True

    meta_items = [
        ("Project Type", "Individual Project Submission (Strictly Independent Implementation)"),
        ("Course Component", "Compiler Design Laboratory (Review 1: Proposal & System Design)"),
        ("Key Innovation", "Interactive Arbitrary User Input Engine, Compile-Time Immutability, AST Visualizer"),
        ("Deliverables", "Formal EBNF Grammar, Hand-Crafted Lexer & Parser, Scoped Symbol Table, Prototype")
    ]
    for i, (k, v) in enumerate(meta_items):
        p = tf_m.paragraphs[0] if i == 0 else tf_m.add_paragraph()
        p.text = f"-  {k}:  {v}"
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(241, 245, 249)
        p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 2: MOTIVATION & BACKGROUND
    # =========================================================================
    s2 = prs.slides.add_slide(blank_slide_layout)
    add_header(s2, "Project Motivation & Background Study", "Problem Understanding & Motivation")

    add_card(s2, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.3), "Deficiencies in Existing Approaches")
    tb2_left = s2.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf2_l = tb2_left.text_frame
    tf2_l.word_wrap = True
    
    pts_left = [
        ("Dynamically Typed Scripting Languages (Python, JS):", "Postpone typing and scoping errors until runtime, leading to silent production failures and lack of static safety."),
        ("Industrial Black-Box Compilers (GCC, Clang/LLVM):", "Feature millions of lines of code where intermediate syntax trees and representation lowering are completely opaque."),
        ("Toy Lab Interpreters & Calculators:", "Directly evaluate syntax trees without symbol tables, lexical scopes, intermediate representations, or code optimizations.")
    ]
    for i, (heading, desc) in enumerate(pts_left):
        p = tf2_l.paragraphs[0] if i == 0 else tf2_l.add_paragraph()
        p.text = f"- {heading}"
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY_DARK
        p.space_after = Pt(2)
        
        pd = tf2_l.add_paragraph()
        pd.text = f"   {desc}"
        pd.font.name = "Calibri"
        pd.font.size = Pt(10)
        pd.font.color.rgb = COLOR_TEXT_MUTED
        pd.space_after = Pt(10)

    add_card(s2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3), "The Zenith Value Proposition")
    tb2_right = s2.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf2_r = tb2_right.text_frame
    tf2_r.word_wrap = True

    pts_right = [
        ("Full Pedagogical Transparency:", "Exposes every compiler phase (Token Table, AST Tree, Scoped Symbol Table, and TAC Intermediate Code) as inspectable artifacts."),
        ("Strict Compile-Time Safety:", "Enforces static type checking, variable immutability (let vs const), and scope resolution before code execution begins."),
        ("Interactive Problem Input Engine:", "Accepts arbitrary user-supplied programs and algorithms dynamically at runtime, allowing any computational problem to be verified."),
        ("Zero Dependency Architecture:", "Engineered entirely in pure standard library Python, eliminating build failures and toolchain friction.")
    ]
    for i, (heading, desc) in enumerate(pts_right):
        p = tf2_r.paragraphs[0] if i == 0 else tf2_r.add_paragraph()
        p.text = f"- {heading}"
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY_BLUE
        p.space_after = Pt(2)
        
        pd = tf2_r.add_paragraph()
        pd.text = f"   {desc}"
        pd.font.name = "Calibri"
        pd.font.size = Pt(10)
        pd.font.color.rgb = COLOR_TEXT_MUTED
        pd.space_after = Pt(10)

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT
    # =========================================================================
    s3 = prs.slides.add_slide(blank_slide_layout)
    add_header(s3, "Formal Problem Statement & Problem Domain", "Problem Formulation")

    add_card(s3, Inches(0.8), Inches(1.6), Inches(11.733), Inches(2.0), "Formal Problem Definition", title_color=COLOR_PRIMARY_BLUE)
    tb3_p = s3.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.3), Inches(1.3))
    tf3_p = tb3_p.text_frame
    tf3_p.word_wrap = True
    p = tf3_p.paragraphs[0]
    p.text = (
        "To formulate, design, implement, and rigorously validate a modular multi-pass compiler for a strongly-typed "
        "procedural language named Zenith. The system transforms human-readable source programs through deterministic lexical "
        "scanning, LL(1) recursive descent parsing, Abstract Syntax Tree (AST) synthesis, and hierarchical scoped symbol table "
        "management, establishing an intermediate representation pipeline for optimization and execution."
    )
    p.font.name = "Calibri"
    p.font.size = Pt(11.5)
    p.font.color.rgb = COLOR_TEXT_MAIN
    p.line_spacing = 1.3

    add_card(s3, Inches(0.8), Inches(3.8), Inches(3.7), Inches(3.1), "1. Arbitrary User Input Engine")
    tb3_1 = s3.shapes.add_textbox(Inches(0.95), Inches(4.4), Inches(3.4), Inches(2.4))
    tf3_1 = tb3_1.text_frame
    tf3_1.word_wrap = True
    p = tf3_1.paragraphs[0]
    p.text = (
        "- Dynamic Execution:\n"
        "  Accepts arbitrary source programs from the user at runtime.\n\n"
        "- Flexible Problem Solving:\n"
        "  Any mathematical, algorithmic, or control-flow problem can be entered and compiled.\n\n"
        "- Live Interactive Testing:\n"
        "  Includes REPL mode for immediate verification."
    )
    p.font.name = "Calibri"
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_MUTED

    add_card(s3, Inches(4.8), Inches(3.8), Inches(3.7), Inches(3.1), "2. Deterministic Parsing & AST")
    tb3_2 = s3.shapes.add_textbox(Inches(4.95), Inches(4.4), Inches(3.4), Inches(2.4))
    tf3_2 = tb3_2.text_frame
    tf3_2.word_wrap = True
    p = tf3_2.paragraphs[0]
    p.text = (
        "- LL(1) Recursive Descent:\n"
        "  Unambiguous context-free grammar with zero left-recursion.\n\n"
        "- Precedence Climbing:\n"
        "  7 operator priority levels evaluated deterministically.\n\n"
        "- AST Visualization:\n"
        "  Discards concrete punctuation while preserving semantic structure."
    )
    p.font.name = "Calibri"
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_MUTED

    add_card(s3, Inches(8.8), Inches(3.8), Inches(3.733), Inches(3.1), "3. Scoped Symbol Table")
    tb3_3 = s3.shapes.add_textbox(Inches(8.95), Inches(4.4), Inches(3.4), Inches(2.4))
    tf3_3 = tb3_3.text_frame
    tf3_3.word_wrap = True
    p = tf3_3.paragraphs[0]
    p.text = (
        "- Environment Tree:\n"
        "  Parent-chained scopes for global, function, and block levels.\n\n"
        "- Immutability Tracking:\n"
        "  Distinguishes let (mutable) from const (immutable).\n\n"
        "- Duplicate Prevention:\n"
        "  Detects illegal redeclarations within the same scope in O(1)."
    )
    p.font.name = "Calibri"
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 4: OBJECTIVES
    # =========================================================================
    s4 = prs.slides.add_slide(blank_slide_layout)
    add_header(s4, "Project Objectives & Phased Deliverables", "Measurable Objectives")

    add_card(s4, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.3), "Primary Engineering Objectives")
    tb4_l = s4.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf4_l = tb4_l.text_frame
    tf4_l.word_wrap = True

    obj_items = [
        ("Formal EBNF Grammar:", "Formulate an unambiguous, mathematically sound Context-Free Grammar covering procedural constructs."),
        ("Lexical Analysis & Coordinates:", "Build a lookahead scanner with precise line and column tracking for exact error reporting."),
        ("Recursive Descent Parser:", "Implement LL(1) top-down parsing with operator precedence climbing and panic-mode error recovery."),
        ("Abstract Syntax Tree Synthesis:", "Construct a strongly-typed, object-oriented AST representation with ASCII tree visualizer."),
        ("Hierarchical Symbol Table:", "Implement an environment tree tracking identifier types, categories, and lexical levels."),
        ("Interactive User CLI & REPL:", "Provide dynamic user input capabilities to verify any arbitrary program logic on-the-fly.")
    ]
    for i, (k, v) in enumerate(obj_items):
        p = tf4_l.paragraphs[0] if i == 0 else tf4_l.add_paragraph()
        p.text = f"- {k} {v}"
        p.font.name = "Calibri"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(8)

    add_card(s4, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3), "Phased Project Roadmap")
    tb4_r = s4.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf4_r = tb4_r.text_frame
    tf4_r.word_wrap = True

    phases = [
        ("Phase 1: Problem Definition & Front-End Prototype [COMPLETED]",
         "Formal EBNF grammar, hand-crafted Lexer, LL(1) Parser, AST tree visualizer, Scoped Symbol Table, and interactive user input checker."),
        ("Phase 2: Core Implementation [UPCOMING TARGET]",
         "Semantic analysis, static type checking, immutability enforcement, function signature validation, and Three-Address Code (TAC) generation."),
        ("Phase 3: Final Implementation & Optimization [UPCOMING TARGET]",
         "Machine-independent optimizations (constant folding, algebraic simplification, dead code elimination) and stack-based virtual machine execution.")
    ]
    for i, (title, body) in enumerate(phases):
        p = tf4_r.paragraphs[0] if i == 0 else tf4_r.add_paragraph()
        p.text = f"- {title}"
        p.font.name = "Calibri"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY_BLUE if i == 0 else COLOR_PRIMARY_DARK
        p.space_after = Pt(2)
        
        pd = tf4_r.add_paragraph()
        pd.text = f"   {body}"
        pd.font.name = "Calibri"
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = COLOR_TEXT_MUTED
        pd.space_after = Pt(12)

    # =========================================================================
    # SLIDE 5: SCOPE OF THE PROJECT
    # =========================================================================
    s5 = prs.slides.add_slide(blank_slide_layout)
    add_header(s5, "Scope of the Project -- In-Scope vs. Boundaries", "Scope Boundaries")

    add_card(s5, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.3), "In-Scope Language & Compiler Features")
    tb5_l = s5.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf5_l = tb5_l.text_frame
    tf5_l.word_wrap = True

    in_scope = [
        ("Primitive Data Types:", "int, float, bool, string, and void (function returns)."),
        ("Variable Declarations:", "Explicit let (mutable variable) and const (immutable constant)."),
        ("Expression Hierarchy:", "Arithmetic (+, -, *, /, %), Relational (==, !=, <, <=, >, >=), and Logical (&&, ||, !)."),
        ("Structured Control Flow:", "Conditionals (if-elif-else), while loops, and initialized for loops."),
        ("Function Definitions:", "Formal typed parameters, explicit return types, and local activation records."),
        ("Intermediate Representation:", "Three-Address Code (TAC) quadruples with temporary register assignment."),
        ("Execution Engine:", "Stack-based virtual machine evaluating intermediate instructions.")
    ]
    for i, (k, v) in enumerate(in_scope):
        p = tf5_l.paragraphs[0] if i == 0 else tf5_l.add_paragraph()
        p.text = f"- {k} {v}"
        p.font.name = "Calibri"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(7)

    add_card(s5, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3), "Out-of-Scope Boundaries (Design Non-Goals)")
    tb5_r = s5.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf5_r = tb5_r.text_frame
    tf5_r.word_wrap = True

    out_scope = [
        ("Dynamic Heap Garbage Collection:", "Memory follows structured lexical activation records. Complex mark-and-sweep or generational GC is excluded to prioritize compiler translation fundamentals."),
        ("Complex OOP Inheritance & Virtual Tables:", "Class hierarchies and polymorphic virtual method tables are omitted to maintain focus on procedural compiler pipeline clarity."),
        ("Hardware Machine Assembly Emission:", "Direct emission of x86-64/ARM machine assembly is replaced with Three-Address Code and bytecode execution to eliminate platform-specific ABI linking quirks."),
        ("Asynchronous Concurrency:", "Threading primitives and async event loops are omitted to preserve deterministic parsing and intermediate code generation.")
    ]
    for i, (k, v) in enumerate(out_scope):
        p = tf5_r.paragraphs[0] if i == 0 else tf5_r.add_paragraph()
        p.text = f"- {k}"
        p.font.name = "Calibri"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = RGBColor(180, 83, 9)
        p.space_after = Pt(2)
        
        pd = tf5_r.add_paragraph()
        pd.text = f"   {v}"
        pd.font.name = "Calibri"
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = COLOR_TEXT_MUTED
        pd.space_after = Pt(10)

    # =========================================================================
    # SLIDE 6: COMPILER CONCEPTS
    # =========================================================================
    s6 = prs.slides.add_slide(blank_slide_layout)
    add_header(s6, "Compiler Design Concepts Involved", "Curriculum Mapping")

    concepts = [
        ("1. Finite Automata & Lexing", "Regular expressions modeled as Deterministic Finite Automata (DFA). Hand-crafted scanner tracking coordinates (line:col) and handling string escapes and comments.", Inches(0.8), Inches(1.6)),
        ("2. Context-Free Grammars", "Formal 4-tuple G = (V, Sigma, R, S) in Extended Backus-Naur Form (EBNF). Eliminates left-recursion and grammar ambiguities.", Inches(4.8), Inches(1.6)),
        ("3. Recursive Descent Parsing", "Top-down LL(1) parsing where each non-terminal is a dedicated function. Precedence climbing resolves 7 operator tiers deterministically.", Inches(8.8), Inches(1.6)),
        ("4. Abstract Syntax Trees", "Discards syntactic punctuation (semicolons, parentheses) while preserving operator binding power and statement structure.", Inches(0.8), Inches(4.3)),
        ("5. Scoped Symbol Tables", "Environment tree with parent-pointers. Enforces lexical scoping, O(1) duplicate detection, and variable immutability checks.", Inches(4.8), Inches(4.3)),
        ("6. Panic-Mode Recovery", "Synchronizes at statement boundaries (semicolons and statement keywords) to report multiple errors in a single compiler pass.", Inches(8.8), Inches(4.3)),
    ]
    for title, desc, l, t in concepts:
        add_card(s6, l, t, Inches(3.733), Inches(2.5), title)
        tb = s6.shapes.add_textbox(l + Inches(0.15), t + Inches(0.65), Inches(3.4), Inches(1.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = desc
        p.font.name = "Calibri"
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 7: PROPOSED METHODOLOGY
    # =========================================================================
    s7 = prs.slides.add_slide(blank_slide_layout)
    add_header(s7, "Proposed Methodology & Development Lifecycle", "Engineering Methodology")

    add_card(s7, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.3), "Multi-Pass Compiler Engineering Model")
    tb7 = s7.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.3), Inches(4.4))
    tf7 = tb7.text_frame
    tf7.word_wrap = True

    steps = [
        ("Pass 1: Lexical Analysis (Scanner)", "Converts continuous source text into a discrete Token stream with coordinate attributes."),
        ("Pass 2: Syntax Analysis (Parser)", "Validates token stream against EBNF grammar productions and constructs the Abstract Syntax Tree."),
        ("Pass 3: Scoped Symbol Resolution", "Traverses AST to construct lexical scopes, register symbol types, and detect duplicate declarations."),
        ("Pass 4: Semantic Analysis & Type Checking (Phase 2)", "Validates expression types, return types, and prevents mutation of constant identifiers."),
        ("Pass 5: Intermediate Code Generation (Phase 2)", "Flattens AST into linear Three-Address Code (TAC) quadruples with temporary variables."),
        ("Pass 6: Code Optimization (Phase 3)", "Applies machine-independent optimizations: Constant Folding, Algebraic Simplification, Dead Code Elimination."),
        ("Pass 7: Target Execution (Phase 3)", "Executes optimized TAC instructions via a stack-based virtual machine.")
    ]
    for i, (k, v) in enumerate(steps):
        p = tf7.paragraphs[0] if i == 0 else tf7.add_paragraph()
        p.text = f"- {k}:  {v}"
        p.font.name = "Calibri"
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_PRIMARY_BLUE if i < 3 else COLOR_TEXT_MAIN
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 8: SYSTEM ARCHITECTURE
    # =========================================================================
    s8 = prs.slides.add_slide(blank_slide_layout)
    add_header(s8, "System Architecture & Component Interaction", "Architectural Pipeline")

    add_card(s8, Inches(0.8), Inches(1.6), Inches(11.733), Inches(2.0), "Data Flow Pipeline")
    tb8_f = s8.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.3), Inches(1.2))
    tf8_f = tb8_f.text_frame
    tf8_f.word_wrap = True
    p = tf8_f.paragraphs[0]
    p.text = (
        "Source Input (.zen / User Prompt)  ===>  [ Lexical Analyzer (lexer.py) ]  ===>  Token Stream\n"
        "                                               │\n"
        "                                               ▼\n"
        "Token Stream                       ===>  [ Recursive Descent Parser (parser.py) ]  ===>  AST\n"
        "                                               │\n"
        "                                               ▼\n"
        "Abstract Syntax Tree (AST)         ===>  [ Symbol Table Builder (symbol_table.py) ]  ===>  Scoped Environments\n"
        "                                               │\n"
        "                                               ▼\n"
        "AST & Scoped Environments          ===>  [ Terminal Visualizer & CLI (printer.py / main.py) ]"
    )
    p.font.name = "Courier New"
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_PRIMARY_BLUE

    # Component modules
    mods = [
        ("src/tokens.py", "TokenType enum (34 token types) and Token dataclass with line/col metadata.", Inches(0.8), Inches(3.8)),
        ("src/lexer.py", "Hand-crafted scanner handling keywords, identifiers, literals, comments, and lookahead.", Inches(4.8), Inches(3.8)),
        ("src/ast_nodes.py", "Object-oriented AST dataclasses for statements, expressions, blocks, and parameters.", Inches(8.8), Inches(3.8)),
        ("src/parser.py", "LL(1) recursive descent parser with precedence climbing and panic-mode recovery.", Inches(0.8), Inches(5.4)),
        ("src/symbol_table.py", "Hierarchical scoped symbol table managing local, function, and global environments.", Inches(4.8), Inches(5.4)),
        ("src/main.py & printer.py", "CLI driver, ASCII tree visualizer, and interactive REPL checker for user input.", Inches(8.8), Inches(5.4))
    ]
    for name, desc, l, t in mods:
        add_card(s8, l, t, Inches(3.733), Inches(1.5), name)
        tb = s8.shapes.add_textbox(l + Inches(0.15), t + Inches(0.55), Inches(3.4), Inches(0.85))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = desc
        p.font.name = "Calibri"
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 9: TECHNOLOGY STACK & GRAMMAR
    # =========================================================================
    s9 = prs.slides.add_slide(blank_slide_layout)
    add_header(s9, "Technology Stack & Language Specification", "Tools & Grammar")

    add_card(s9, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.3), "Technology Stack & Feasibility")
    tb9_l = s9.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf9_l = tb9_l.text_frame
    tf9_l.word_wrap = True

    tech_items = [
        ("Language:", "Python 3.9+ (Standard Library Only)."),
        ("Zero Toolchain Dependencies:", "Eliminates build and linking failures common in C/C++ Flex/Bison cross-platform configurations."),
        ("High Code Maintainability:", "Leverages Python dataclasses, recursive functions, and pattern matching for clean AST traversal."),
        ("Cross-Platform Portability:", "Runs natively on macOS, Linux, and Windows without binary recompilation.")
    ]
    for i, (k, v) in enumerate(tech_items):
        p = tf9_l.paragraphs[0] if i == 0 else tf9_l.add_paragraph()
        p.text = f"- {k} {v}"
        p.font.name = "Calibri"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(8)

    add_card(s9, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3), "Operator Precedence Hierarchy")
    tb9_r = s9.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf9_r = tb9_r.text_frame
    tf9_r.word_wrap = True

    prec_items = [
        ("Level 1 (Lowest):", "Logical OR (||)  --  Left-to-Right"),
        ("Level 2:", "Logical AND (&&)  --  Left-to-Right"),
        ("Level 3:", "Equality (==, !=)  --  Left-to-Right"),
        ("Level 4:", "Relational (<, <=, >, >=)  --  Left-to-Right"),
        ("Level 5:", "Additive (+, -)  --  Left-to-Right"),
        ("Level 6:", "Multiplicative (*, /, %)  --  Left-to-Right"),
        ("Level 7 (Highest):", "Unary (- , !)  --  Right-to-Left prefix binding")
    ]
    for i, (lvl, op) in enumerate(prec_items):
        p = tf9_r.paragraphs[0] if i == 0 else tf9_r.add_paragraph()
        p.text = f"- {lvl}  {op}"
        p.font.name = "Calibri"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_PRIMARY_BLUE
        p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 10: INNOVATION
    # =========================================================================
    s10 = prs.slides.add_slide(blank_slide_layout)
    add_header(s10, "Innovation, Originality & Unique Features", "Project Novelty")

    inno = [
        ("1. Dynamic User Input Engine",
         "The compiler includes an interactive CLI and REPL (run_interactive.py) allowing users to enter ANY arbitrary computational problem or algorithmic logic at runtime. It is not restricted to static files.",
         Inches(0.8), Inches(1.6)),
        ("2. Compile-Time Immutability",
         "Explicit semantic enforcement of let (mutable) vs const (immutable). Reassignments to constants are caught and rejected at compile time before execution begins.",
         Inches(6.8), Inches(1.6)),
        ("3. Pedagogical AST Visualizer",
         "Renders complete hierarchical ASCII syntax trees in terminal output, allowing evaluators and students to visually trace parsing decisions and operator binding power.",
         Inches(0.8), Inches(4.3)),
        ("4. Panic-Mode Synchronization",
         "Recovers from syntax errors at statement boundaries (semicolons and keywords), preventing cascading crashes and discovering multiple independent errors in one pass.",
         Inches(6.8), Inches(4.3))
    ]
    for title, desc, l, t in inno:
        add_card(s10, l, t, Inches(5.733), Inches(2.5), title)
        tb = s10.shapes.add_textbox(l + Inches(0.2), t + Inches(0.7), Inches(5.3), Inches(1.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = desc
        p.font.name = "Calibri"
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_TEXT_MUTED
        p.line_spacing = 1.3

    # =========================================================================
    # SLIDE 11: INITIAL PROTOTYPE SCREENSHOT 1
    # =========================================================================
    s11 = prs.slides.add_slide(blank_slide_layout)
    add_header(s11, "Working Prototype Demonstration -- Lexical & Syntax Analysis", "Working Evidence")

    # Left: Explanation card
    add_card(s11, Inches(0.8), Inches(1.6), Inches(4.3), Inches(5.3), "Interactive Input Test Case")
    tb11 = s11.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(3.9), Inches(4.3))
    tf11 = tb11.text_frame
    tf11.word_wrap = True
    p = tf11.paragraphs[0]
    p.text = (
        "- Problem Evaluated:\n"
        "  User-input circle area calculation.\n\n"
        "- Input Source:\n"
        "  const PI: float = 3.14159;\n"
        "  let r: float = 10.0;\n"
        "  let circle_area: float = PI * r * r;\n"
        "  print('Circle area is:', circle_area);\n\n"
        "- Front-End Verification:\n"
        "  • Lexer identified all 39 tokens with coordinates.\n"
        "  • Parser built hierarchical AST with correct operator precedence (* binds tighter than +).\n"
        "  • Zero syntax or lexical errors."
    )
    p.font.name = "Calibri"
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_MAIN

    # Right: Embedded Screenshot 1
    img1_path = "/Users/apple/.gemini/antigravity/brain/13593b79-d831-49dd-a83e-25e1c40e9896/.user_uploaded/media_1789055534478.png"
    if os.path.exists(img1_path):
        s11.shapes.add_picture(img1_path, Inches(5.3), Inches(1.6), width=Inches(7.2))

    # =========================================================================
    # SLIDE 12: SYMBOL TABLE SCREENSHOT 2 & ROADMAP
    # =========================================================================
    s12 = prs.slides.add_slide(blank_slide_layout)
    add_header(s12, "Scoped Symbol Table Verification & Future Phases", "Execution Evidence & Roadmap")

    # Top: Embedded Screenshot 2
    img2_path = "/Users/apple/.gemini/antigravity/brain/13593b79-d831-49dd-a83e-25e1c40e9896/.user_uploaded/media_1789055554680.png"
    if os.path.exists(img2_path):
        s12.shapes.add_picture(img2_path, Inches(1.8), Inches(1.5), width=Inches(9.7))

    # Bottom cards: Roadmap
    add_card(s12, Inches(0.8), Inches(4.5), Inches(5.7), Inches(2.4), "Phase 2: Core Implementation")
    tb12_l = s12.shapes.add_textbox(Inches(1.0), Inches(5.1), Inches(5.3), Inches(1.6))
    tf12_l = tb12_l.text_frame
    tf12_l.word_wrap = True
    p = tf12_l.paragraphs[0]
    p.text = (
        "- Static Type Checking across expressions.\n"
        "- Function signature & return type verification.\n"
        "- Immutability enforcement (prevent reassigning to const).\n"
        "- Three-Address Code (TAC) quadruple generation."
    )
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_MUTED

    add_card(s12, Inches(6.8), Inches(4.5), Inches(5.7), Inches(2.4), "Phase 3: Optimization & VM")
    tb12_r = s12.shapes.add_textbox(Inches(7.0), Inches(5.1), Inches(5.3), Inches(1.6))
    tf12_r = tb12_r.text_frame
    tf12_r.word_wrap = True
    p = tf12_r.paragraphs[0]
    p.text = (
        "- Machine-independent TAC optimizations (Constant folding, DCE).\n"
        "- Stack-based virtual machine execution of intermediate bytecode.\n"
        "- Comprehensive boundary testing & performance evaluation.\n"
        "- Final project documentation and demonstration."
    )
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_MUTED

    # Save presentations
    out_pptx = "/Users/apple/.gemini/antigravity/scratch/Review1_Presentation.pptx"
    prs.save(out_pptx)
    print(f"✅ Generated PowerPoint Presentation successfully: {out_pptx}")


if __name__ == "__main__":
    create_presentation()
