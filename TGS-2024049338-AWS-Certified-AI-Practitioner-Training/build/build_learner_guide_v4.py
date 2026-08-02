#!/usr/bin/env python3
"""Learner Guide v4.0 for TGS-2024049338 as a CKA-style LAB MANUAL.

Mirrors the CKA Learner Guide (a lab manual, not a concept guide):
  cover -> version control -> TOC -> Exam Domains table -> Before You Start
  -> all 25 labs rendered inline, grouped by DAY then DOMAIN, each lab with a
     bold metadata line (domain / duration / slide range) and its full lab.md body
  -> AWS Cheat-Sheet -> Glossary.

Every lab's prose, tables, steps and code come straight from labs/lab-NN/lab.md and
labs/tools.md. Nothing about AWS is invented here; slide ranges are read from lab.md.
"""
import json, os, re, sys
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_BREAK

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
LABS = os.path.join(REPO, "labs")
for cand in (os.path.join(REPO, ".claude/skills/tertiary-lesson-plan"),
             os.path.expanduser("~/.claude/skills/tertiary-lesson-plan")):
    if os.path.isdir(cand):
        sys.path.insert(0, cand); break
import prodoc
from prodoc import (add_cover_page, add_version_control, add_toc,
                    add_page_numbers, enable_update_fields, style_headings, _shade_cell)

TITLE   = "AWS Certified AI Practitioner Training (AIF-C01)"
CODE    = "TGS-2024049338"
VERSION = "4.0"
prodoc.TGS = f"TGS Ref No: {CODE}"
ORG_LOGO = next((x for x in (
    os.path.join(REPO, ".claude/skills/tertiary-lesson-plan/assets/tertiary-infotech-logo.png"),
    os.path.expanduser("~/.claude/skills/tertiary-lesson-plan/assets/tertiary-infotech-logo.png"),
) if os.path.isfile(x)), None)

DARK  = RGBColor(0x11, 0x18, 0x27)
BRAND = RGBColor(0x1F, 0x6F, 0xEB)
GREY  = RGBColor(0x55, 0x5B, 0x66)
CODEBG = "F2F4F7"
HDRBG  = "1F6FEB"
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)

VERSIONS = [
    ("1.0", "29 Sep 2024", "First version", "Tertiary Infotech Academy"),
    ("2.0", "17 Oct 2025", "Update company name", "Tertiary Infotech Academy"),
    ("3.0", "20 Jul 2026", "Realigned to AIF-C01 exam domains", "Tertiary Infotech Academy"),
    ("4.0", "21 Jul 2026",
     "Reformatted to the house lab-manual layout: all 25 labs inline, grouped by day and "
     "exam domain, with a Before-You-Start setup section, cheat-sheet and glossary",
     "Tertiary Infotech Academy"),
]

# domain number -> (name, weight, first lab, last lab)
DOMAINS = [
    (1, "Fundamentals of AI and ML", 20, 1, 5),
    (2, "Fundamentals of Generative AI", 24, 6, 11),
    (3, "Applications of Foundation Models", 28, 12, 18),
    (4, "Guidelines for Responsible AI", 14, 19, 22),
    (5, "Security, Compliance and Governance for AI Solutions", 14, 23, 25),
]
DOMNAME = {n: nm for n, nm, w, a, b in DOMAINS}
DOMWT   = {n: w for n, nm, w, a, b in DOMAINS}
def lab_domain(n):
    for num, nm, w, a, b in DOMAINS:
        if a <= n <= b:
            return num
    return None

# Day split matches Lesson Plan v5: Day 1 = domains 1&2 (labs 1-11); Day 2 = domains 3,4,5 (labs 12-25)
DAYS = [
    ("DAY 1 — Domains 1 & 2 (Labs 01-11)", [1, 2]),
    ("DAY 2 — Domains 3, 4 & 5 (Labs 12-25)", [3, 4, 5]),
]

