#!/usr/bin/env python3
"""
Comprehensive 10+ Page Academic Project Report Generator for Phase 1.
Generates Phase1_Report_Complete.pdf strictly fulfilling Section 8.3 deliverables:
• Project Title
• Abstract
• Problem Statement
• Motivation
• Objectives
• Scope
• Background Study
• Compiler Design Concepts Involved
• Proposed Methodology
• System Architecture
• Technology Stack
• Initial Prototype (with screenshot/figure frames)
"""

import os
import sys

class AcademicPDF:
    def __init__(self, filename="Phase1_Report_Complete.pdf", page_width=595, page_height=842):
        self.filename = filename
        self.w = page_width
        self.h = page_height
        self.margin_x = 54
        self.margin_top = 54
        self.margin_bottom = 54
        self.printable_width = self.w - 2 * self.margin_x
        
        self.pages = []
        self.current_stream = []
        self.cursor_y = self.h - self.margin_top
        self.current_page_num = 1

    def new_page(self):
        self.pages.append("\n".join(self.current_stream))
        self.current_stream = []
        self.cursor_y = self.h - self.margin_top
        self.current_page_num += 1

    def check_space(self, needed_pt):
        if self.cursor_y - needed_pt < self.margin_bottom:
            self.new_page()

    def add_page_header(self, title_text="COMPILER DESIGN LABORATORY PROJECT — PHASE 1 REPORT"):
        self.current_stream.append(
            f"BT /F2 8 Tf 0.45 0.5 0.6 rg {self.margin_x} {self.h - 32} Td ({self._escape(title_text)}) Tj ET"
        )
        self.current_stream.append(
            f"0.85 0.88 0.92 RG 0.8 w {self.margin_x} {self.h - 36} m {self.w - self.margin_x} {self.h - 36} l S"
        )

    def add_title(self, text):
        self.check_space(50)
        escaped = self._escape(text)
        self.current_stream.append(
            f"BT /F2 20 Tf 0.1 0.22 0.45 rg {self.margin_x} {self.cursor_y} Td ({escaped}) Tj ET"
        )
        self.cursor_y -= 28

    def add_subtitle(self, text):
        self.check_space(35)
        escaped = self._escape(text)
        self.current_stream.append(
            f"BT /F1 11 Tf 0.25 0.35 0.55 rg {self.margin_x} {self.cursor_y} Td ({escaped}) Tj ET"
        )
        self.cursor_y -= 20

    def add_heading1(self, text):
        self.check_space(45)
        self.cursor_y -= 8
        escaped = self._escape(text)
        self.current_stream.append(
            f"BT /F2 13 Tf 0.12 0.25 0.5 rg {self.margin_x} {self.cursor_y} Td ({escaped}) Tj ET"
        )
        self.current_stream.append(
            f"0.8 0.85 0.92 RG 1.5 w {self.margin_x} {self.cursor_y - 4} m {self.w - self.margin_x} {self.cursor_y - 4} l S"
        )
        self.cursor_y -= 20

    def add_heading2(self, text):
        self.check_space(32)
        self.cursor_y -= 4
        escaped = self._escape(text)
        self.current_stream.append(
            f"BT /F2 10.5 Tf 0.15 0.32 0.6 rg {self.margin_x} {self.cursor_y} Td ({escaped}) Tj ET"
        )
        self.cursor_y -= 16

    def add_paragraph(self, text, font="/F1", size=9.5, leading=13.5, color="0.15 0.15 0.18"):
        words = text.split()
        if not words:
            self.cursor_y -= leading
            return

        lines = []
        curr = []
        max_chars = 88 if font == "/F1" else 76

        for w in words:
            test_line = " ".join(curr + [w])
            if len(test_line) > max_chars:
                lines.append(" ".join(curr))
                curr = [w]
            else:
                curr.append(w)
        if curr:
            lines.append(" ".join(curr))

        for line in lines:
            self.check_space(leading)
            escaped = self._escape(line)
            self.current_stream.append(
                f"BT {font} {size} Tf {color} rg {self.margin_x} {self.cursor_y} Td ({escaped}) Tj ET"
            )
            self.cursor_y -= leading
        self.cursor_y -= 4

    def add_bullet(self, title, text=""):
        full_text = f"{title}: {text}" if text else title
        words = full_text.split()
        max_chars = 84
        lines = []
        curr = []
        for w in words:
            test_line = " ".join(curr + [w])
            if len(test_line) > max_chars:
                lines.append(" ".join(curr))
                curr = [w]
            else:
                curr.append(w)
        if curr:
            lines.append(" ".join(curr))

        leading = 13.5
        for i, line in enumerate(lines):
            self.check_space(leading)
            escaped = self._escape(line)
            prefix = "\\2022  " if i == 0 else "    "
            self.current_stream.append(
                f"BT /F1 9.5 Tf 0.18 0.18 0.2 rg {self.margin_x + 8} {self.cursor_y} Td ({prefix}{escaped}) Tj ET"
            )
            self.cursor_y -= leading
        self.cursor_y -= 3

    def add_callout(self, title, text, height=55):
        self.check_space(height + 15)
        # Background box
        self.current_stream.append(
            f"0.94 0.97 1.0 rg {self.margin_x} {self.cursor_y - height + 10} {self.printable_width} {height} re f"
        )
        # Left blue bar
        self.current_stream.append(
            f"0.18 0.42 0.72 rg {self.margin_x} {self.cursor_y - height + 10} 4 {height} re f"
        )
        # Border
        self.current_stream.append(
            f"0.82 0.88 0.95 RG 0.8 w {self.margin_x} {self.cursor_y - height + 10} {self.printable_width} {height} re S"
        )
        
        self.current_stream.append(
            f"BT /F2 9.5 Tf 0.12 0.28 0.55 rg {self.margin_x + 12} {self.cursor_y - 2} Td ({self._escape(title)}) Tj ET"
        )
        self.cursor_y -= 15
        
        words = text.split()
        lines = []
        curr = []
        for w in words:
            test = " ".join(curr + [w])
            if len(test) > 80:
                lines.append(" ".join(curr))
                curr = [w]
            else:
                curr.append(w)
        if curr:
            lines.append(" ".join(curr))

        for l in lines:
            self.current_stream.append(
                f"BT /F1 9 Tf 0.2 0.25 0.3 rg {self.margin_x + 12} {self.cursor_y} Td ({self._escape(l)}) Tj ET"
            )
            self.cursor_y -= 12
        self.cursor_y -= 15

    def add_table_row(self, col1, col2, col3, is_header=False, col_widths=(120, 110, 257)):
        self.check_space(18)
        font = "/F2" if is_header else "/F1"
        color = "0.1 0.22 0.45" if is_header else "0.2 0.2 0.22"
        size = 8.5
        
        if is_header:
            self.current_stream.append(
                f"0.88 0.92 0.97 rg {self.margin_x} {self.cursor_y - 4} {self.printable_width} 16 re f"
            )
        else:
            self.current_stream.append(
                f"0.9 0.92 0.95 RG 0.5 w {self.margin_x} {self.cursor_y - 4} m {self.w - self.margin_x} {self.cursor_y - 4} l S"
            )
        
        c1_esc = self._escape(col1)
        c2_esc = self._escape(col2)
        c3_esc = self._escape(col3)

        x1 = self.margin_x + 6
        x2 = x1 + col_widths[0]
        x3 = x2 + col_widths[1]

        self.current_stream.append(f"BT {font} {size} Tf {color} rg {x1} {self.cursor_y} Td ({c1_esc}) Tj ET")
        self.current_stream.append(f"BT {font} {size} Tf {color} rg {x2} {self.cursor_y} Td ({c2_esc}) Tj ET")
        self.current_stream.append(f"BT {font} {size} Tf {color} rg {x3} {self.cursor_y} Td ({c3_esc}) Tj ET")
        self.cursor_y -= 15

    def add_screenshot_frame(self, fig_title, description, height=130):
        self.check_space(height + 35)
        # Background canvas frame
        self.current_stream.append(
            f"0.97 0.98 0.99 rg {self.margin_x} {self.cursor_y - height} {self.printable_width} {height} re f"
        )
        # Dashed border
        self.current_stream.append(
            f"0.75 0.8 0.88 RG [3 3] 0 d 1 w {self.margin_x} {self.cursor_y - height} {self.printable_width} {height} re S [] 0 d"
        )
        
        # Center watermark text inside the frame
        watermark = "[ SCREENSHOT / TERMINAL EXECUTION EVIDENCE PLACEHOLDER ]"
        self.current_stream.append(
            f"BT /F2 9.5 Tf 0.5 0.55 0.65 rg {self.margin_x + 65} {self.cursor_y - height/2} Td ({watermark}) Tj ET"
        )
        self.current_stream.append(
            f"BT /F1 8.5 Tf 0.6 0.65 0.7 rg {self.margin_x + 95} {self.cursor_y - height/2 - 14} Td (Captured from Zenith Compiler CLI Execution Output) Tj ET"
        )

        self.cursor_y -= (height + 14)
        # Figure caption
        self.current_stream.append(
            f"BT /F2 9 Tf 0.15 0.25 0.45 rg {self.margin_x} {self.cursor_y} Td ({self._escape(fig_title)}) Tj ET"
        )
        self.cursor_y -= 12
        self.current_stream.append(
            f"BT /F1 8.5 Tf 0.35 0.4 0.45 rg {self.margin_x} {self.cursor_y} Td ({self._escape(description)}) Tj ET"
        )
        self.cursor_y -= 16

    def _escape(self, text):
        clean = (text
                 .replace("—", "--")
                 .replace("–", "-")
                 .replace("’", "'")
                 .replace("‘", "'")
                 .replace("“", '"')
                 .replace("”", '"')
                 .replace("│", "|")
                 .replace("▼", "v")
                 .replace("►", ">")
                 .replace("•", "*")
                 .replace("Sigma", "Sigma")
                 .replace("\\", "\\\\")
                 .replace("(", "\\(")
                 .replace(")", "\\)"))
        return clean.encode("latin-1", errors="replace").decode("latin-1")

    def save(self):
        if self.current_stream:
            self.pages.append("\n".join(self.current_stream))

        num_pages = len(self.pages)
        objects = []

        def add_obj(content):
            objects.append(content)
            return len(objects)

        obj_catalog = add_obj("<< /Type /Catalog /Pages 2 0 R >>")
        obj_pages = add_obj("")
        obj_f1 = add_obj("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
        obj_f2 = add_obj("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
        obj_f3 = add_obj("<< /Type /Font /Subtype /Type1 /BaseFont /Courier /Encoding /WinAnsiEncoding >>")

        page_ids = []
        for i, pstream in enumerate(self.pages):
            # No header/footer on page 1 (cover)
            if i == 0:
                content_data = pstream
            else:
                footer = f"BT /F1 8 Tf 0.45 0.5 0.55 rg {self.w / 2 - 40} 25 Td (Page {i + 1} of {num_pages}) Tj ET\n"
                footer += f"BT /F1 8 Tf 0.45 0.5 0.55 rg {self.margin_x} 25 Td (Compiler Design Laboratory) Tj ET\n"
                footer += f"BT /F1 8 Tf 0.45 0.5 0.55 rg {self.w - self.margin_x - 120} 25 Td (Phase 1 Deliverables) Tj ET\n"
                content_data = pstream + "\n" + footer

            c_bytes = content_data.encode("latin-1", errors="replace")
            c_len = len(c_bytes)
            
            c_id = add_obj(f"<< /Length {c_len} >>\nstream\n{content_data}\nendstream")
            p_id = add_obj(
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {self.w} {self.h}] "
                f"/Contents {c_id} 0 R /Resources << /Font << /F1 3 0 R /F2 4 0 R /F3 5 0 R >> >> >>"
            )
            page_ids.append(f"{p_id} 0 R")

        kids_str = " ".join(page_ids)
        objects[1] = f"<< /Type /Pages /Kids [{kids_str}] /Count {len(page_ids)} >>"

        out = ["%PDF-1.4\n"]
        xref = [0]
        offset = len(out[0].encode("latin-1"))

        for i, obj in enumerate(objects):
            xref.append(offset)
            block = f"{i + 1} 0 obj\n{obj}\nendobj\n"
            out.append(block)
            offset += len(block.encode("latin-1"))

        xref_offset = offset
        out.append(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n")
        for x in xref[1:]:
            out.append(f"{x:010d} 00000 n \n")

        out.append(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n")

        with open(self.filename, "wb") as f:
            f.write("".join(out).encode("latin-1", errors="replace"))
        print(f"✅ Generated 10+ Page PDF successfully: {self.filename} ({num_pages} pages)")


def build_ten_page_report():
    target_path = "/Users/apple/.gemini/antigravity/scratch/Phase1_Report.pdf"
    pdf = AcademicPDF(filename=target_path)

    # =========================================================================
    # PAGE 1: FORMAL TITLE & COVER PAGE
    # =========================================================================
    pdf.cursor_y = pdf.h - 100
    pdf.add_title("COMPILER DESIGN LABORATORY")
    pdf.add_subtitle("PROJECT INSTRUCTION MANUAL — PHASE 1 SUBMISSION")
    pdf.cursor_y -= 30

    pdf.add_heading1("ZENITH COMPILER")
    pdf.add_subtitle("A Strongly-Typed Procedural Language Compiler with AST Visualization,")
    pdf.add_subtitle("Scoped Symbol Table Management, and Intermediate Code Generation")
    pdf.cursor_y -= 40

    pdf.add_callout(
        "PHASE 1 DELIVERABLES SPECIFICATION (MANUAL SECTION 8.3)",
        "This submission strictly complies with Section 8.3 of the Compiler Design Laboratory Project Instruction Manual. "
        "It provides comprehensive academic documentation covering: Project Title, Abstract, Problem Statement, Motivation, "
        "Objectives, Scope, Background Study, Compiler Concepts, Proposed Methodology, System Architecture, Technology Stack, "
        "and Initial Prototype Verification Evidence.",
        height=75
    )

    pdf.cursor_y -= 50
    pdf.add_heading2("PROJECT METADATA & SUBMISSION DETAILS")
    pdf.add_bullet("Project Type", "Individual Project Submission (Strictly Independent)")
    pdf.add_bullet("Course", "Compiler Design Laboratory")
    pdf.add_bullet("Review Milestone", "Review 1: Project Proposal and System Design (20 Marks)")
    pdf.add_bullet("Implementation Phases", "Phase 1: Design & Prototype  |  Phase 2: Core  |  Phase 3: Final")
    pdf.add_bullet("Deliverable Repository", "/zenith-compiler (Source, Tests, Documentation)")
    
    # =========================================================================
    # PAGE 2: TABLE OF CONTENTS & EXECUTIVE ABSTRACT
    # =========================================================================
    pdf.new_page()
    pdf.add_page_header()
    pdf.add_heading1("TABLE OF CONTENTS")
    pdf.cursor_y -= 5
    
    toc_items = [
        ("Section 1", "Executive Abstract & Keywords", "Page 2"),
        ("Section 2", "Project Title, Motivation & Problem Statement", "Page 3"),
        ("Section 3", "Project Objectives & Scope Boundaries", "Page 4"),
        ("Section 4", "Background Study & Literature Survey", "Page 5"),
        ("Section 5", "Compiler Design Concepts Involved", "Page 6"),
        ("Section 6", "Proposed Methodology & Lifecycle Model", "Page 7"),
        ("Section 7", "System Architecture & Component Interaction", "Page 8"),
        ("Section 8", "Technology Stack & Language Specification", "Page 9"),
        ("Section 9", "Initial Prototype Verification & Screenshots", "Page 10"),
        ("Section 10", "Future Phases Roadmap & Academic References", "Page 11"),
    ]
    for sec, desc, pg in toc_items:
        pdf.add_table_row(sec, desc, pg, col_widths=(70, 340, 77))

    pdf.cursor_y -= 20
    pdf.add_heading1("1. EXECUTIVE ABSTRACT")
    pdf.add_paragraph(
        "This project presents the formal design, architectural specification, and initial implementation of Zenith, "
        "a strongly-typed procedural programming language and its accompanying multi-pass compiler. In contemporary software "
        "systems, developers are forced to choose between dynamically typed scripting environments (which defer type validation "
        "to runtime, causing unhandled production failures) and complex industrial compilers (which act as opaque black boxes, "
        "obscuring internal syntax trees and intermediate representation lowering). The Zenith compiler project bridges this gap "
        "by implementing a transparent, fully verifiable compiler pipeline designed from theoretical foundations."
    )
    pdf.add_paragraph(
        "The project encompasses the canonical phases of language translation: deterministic lexical scanning with coordinate tracking, "
        "LL(1) recursive descent parsing with operator precedence climbing, syntax-directed construction of an Abstract Syntax Tree (AST), "
        "hierarchical scoped symbol table management with parent-chain resolution, static type verification, machine-independent "
        "Three-Address Code (TAC) generation, and optimization passes."
    )
    pdf.add_paragraph(
        "In strict adherence to Phase 1 guidelines (Section 8.3), this report details the complete problem formulation, architectural "
        "pipeline, formal language specification, and experimental validation of the working Phase 1 prototype across four rigorous "
        "test suites. All front-end modules have been implemented and verified with zero external runtime dependencies."
    )
    pdf.cursor_y -= 8
    pdf.add_bullet("Keywords", "Compiler Design, Lexical Analysis, LL(1) Parsing, Recursive Descent, Abstract Syntax Tree, Scoped Symbol Table, Three-Address Code, Static Typing.")

    # =========================================================================
    # PAGE 3: TITLE, MOTIVATION & PROBLEM STATEMENT
    # =========================================================================
    pdf.new_page()
    pdf.add_page_header()
    pdf.add_heading1("2. PROJECT TITLE, MOTIVATION & PROBLEM STATEMENT")
    
    pdf.add_heading2("2.1 Project Title")
    pdf.add_paragraph(
        "Full Formal Title: Zenith: A Strongly-Typed Procedural Language Compiler with AST Visualization, Scoped Symbol Table Management, and Intermediate Three-Address Code Generation."
    )
    pdf.add_paragraph(
        "Short Title for Registration: Design and Implementation of the Zenith Language Compiler."
    )

    pdf.add_heading2("2.2 Motivation")
    pdf.add_paragraph(
        "The motivation for constructing the Zenith compiler arises from three distinct pedagogical and architectural challenges in modern computer science:"
    )
    pdf.add_bullet("1. Runtime Fragility in Scripting Languages", "Popular dynamic languages like Python and JavaScript allow rapid prototyping but postpone syntax and type errors until execution time. In mission-critical environments, compile-time static type enforcement and immutability guarantees are essential.")
    pdf.add_bullet("2. Opacity of Production Toolchains", "Industrial compilers such as GCC and Clang/LLVM are composed of millions of lines of code. Their internal intermediate representations (GIMPLE, LLVM IR) and complex graph-coloring register allocators make it exceedingly difficult to inspect how high-level language constructs are lowered into machine representations.")
    pdf.add_bullet("3. Pedagogical Application of Theory", "Theoretical compiler concepts taught in lecture courses—such as deterministic finite automata, LL(1) parse tables, context-free grammars, and symbol table environment trees—are best mastered through hands-on end-to-end software development.")

    pdf.add_heading2("2.3 Formal Problem Statement")
    pdf.add_paragraph(
        "To formulate, design, implement, and rigorously validate a modular, multi-pass compiler for a strongly-typed procedural language named Zenith, satisfying the following core requirements:"
    )
    pdf.add_bullet("Scanning Requirement", "Transform continuous source text into a discrete stream of strongly-typed tokens while maintaining exact line and column coordinate metadata for robust diagnostics.")
    pdf.add_bullet("Parsing Requirement", "Parse the token stream using a deterministic LL(1) recursive descent parser adhering to an unambiguous context-free grammar with operator precedence climbing.")
    pdf.add_bullet("Syntax-Directed Translation", "Construct an explicit, strongly-typed Abstract Syntax Tree (AST) that eliminates syntactic punctuation while preserving semantic structure.")
    pdf.add_bullet("Scope Management Requirement", "Manage nested lexical environments through a hierarchical scoped symbol table, enforcing variable declaration rules and immutability constraints.")
    pdf.add_bullet("Intermediate Code & Execution", "Establish a clear architectural interface to translate the AST into linearized Three-Address Code (TAC) and execute instructions via a virtual machine in subsequent phases.")

    # =========================================================================
    # PAGE 4: OBJECTIVES AND SCOPE
    # =========================================================================
    pdf.new_page()
    pdf.add_page_header()
    pdf.add_heading1("3. PROJECT OBJECTIVES AND SCOPE BOUNDARIES")

    pdf.add_heading2("3.1 Primary Project Objectives")
    pdf.add_bullet("1. Grammar Specification", "Design an unambiguous, left-recursion-free Context-Free Grammar in Extended Backus-Naur Form (EBNF) supporting procedural programming constructs.")
    pdf.add_bullet("2. Hand-Crafted Scanner", "Develop a high-performance lexical analyzer recognizing keywords, identifiers, numeric literals, strings, comments, and compound operators with coordinate tracking.")
    pdf.add_bullet("3. Recursive Descent Parser", "Implement a top-down parser with operator precedence climbing, panic-mode error recovery, and synchronization at statement boundaries.")
    pdf.add_bullet("4. AST Construction", "Formulate an object-oriented Abstract Syntax Tree hierarchy with visual ASCII tree formatting for verification.")
    pdf.add_bullet("5. Scoped Symbol Table", "Implement an environment tree data structure supporting parent-pointer chaining, local vs. enclosing scope lookups, and duplicate declaration prevention.")
    pdf.add_bullet("6. CLI & REPL Environment", "Deliver an interactive command-line interface and Read-Eval-Print Loop allowing real-time token, AST, and symbol table inspection.")

    pdf.add_heading2("3.2 Scope of the Project")
    pdf.add_paragraph(
        "To ensure high engineering depth and complete feasibility within the semester timeline, the project boundaries are defined as follows:"
    )
    pdf.add_callout(
        "IN-SCOPE FUNCTIONALITY",
        "• Primitive Data Types: int, float, bool, string, and void.\n"
        "• Variable Bindings: Mutable ('let') and immutable ('const') variable declarations.\n"
        "• Comprehensive Operators: Arithmetic (+, -, *, /, %), Relational (==, !=, <, <=, >, >=), Logical (&&, ||, !).\n"
        "• Structured Control Flow: Multi-way branching (if-elif-else), while loops, and initialized for loops.\n"
        "• Functional Abstractions: Function declarations with typed formal parameters and explicit return types.\n"
        "• Intermediate Representation: Linearized Three-Address Code (TAC) quadruples with temporary variables.\n"
        "• Code Optimization: Machine-independent constant folding, algebraic simplification, and dead code elimination.\n"
        "• Target Execution: Stack-based virtual machine execution of intermediate bytecode instructions.",
        height=110
    )

    pdf.cursor_y -= 15
    pdf.add_callout(
        "OUT-OF-SCOPE BOUNDARIES (DESIGN NON-GOALS)",
        "• Dynamic Heap Garbage Collection: Memory allocation follows structured lexical activation records; complex mark-and-sweep or generational garbage collectors are excluded.\n"
        "• Complex Object-Oriented Polymorphism: Virtual method tables and multi-inheritance hierarchies are excluded to prioritize procedural compiler pipeline clarity.\n"
        "• Native Hardware Assembly Emission: Direct generation of x86-64 or ARM machine code is replaced with Three-Address Code and virtual machine bytecode to avoid platform-dependent ABI calling conventions.",
        height=80
    )

    # =========================================================================
    # PAGE 5: BACKGROUND STUDY & LITERATURE SURVEY
    # =========================================================================
    pdf.new_page()
    pdf.add_page_header()
    pdf.add_heading1("4. BACKGROUND STUDY & LITERATURE SURVEY")

    pdf.add_heading2("4.1 Theoretical Foundations of Language Processing")
    pdf.add_paragraph(
        "Compiler construction represents one of the most mature subfields of computer science. As detailed in canonical texts such as "
        "Compilers: Principles, Techniques, and Tools (Aho, Lam, Sethi, and Ullman), a compiler translates a source program into an equivalent "
        "target language representation through a sequence of discrete analytical and synthetic phases."
    )

    pdf.add_heading2("4.2 Lexical Analysis & Finite Automata")
    pdf.add_paragraph(
        "Lexical analysis (scanning) transforms an unstructured stream of characters into a stream of categorized tokens. Formally, tokens "
        "are specified via Regular Expressions (RE). By Thompson's Construction, regular expressions correspond to Non-deterministic "
        "Finite Automata (NFA), which can be converted via subset construction into Deterministic Finite Automata (DFA). While tools like "
        "Lex and Flex automatically generate DFA tables, a hand-crafted scanner provides greater flexibility for coordinate tracking (line and column), "
        "custom lookahead buffers, and fine-grained error messages."
    )

    pdf.add_heading2("4.3 Parsing Techniques: Top-Down vs. Bottom-Up")
    pdf.add_paragraph(
        "Syntax analysis verifies whether the token sequence belongs to the formal language defined by a Context-Free Grammar (CFG). "
        "Two dominant parsing paradigms exist in the literature:"
    )
    pdf.add_bullet("Bottom-Up Parsers (LR, LALR, SLR)", "Employed by tools like Yacc and Bison. They operate by shifting tokens onto a stack and reducing them according to grammar productions. While capable of parsing large grammar classes, LALR parsers suffer from obscure shift-reduce conflicts and difficult-to-customize error recovery.")
    pdf.add_bullet("Top-Down Parsers (LL(k), Recursive Descent)", "Construct the parse tree from the root down to the leaves. Hand-written recursive descent parsers directly mirror grammar productions in programming language functions. When combined with operator precedence climbing, recursive descent parsers achieve optimal diagnostic clarity, zero build dependencies, and intuitive debuggability.")

    pdf.add_heading2("4.4 Abstract Syntax Trees (AST) vs. Concrete Parse Trees")
    pdf.add_paragraph(
        "A Concrete Parse Tree (CST) represents the exact syntactic derivation of a string, retaining all punctuation tokens (parentheses, commas, "
        "semicolons) and intermediate non-terminal expansions. In contrast, an Abstract Syntax Tree (AST) condenses the parse tree into an "
        "operator-operand hierarchy, discarding syntactic noise while preserving semantic relationships. ASTs serve as the primary intermediate "
        "data structure for semantic analysis and code generation."
    )

    pdf.add_heading2("4.5 Intermediate Representations (IR)")
    pdf.add_paragraph(
        "Decoupling the compiler front-end from the back-end is achieved through Intermediate Representations. Three-Address Code (TAC) is a "
        "linearized representation where each instruction has at most one operator and at most three operand addresses (result = arg1 op arg2). "
        "TAC linearizes complex nested expression trees into sequential instructions, forming the basis for basic block partitioning, control-flow "
        "graph (CFG) analysis, and data-flow optimizations."
    )

    # =========================================================================
    # PAGE 6: COMPILER DESIGN CONCEPTS INVOLVED
    # =========================================================================
    pdf.new_page()
    pdf.add_page_header()
    pdf.add_heading1("5. COMPILER DESIGN CONCEPTS INVOLVED")

    pdf.add_paragraph(
        "The Zenith compiler project directly implements and validates key theoretical concepts from the Compiler Design curriculum:"
    )

    pdf.add_heading2("5.1 Regular Expressions & DFA Tokenization")
    pdf.add_paragraph(
        "The Lexical Analyzer categorizes 34 distinct token types using regular expression matching. It tracks line and column coordinates, "
        "handles escape sequences in string literals, filters single-line (//) and multi-line (/* */) comments, and uses lookahead matching "
        "to resolve multi-character operator ambiguities (such as = vs ==, < vs <=, and - vs ->)."
    )

    pdf.add_heading2("5.2 Context-Free Grammars & EBNF Specification")
    pdf.add_paragraph(
        "The language syntax is governed by a formal 4-tuple G = (V, Sigma, R, S), where V is the set of non-terminals, Sigma is the alphabet "
        "of terminal tokens, R is the set of production rules, and S is the start symbol (program). The grammar is structured in Extended "
        "Backus-Naur Form (EBNF) and formulated to eliminate left recursion and common prefix ambiguity."
    )

    pdf.add_heading2("5.3 Operator Precedence Climbing")
    pdf.add_paragraph(
        "To resolve mathematical ambiguities without cumbersome grammar transformations, the parser implements operator precedence climbing. "
        "Expressions are parsed through seven distinct priority tiers, ensuring that higher-precedence operators (multiplication, division) "
        "bind more tightly than lower-precedence operators (addition, relational comparisons, and logical operators)."
    )

    pdf.add_heading2("5.4 Hierarchical Scoped Symbol Tables")
    pdf.add_paragraph(
        "Lexical scoping is modeled as a tree of environment tables linked via parent pointers. Each scope records local symbol declarations "
        "with attributes including identifier name, data type, category (variable, constant, function), declaration line, and scope level. "
        "The symbol table detects invalid duplicate declarations in O(1) time and resolves identifier references hierarchically from the current "
        "scope up to the global scope."
    )

    pdf.add_heading2("5.5 Panic-Mode Error Recovery & Synchronization")
    pdf.add_paragraph(
        "Rather than terminating on the first syntax fault, the parser employs panic-mode error recovery. Upon detecting a malformed construct, "
        "the parser records a coordinate-annotated error message and discards tokens until a synchronizing statement boundary (semicolon or "
        "keywords such as 'let', 'if', 'while', 'fn') is reached, enabling the detection of multiple independent syntax errors in a single pass."
    )

    # =========================================================================
    # PAGE 7: PROPOSED METHODOLOGY
    # =========================================================================
    pdf.new_page()
    pdf.add_page_header()
    pdf.add_heading1("6. PROPOSED METHODOLOGY & DEVELOPMENT LIFECYCLE")

    pdf.add_heading2("6.1 Multi-Pass Compiler Engineering Lifecycle")
    pdf.add_paragraph(
        "The project adopts an iterative, multi-pass engineering methodology where each compiler stage produces a fully verified intermediate "
        "artifact before downstream translation begins:"
    )
    pdf.add_bullet("Stage 1: Lexical Specification", "Formal definition of token patterns, keywords, operators, and coordinate tracking mechanisms.")
    pdf.add_bullet("Stage 2: Grammar Engineering", "Formulation of unambiguous EBNF grammar rules and operator precedence hierarchy.")
    pdf.add_bullet("Stage 3: Front-End Construction", "Implementation of hand-crafted Lexer, Recursive Descent Parser, and AST node hierarchy.")
    pdf.add_bullet("Stage 4: Scope & Symbol Management", "Implementation of the hierarchical environment tree and scope resolution builder.")
    pdf.add_bullet("Stage 5: Test-Driven Verification", "Validation against dedicated test suites covering expressions, control flow, functions, and error recovery.")

    pdf.add_heading2("6.2 Phase-wise Implementation Breakdown")
    pdf.add_table_row("Implementation Phase", "Core Functional Modules", "Review Target & Weight", is_header=True)
    pdf.add_table_row("Phase 1 (Completed)", "Grammar, Lexer, Parser, AST Visualizer, Symbol Table", "Review 1: Problem Definition & Design (20 Marks)")
    pdf.add_table_row("Phase 2 (Upcoming)", "Type Checker, Semantic Rules, Three-Address Code (TAC)", "Review 2: Core Implementation (25 Marks)")
    pdf.add_table_row("Phase 3 (Upcoming)", "Constant Folding Optimizer, Virtual Machine Runtime", "Review 3: Final System & Testing (35 Marks)")

    pdf.cursor_y -= 10
    pdf.add_heading2("6.3 Verification & Quality Assurance Strategy")
    pdf.add_paragraph(
        "The verification strategy follows a test-driven approach utilizing four dedicated test programs designed to exercise every language feature:"
    )
    pdf.add_bullet("Basic Math Suite", "Validates integer/float literals, operator precedence climbing, and boolean relational evaluations.")
    pdf.add_bullet("Control Flow Suite", "Validates branch parsing in multi-branch if-elif-else statements, while loop condition evaluation, and for loop variable initialization.")
    pdf.add_bullet("Functions Suite", "Validates function declaration parsing, typed parameter lists, return statements, and local scope creation.")
    pdf.add_bullet("Error Recovery Suite", "Validates panic-mode recovery, unterminated literals, missing semicolons, and exact coordinate reporting.")

    # =========================================================================
    # PAGE 8: SYSTEM ARCHITECTURE
    # =========================================================================
    pdf.new_page()
    pdf.add_page_header()
    pdf.add_heading1("7. SYSTEM ARCHITECTURE & COMPONENT DESIGN")

    pdf.add_heading2("7.1 End-to-End Architectural Pipeline")
    pdf.add_paragraph(
        "The Zenith compiler is organized into a modular, multi-pass pipeline where each component operates on well-defined data structures:"
    )
    pdf.add_callout(
        "ZENITH COMPILER ARCHITECTURAL DATA FLOW",
        "Source Code (.zen) ---> [Lexical Analyzer (lexer.py)] ---> Token Stream\n"
        "                              │\n"
        "                              ▼\n"
        "Token Stream ---------> [Recursive Descent Parser (parser.py)] ---> Abstract Syntax Tree (AST)\n"
        "                              │\n"
        "                              ▼\n"
        "Abstract Syntax Tree -> [Symbol Table Builder (symbol_table.py)] ---> Scoped Environment Tree\n"
        "                              │\n"
        "                              ▼\n"
        "AST & Symbol Table ---> [Terminal Visualizer & CLI (printer.py / main.py)] ---> Human-Inspectable Output",
        height=90
    )

    pdf.cursor_y -= 10
    pdf.add_heading2("7.2 Component Role Descriptions")
    pdf.add_bullet("Lexical Analyzer (src/lexer.py)", "Scans character buffers, identifies lexemes, checks keyword dictionaries, tracks line:column coordinates, and logs lexical errors.")
    pdf.add_bullet("Token Definitions (src/tokens.py)", "Defines the TokenType enumeration (34 distinct token categories) and the immutable Token dataclass.")
    pdf.add_bullet("AST Node Hierarchy (src/ast_nodes.py)", "Object-oriented dataclass hierarchy representing statements (VarDecl, IfStmt, WhileStmt, FnDecl) and expressions (BinaryExpr, LiteralExpr, CallExpr).")
    pdf.add_bullet("Recursive Descent Parser (src/parser.py)", "Enforces EBNF grammar productions, executes precedence climbing, handles lookahead, and implements panic-mode recovery.")
    pdf.add_bullet("Scoped Symbol Table (src/symbol_table.py)", "Manages hierarchical lexical scopes (global, function, block), validates identifier declarations, and enforces immutability.")
    pdf.add_bullet("AST Visualizer & Printer (src/printer.py)", "Renders ASCII tree representations of the AST and tabular summaries of tokens and symbol tables.")
    pdf.add_bullet("CLI Driver & REPL (src/main.py)", "Provides the command-line interface, argument flags (--tokens, --ast, --symtab, --all), and an interactive shell.")

    # =========================================================================
    # PAGE 9: TECHNOLOGY STACK & LANGUAGE SPECIFICATION
    # =========================================================================
    pdf.new_page()
    pdf.add_page_header()
    pdf.add_heading1("8. TECHNOLOGY STACK & LANGUAGE SPECIFICATION")

    pdf.add_heading2("8.1 Technology Selection Justification")
    pdf.add_paragraph(
        "The compiler is implemented in modern Python 3 (standard library only). This technology choice provides significant advantages for laboratory evaluation:"
    )
    pdf.add_bullet("Zero External Toolchain Dependencies", "Eliminates build and linking errors associated with C/C++ Flex/Bison configurations across different operating systems.")
    pdf.add_bullet("High Diagnostic Transparency", "Python's dataclasses, pattern matching, and recursion support clean, readable implementations of tree traversal algorithms.")
    pdf.add_bullet("Portability & Demonstration", "Executes out-of-the-box on macOS, Linux, and Windows without binary recompilation.")

    pdf.add_heading2("8.2 Formal Context-Free Grammar (EBNF Summary)")
    pdf.add_paragraph(
        "The Zenith grammar is structured in Extended Backus-Naur Form (EBNF) to guarantee deterministic LL(1) derivation:"
    )
    pdf.add_bullet("Program Level", "program ::= { statement }")
    pdf.add_bullet("Statement Level", "statement ::= var_decl | assignment | if_stmt | while_stmt | for_stmt | fn_decl | return_stmt | print_stmt | block")
    pdf.add_bullet("Variable Declarations", "var_decl ::= ('let' | 'const') IDENTIFIER ':' type ['=' expression] ';'")
    pdf.add_bullet("Conditionals", "if_stmt ::= 'if' '(' expression ')' block { 'elif' '(' expression ')' block } ['else' block]")
    pdf.add_bullet("Loops", "while_stmt ::= 'while' '(' expression ')' block  |  for_stmt ::= 'for' '(' [var_decl] [expression] ';' [assignment] ')' block")
    pdf.add_bullet("Functions", "fn_decl ::= 'fn' IDENTIFIER '(' [param_list] ')' ['->' type] block")

    pdf.add_heading2("8.3 Operator Precedence and Associativity Table")
    pdf.add_table_row("Precedence Level", "Operator Class", "Associativity & Binding Power", is_header=True)
    pdf.add_table_row("Level 1 (Lowest)", "Logical OR (||)", "Left-to-Right evaluation")
    pdf.add_table_row("Level 2", "Logical AND (&&)", "Left-to-Right evaluation")
    pdf.add_table_row("Level 3", "Equality (==, !=)", "Left-to-Right evaluation")
    pdf.add_table_row("Level 4", "Relational (<, <=, >, >=)", "Left-to-Right evaluation")
    pdf.add_table_row("Level 5", "Additive (+, -)", "Left-to-Right evaluation")
    pdf.add_table_row("Level 6", "Multiplicative (*, /, %)", "Left-to-Right evaluation")
    pdf.add_table_row("Level 7 (Highest)", "Unary (- , !)", "Right-to-Left prefix binding")

    # =========================================================================
    # PAGE 10: INITIAL PROTOTYPE VERIFICATION & SCREENSHOT EVIDENCE
    # =========================================================================
    pdf.new_page()
    pdf.add_page_header()
    pdf.add_heading1("9. INITIAL PROTOTYPE VERIFICATION & SCREENSHOTS")

    pdf.add_paragraph(
        "The Phase 1 prototype was verified across four test programs. The execution outputs demonstrate functional correctness across "
        "tokenization, AST tree construction, scoped symbol resolution, and panic-mode error diagnostics."
    )

    pdf.add_screenshot_frame(
        "Figure 1: Lexical Analysis & Token Classification Output",
        "Evidence showing tokens identified from tests/01_basic_math.zen with exact line, column, and literal values."
    )

    pdf.add_screenshot_frame(
        "Figure 2: Abstract Syntax Tree (AST) Hierarchical Tree Output",
        "Evidence showing recursive descent parsing and visual AST output for tests/02_control_flow.zen."
    )

    # =========================================================================
    # PAGE 11: SCOPE SCREENSHOT EVIDENCE, ROADMAP & REFERENCES
    # =========================================================================
    pdf.new_page()
    pdf.add_page_header()
    pdf.add_heading1("10. SYMBOL TABLE EVIDENCE, ROADMAP & REFERENCES")

    pdf.add_screenshot_frame(
        "Figure 3: Hierarchical Scoped Symbol Table Output",
        "Evidence showing parent-chained scopes (global vs. local function scopes) for tests/03_functions.zen."
    )

    pdf.add_heading2("10.1 Roadmap for Phase 2 and Phase 3")
    pdf.add_bullet("Phase 2 Target (Core Implementation)", "Implement semantic type checking, return type validation, immutability checking for const variables, and generation of linearized Three-Address Code (TAC) quadruples.")
    pdf.add_bullet("Phase 3 Target (Final Implementation)", "Implement machine-independent TAC optimizations (constant folding, dead code elimination) and construct a lightweight stack-based virtual machine runtime.")

    pdf.add_heading2("10.2 Academic References")
    pdf.add_bullet("1. Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006)", "Compilers: Principles, Techniques, and Tools (2nd Edition). Addison-Wesley.")
    pdf.add_bullet("2. Cooper, K. D., & Torczon, L. (2011)", "Engineering a Compiler (2nd Edition). Morgan Kaufmann.")
    pdf.add_bullet("3. Louden, K. C. (1997)", "Compiler Construction: Principles and Practice. PWS Publishing.")
    pdf.add_bullet("4. Grune, D., van Reeuwijk, K., Bal, H. E., Jacobs, C. J., & Langendoen, K. (2012)", "Modern Compiler Design. Springer.")

    pdf.save()


if __name__ == "__main__":
    build_ten_page_report()