# --------------------------------------------------------------- lab discovery
def lab_dirs():
    out = {}
    for d in sorted(os.listdir(LABS)):
        m = re.match(r'lab-(\d\d)-', d)
        if m and os.path.isdir(os.path.join(LABS, d)):
            out[int(m.group(1))] = d
    return out
DIRS = lab_dirs()

def load_lab(n):
    d = DIRS[n]
    j = json.load(open(os.path.join(LABS, d, "index.json"), encoding="utf-8"))
    body = open(os.path.join(LABS, d, "lab.md"), encoding="utf-8").read()
    sr = re.search(r'\*\*Slide reference:\*\*\s*(.+)', body)
    slides_raw = sr.group(1).strip() if sr else ""
    m = re.search(r'slides?\s*([\d]+\s*[–—-]\s*[\d]+)', slides_raw)
    slides = m.group(1).replace(" ", "") if m else slides_raw
    title = re.sub(r'^Lab\s*0?\d+\s*[—-]\s*', '', j["title"]).strip()
    return dict(dir=d, title=title, time=str(j.get("time", "")).strip(),
                slides=slides, body=body)

# ------------------------------------------------------------- markdown render
INLINE = re.compile(r'(\*\*.+?\*\*|`[^`]+`|\[[^\]]+\]\([^)]+\))')

def _plain(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    return text.strip()

def add_inline(p, text, size=11, color=DARK):
    for tok in INLINE.split(text):
        if not tok:
            continue
        if tok.startswith('**') and tok.endswith('**'):
            r = p.add_run(tok[2:-2]); r.bold = True; r.font.name = "Arial"; r.font.color.rgb = color
            r.font.size = Pt(size)
        elif tok.startswith('`') and tok.endswith('`'):
            r = p.add_run(tok[1:-1]); r.font.name = "Consolas"; r.font.size = Pt(size - 0.5)
            r.font.color.rgb = RGBColor(0xB3, 0x11, 0x2A)
        elif tok.startswith('[') and re.fullmatch(r'\[[^\]]+\]\([^)]+\)', tok):
            m = re.match(r'\[([^\]]+)\]\(([^)]+)\)', tok)
            txt, url = m.group(1), m.group(2)
            r = p.add_run(txt); r.font.name = "Arial"; r.font.size = Pt(size); r.underline = True
            r.font.color.rgb = BRAND
            if url.startswith("http") and url not in txt:
                r2 = p.add_run(f" ({url})"); r2.font.name = "Arial"; r2.font.size = Pt(size - 1.5)
                r2.font.color.rgb = GREY
        else:
            r = p.add_run(tok); r.font.name = "Arial"; r.font.size = Pt(size); r.font.color.rgb = color

def _heading(doc, text, level):
    lvl = min(max(level, 1), 9)
    h = doc.add_heading("", level=lvl)
    r = h.add_run(_plain(text)); r.font.name = "Arial"
    return h

def _table(doc, rows):
    header, body = rows[0], rows[1:]
    t = doc.add_table(rows=0, cols=len(header)); t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hr = t.add_row().cells
    for i, cell in enumerate(header):
        hr[i].text = ""; p = hr[i].paragraphs[0]
        add_inline(p, cell, size=9, color=WHITE)
        for run in p.runs:
            run.bold = True; run.font.color.rgb = WHITE; run.font.size = Pt(9)
        _shade_cell(hr[i], HDRBG)
    for row in body:
        cells = t.add_row().cells
        for i in range(len(header)):
            val = row[i] if i < len(row) else ""
            cells[i].text = ""
            add_inline(cells[i].paragraphs[0], val, size=8.5)
    doc.add_paragraph()

def _codeblock(doc, lines):
    t = doc.add_table(rows=1, cols=1); t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = t.rows[0].cells[0]; _shade_cell(cell, CODEBG); cell.text = ""
    for j, ln in enumerate(lines):
        p = cell.paragraphs[0] if j == 0 else cell.add_paragraph()
        p.paragraph_format.space_after = Pt(0); p.paragraph_format.space_before = Pt(0)
        r = p.add_run(ln if ln else " "); r.font.name = "Consolas"; r.font.size = Pt(9)
        r.font.color.rgb = DARK
    doc.add_paragraph()

def _para(doc, text, style=None, size=11):
    if style:
        p = doc.add_paragraph(style=style)
    else:
        p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    add_inline(p, text, size=size)
    return p

def _quote(doc, text):
    p = doc.add_paragraph(); p.paragraph_format.left_indent = Inches(0.3)
    p.paragraph_format.space_after = Pt(4)
    add_inline(p, text, size=10.5, color=GREY)
    for r in p.runs:
        r.italic = True

TABLE_ROW = re.compile(r'^\s*\|(.+)\|\s*$')
SEP_ROW   = re.compile(r'^\s*\|?[\s:|-]+\|?\s*$')
LIST_RE   = re.compile(r'^(\s*)([-*]|\d+\.)\s+(.*)$')

def render_markdown(doc, text, hshift, skip_h1=True):
    """Render markdown into the docx. md-H(n) -> docx Heading(n+hshift)."""
    # strip trailing copyright line
    text = re.sub(r'\nCopyright 2026.*?All rights reserved\.\s*$', '', text, flags=re.S)
    lines = text.split("\n")
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()

        # fenced code block
        if stripped.startswith("```"):
            j = i + 1; code = []
            while j < n and not lines[j].strip().startswith("```"):
                code.append(lines[j]); j += 1
            _codeblock(doc, code); i = j + 1; continue

        # blank
        if not stripped:
            i += 1; continue

        # horizontal rule
        if re.match(r'^\s*(-{3,}|\*{3,}|_{3,})\s*$', line):
            i += 1; continue

        # heading
        hm = re.match(r'^(#{1,6})\s+(.*)$', stripped)
        if hm:
            lvl = len(hm.group(1))
            if lvl == 1 and skip_h1:
                i += 1; continue
            _heading(doc, hm.group(2), lvl + hshift)
            i += 1; continue

        # table
        if TABLE_ROW.match(line) and i + 1 < n and SEP_ROW.match(lines[i + 1]) \
           and "|" in lines[i + 1]:
            block = []
            while i < n and TABLE_ROW.match(lines[i]):
                block.append(lines[i]); i += 1
            rows = []
            for bi, brow in enumerate(block):
                if bi == 1:  # separator
                    continue
                cells = [c.strip() for c in brow.strip().strip("|").split("|")]
                rows.append(cells)
            if rows:
                _table(doc, rows)
            continue

        # blockquote
        if stripped.startswith(">"):
            q = []
            while i < n and lines[i].strip().startswith(">"):
                q.append(re.sub(r'^\s*>\s?', '', lines[i])); i += 1
            _quote(doc, " ".join(x.strip() for x in q if x.strip()))
            continue

        # list
        lm = LIST_RE.match(line)
        if lm:
            while i < n:
                lm = LIST_RE.match(lines[i])
                if not lm:
                    # continuation (indented, non-blank, not a new block)
                    if lines[i].strip() and lines[i].startswith(" ") \
                       and not TABLE_ROW.match(lines[i]) \
                       and not re.match(r'^\s*#', lines[i]) \
                       and not lines[i].strip().startswith("```"):
                        i += 1; continue
                    break
                indent, marker, content = lm.group(1), lm.group(2), lm.group(3)
                ordered = bool(re.match(r'\d+\.', marker))
                lvl2 = len(indent) >= 2
                if ordered:
                    style = "List Number 2" if lvl2 else "List Number"
                else:
                    style = "List Bullet 2" if lvl2 else "List Bullet"
                try:
                    _para(doc, content, style=style, size=10.5)
                except KeyError:
                    _para(doc, content, style=("List Number" if ordered else "List Bullet"),
                          size=10.5)
                i += 1
            continue

        # paragraph: gather consecutive plain lines
        para = [stripped]; i += 1
        while i < n:
            s = lines[i].strip()
            if not s or re.match(r'^(#{1,6})\s', s) or s.startswith(">") \
               or s.startswith("```") or TABLE_ROW.match(lines[i]) \
               or LIST_RE.match(lines[i]) \
               or re.match(r'^\s*(-{3,}|\*{3,}|_{3,})\s*$', lines[i]):
                break
            para.append(s); i += 1
        # label-block heuristic: consecutive **Label:** lines -> one paragraph each
        if len(para) > 1 and all(re.match(r'^\*\*.+?:\*\*', ln) for ln in para):
            for ln in para:
                _para(doc, ln, size=10.5)
        else:
            _para(doc, " ".join(para), size=11)
    return

# ------------------------------------------------------------- fixed sections
def exam_domains_table(doc):
    rows = [["Domain", "Weight", "Labs"]]
    for num, nm, w, a, b in DOMAINS:
        rows.append([f"D{num} — {nm}", f"{w}%", f"Labs {a:02d}–{b:02d}"])
    _table(doc, rows)

CHEATSHEET = [
    ("aws sts get-caller-identity", "Show the account ID and identity behind the current credentials."),
    ("aws bedrock list-foundation-models", "List the foundation models available in the current Region."),
    ("aws bedrock get-foundation-model", "Show the details of one specific foundation model."),
    ("aws bedrock-runtime invoke-model", "Send a prompt to a model and return its response."),
    ("aws bedrock-agent list-knowledge-bases", "List the Bedrock knowledge bases used by the RAG labs."),
    ("aws opensearchserverless list-collections", "List OpenSearch Serverless vector collections (check after RAG labs)."),
    ("aws sagemaker list-endpoints", "List SageMaker inference endpoints — these bill continuously."),
    ("aws sagemaker delete-endpoint", "Delete a SageMaker inference endpoint during cleanup."),
    ("aws qbusiness list-applications", "List Amazon Q Business applications."),
    ("aws macie2 get-macie-session", "Show whether Amazon Macie is enabled in the Region."),
    ("aws s3 rb", "Remove an S3 bucket during cleanup (with --force to empty it first)."),
    ("aws kms schedule-key-deletion", "Schedule deletion of a KMS customer managed key."),
]

def cheatsheet_table(doc):
    rows = [["Command", "What it does"]] + [[f"`{c}`", d] for c, d in CHEATSHEET]
    _table(doc, rows)

GLOSSARY = [
    ("Foundation model", "A large model pre-trained on broad data that can be adapted to many downstream tasks."),
    ("Generative AI", "Deep-learning models that produce new content — text, image, audio or code — rather than a label."),
    ("Amazon Bedrock", "AWS managed service that serves foundation models from several providers through one API."),
    ("Amazon SageMaker", "AWS platform for building, training, tuning and hosting your own machine-learning models."),
    ("Amazon Q Business", "AWS generative-AI assistant that answers questions over an organisation's connected data."),
    ("Inference", "Using a trained model to produce an output (a prediction) for new, unseen input."),
    ("Token", "The unit of text a model reads and generates; a chunk of characters, roughly part of a word."),
    ("Embedding", "A numeric vector that represents text or other data so similar items sit close together."),
    ("Vector store", "A database that indexes embeddings for fast similarity search, as used in RAG."),
    ("RAG", "Retrieval-Augmented Generation — retrieving relevant documents and adding them to the prompt."),
    ("Prompt engineering", "Designing the input to a model to steer its output toward the desired result."),
    ("Zero-shot / few-shot", "Prompting with no worked examples, or with a few examples, to guide the model."),
    ("Fine-tuning", "Further training a foundation model on your own data to specialise its behaviour."),
    ("Hallucination", "A confident model output that is factually wrong or not grounded in the source data."),
    ("Guardrail", "A configurable policy that filters or blocks unwanted model inputs and outputs."),
    ("Prompt injection", "An attack that hides instructions in input to override a model's intended behaviour."),
    ("Bias", "Systematic skew in data or model outputs that unfairly favours or harms particular groups."),
    ("Explainability", "The degree to which a model's outputs and feature influence can be understood by humans."),
    ("Model card", "A structured document recording a model's intended use, data, performance and limitations."),
    ("Inference parameters", "Settings such as temperature, top-p and max tokens that shape a model's generation."),
    ("Hyperparameter", "A value set before training (e.g. learning rate) that controls how the model learns."),
    ("IAM", "AWS Identity and Access Management — controls who can call which AWS actions on which resources."),
]

def glossary_table(doc):
    rows = [["Term", "Meaning"]] + [[t, m] for t, m in GLOSSARY]
    _table(doc, rows)

# --------------------------------------------------------------------- main
def main():
    doc = Document()
    style_headings(doc)
    doc.styles["Normal"].font.name = "Arial"; doc.styles["Normal"].font.size = Pt(11)

    add_cover_page(doc, "Learner Guide", TITLE, VERSION, course_code=CODE, org_logo=ORG_LOGO)
    add_version_control(doc, VERSIONS)
    add_toc(doc)

    _heading(doc, "Exam Domains", 1)
    _para(doc, "This Learner Guide is a lab manual. Its 25 hands-on labs are grouped by the five "
               "official AIF-C01 exam domains and delivered across two days. Work each lab in your "
               "own AWS account; every lab ends with a cleanup step.")
    exam_domains_table(doc)

    _heading(doc, "Before You Start — Setup & Prerequisites", 1)
    tools = open(os.path.join(LABS, "tools.md"), encoding="utf-8").read()
    tools = re.sub(r'^#\s+.*\n', '', tools, count=1)  # drop the tools.md H1
    render_markdown(doc, tools, hshift=0, skip_h1=True)

    for banner, dom_nums in DAYS:
        _heading(doc, banner, 1)
        for dnum in dom_nums:
            _heading(doc, f"DOMAIN {dnum} — {DOMNAME[dnum]} ({DOMWT[dnum]}%)", 2)
            a = next(x for x in DOMAINS if x[0] == dnum)[3]
            b = next(x for x in DOMAINS if x[0] == dnum)[4]
            for n in range(a, b + 1):
                if n not in DIRS:
                    continue
                lab = load_lab(n)
                _heading(doc, f"Lab {n} — {lab['title']}", 2)
                meta = (f"**Domain:** {DOMNAME[dnum]} — **Duration:** {lab['time']} min "
                        f"— **Slides:** {lab['slides']}")
                mp = _para(doc, meta, size=10.5)
                for r in mp.runs:
                    r.font.color.rgb = BRAND
                render_markdown(doc, lab["body"], hshift=1, skip_h1=True)

    _heading(doc, "AWS Cheat-Sheet", 1)
    _para(doc, "A quick reference to AWS CLI commands used across the labs. Run them with your "
               "working Region set (see Before You Start). Add each command's own required "
               "arguments — see the AWS CLI help for exact syntax.")
    cheatsheet_table(doc)

    _heading(doc, "Glossary", 1)
    _para(doc, "Key AIF-C01 terms used throughout the labs.")
    glossary_table(doc)

    add_page_numbers(doc, left_text=f"{TITLE} · {CODE}")
    enable_update_fields(doc)

    out = os.path.join(REPO, "courseware", f"LG-{TITLE}.docx")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    doc.save(out)
    print("wrote", out)
    print(f"  labs rendered: {len(DIRS)}")
    return out

if __name__ == "__main__":
    main()
