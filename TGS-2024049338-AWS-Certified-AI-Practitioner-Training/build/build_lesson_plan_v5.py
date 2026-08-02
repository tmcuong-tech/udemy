#!/usr/bin/env python3
"""Lesson Plan v5.0 for TGS-2024049338 in the CKA layout/design.

Follows the CKA Lesson Plan (TGS-2025054612 v1.0):
  cover -> version control -> TOC -> Course Info block -> Learning Outcomes
  -> day-by-day schedule tables (Time | Topic/Activity | Duration | Slides), domain-banded
  -> "Labs Covered" summary table (Lab # | Domain | Topic | Title)
  -> Assessment section.

Keeps the AWS course at 2 days / 14 training hours. All 25 labs are mapped; each is tagged
[Demo] (in-class walkthrough) or [Self-paced] (learner's own AWS account) so the in-class total
fits 14 h. Slide ranges are read from build/slide_map.json — never hand-typed.
"""
import json, os, sys
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH


def add_header_logo(doc, logo_path, width_in=1.25):
    """Put the org logo in the running page header (top of every page after the cover)."""
    if not logo_path or not os.path.isfile(logo_path):
        return
    sec = doc.sections[0]
    sec.different_first_page_header_footer = True   # keep the cover page clean
    hdr = sec.header; hdr.is_linked_to_previous = False
    p = hdr.paragraphs[0] if hdr.paragraphs else hdr.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.add_run().add_picture(logo_path, width=Inches(width_in))

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
for cand in (os.path.join(REPO, ".claude/skills/tertiary-lesson-plan"),
             os.path.expanduser("~/.claude/skills/tertiary-lesson-plan")):
    if os.path.isdir(cand):
        sys.path.insert(0, cand); break
import prodoc
from prodoc import (add_cover_page, add_version_control, add_toc,
                    add_page_numbers, enable_update_fields, style_headings, _shade_cell)

TITLE   = "AWS Certified AI Practitioner Training (AIF-C01)"
CODE    = "TGS-2024049338"
VERSION = "5.0"
prodoc.TGS = f"TGS Ref No: {CODE}"
ORG_LOGO = next((x for x in (
    os.path.join(REPO, ".claude/skills/tertiary-lesson-plan/assets/tertiary-infotech-logo.png"),
    os.path.expanduser("~/.claude/skills/tertiary-lesson-plan/assets/tertiary-infotech-logo.png"),
) if os.path.isfile(x)), None)

DARK  = RGBColor(0x11, 0x18, 0x27)
BRAND = RGBColor(0x1F, 0x6F, 0xEB)
GREY  = RGBColor(0x55, 0x5B, 0x66)

VERSIONS = [
    ("1.0", "29 Sep 2024", "First version", "Tertiary Infotech Academy"),
    ("2.0", "", "New Format", "Tertiary Infotech Academy"),
    ("3.0", "17 Oct 2025", "Update company name", "Tertiary Infotech Academy"),
    ("4.0", "20 Jul 2026",
     "Realigned to official AIF-C01 exam domains; teaching order follows the deck (Domain 1–5) "
     "with contiguous slide ranges; Slides column populated from the built deck.",
     "Tertiary Infotech Academy"),
    ("5.0", "21 Jul 2026",
     "Reformatted to the current house lesson-plan layout (Course Information, Learning Outcomes, "
     "Learning Reinforcement, Course Schedule, Lab Reference); day-by-day schedule as Time / Duration "
     "/ Topic-Activity with a Slides column retained; Lab Reference table maps each exam domain, its "
     "weighting and its labs. Deck and 2-day / 14-hour duration unchanged.",
     "Tertiary Infotech Academy"),
]

DOMAINS = [
    (1, "Fundamentals of AI and ML", 20),
    (2, "Fundamentals of Generative AI", 24),
    (3, "Applications of Foundation Models", 28),
    (4, "Guidelines for Responsible AI", 14),
    (5, "Security, Compliance, and Governance for AI Solutions", 14),
]

# Lab catalogue: (num, domain, topic, title, mins, slides, mode)
LABS = [
 (1,1,"AI/ML terminology","AI, ML and Deep Learning Terminology",30,"25–51","Demo"),
 (2,1,"Data & labelling","Data Types and Labelling for ML",35,"25–51","Demo"),
 (3,1,"AWS AI services","AWS Managed AI Services Tour",40,"52–83","Demo"),
 (4,1,"SageMaker","Train and Deploy a Model with SageMaker",45,"84–135","Self-paced"),
 (5,1,"ML pipeline","The ML Pipeline and Data Preparation",40,"84–135","Self-paced"),
 (6,2,"Amazon Bedrock","Amazon Bedrock Getting Started",30,"137–164","Demo"),
 (7,2,"Foundation models","Comparing Foundation Models and Inference Parameters",35,"137–164","Demo"),
 (8,2,"Tokens & embeddings","Tokens, Embeddings and Vector Representations",35,"137–164","Demo"),
 (9,2,"GenAI limits","Generative AI Capabilities and Limitations",30,"165–172","Demo"),
 (10,2,"Service choice","Choosing Bedrock, SageMaker JumpStart or a Managed Service",35,"173–182","Demo"),
 (11,2,"Amazon Q Business","Amazon Q Business Getting Started",40,"173–182","Self-paced"),
 (12,3,"Prompt basics","Prompt Engineering Basics — Zero-Shot and Few-Shot",35,"210–235","Demo"),
 (13,3,"Advanced prompting","Advanced Prompting and Prompt Templates",40,"210–235","Demo"),
 (14,3,"Prompt risks","Prompt Misuse, Injection and Defences",35,"210–235","Demo"),
 (15,3,"RAG","RAG with Knowledge Bases for Amazon Bedrock",45,"184–209","Self-paced"),
 (16,3,"Vector stores","Vector Stores and Retrieval Quality",40,"184–209","Self-paced"),
 (17,3,"Fine-tuning","Fine-Tuning and Model Customisation",40,"236–247","Self-paced"),
 (18,3,"Evaluation","Evaluating Foundation Model Performance",40,"248–271","Self-paced"),
 (19,4,"Guardrails","Amazon Bedrock Guardrails",40,"273–284","Demo"),
 (20,4,"Bias detection","Bias Detection with SageMaker Clarify",40,"273–284","Self-paced"),
 (21,4,"Explainability","Explainability and Feature Attribution",35,"285–297","Demo"),
 (22,4,"Model cards","Model Cards and Transparency",30,"285–297","Demo"),
 (23,5,"IAM & KMS","Securing AI Workloads with IAM and KMS",40,"299–333","Self-paced"),
 (24,5,"Macie","Data Protection with Amazon Macie",35,"299–333","Self-paced"),
 (25,5,"Governance","Governance, Audit and Model Lineage",35,"334–374","Demo"),
]
LAB = {l[0]: l for l in LABS}
DOMNAME = {n: nm for n, nm, w in DOMAINS}
DOMWT   = {n: w for n, nm, w in DOMAINS}

def lab_cell(nums):
    """Activity cell text for one or more labs."""
    out = []
    for n in nums:
        _, _, _, title, mins, _, mode = LAB[n]
        out.append(f"Lab {n}: {title} [{mode}]")
    return "\n".join(out)

def lab_slides(nums):
    return ", ".join(sorted({LAB[n][5] for n in nums}, key=lambda s: int(s.split("–")[0])))

ATT = "QR Attendance, Attendance Sheet, TV, Laptop, Wi-Fi"

# Day schedules: rows = (time, activity, duration, slides)
DAY1 = [
 ("9:00 – 9:15", "Registration & Digital Attendance (AM) — trainer/learner intro, course structure, "
  "AWS account & Bedrock model-access check", "15 min", "1–22"),
 ("9:15 – 9:45", "DOMAIN 1 — Fundamentals of AI and ML (20%)\nLecture: AI vs ML vs deep learning; "
  "learning types; inferencing; data types", "30 min", "24–51"),
 ("9:45 – 10:30", lab_cell([1, 2]) + "\nGuided walkthrough; full labs self-paced in own account",
  "45 min", lab_slides([1, 2])),
 ("10:30 – 10:45", "Tea Break", "15 min", "—"),
 ("10:45 – 11:45", "Lecture: AI use cases & AWS managed AI services; ML development lifecycle\n"
  + lab_cell([3]), "60 min", "52–135"),
 ("11:45 – 12:15", lab_cell([4, 5]) + "\nOverview + cost/cleanup briefing; run self-paced",
  "30 min", lab_slides([4, 5])),
 ("12:15 – 1:15", "Lunch Break", "60 min", "—"),
 ("1:15 – 1:25", "Digital Attendance (PM)", "10 min", "—"),
 ("1:25 – 2:25", "DOMAIN 2 — Fundamentals of Generative AI (24%)\nLecture: foundation models; "
  "generative AI concepts; tokens & embeddings", "60 min", "136–164"),
 ("2:25 – 3:10", lab_cell([6, 7, 8]), "45 min", lab_slides([6, 7, 8])),
 ("3:10 – 3:25", "Tea Break", "15 min", "—"),
 ("3:25 – 4:25", "Lecture: capabilities vs limitations; AWS infra for GenAI; service selection\n"
  + lab_cell([9, 10]), "60 min", "165–182"),
 ("4:25 – 5:05", lab_cell([11]) + "\nOverview; run self-paced in own account", "40 min",
  lab_slides([11])),
 ("5:05 – 5:50", "Case Study — Generative AI adoption (Retail / Amazon Q Business)", "45 min",
  "137–182"),
 ("5:50 – 6:00", "Day 1 Review & Q&A", "10 min", "—"),
]

DAY2 = [
 ("9:00 – 9:10", "Digital Attendance (AM) — Day 1 recap", "10 min", "—"),
 ("9:10 – 10:10", "DOMAIN 3 — Applications of Foundation Models (28%)\nLecture: design considerations; "
  "prompt engineering", "60 min", "183–235"),
 ("10:10 – 10:55", lab_cell([12, 13, 14]), "45 min", lab_slides([12, 13, 14])),
 ("10:55 – 11:10", "Tea Break", "15 min", "—"),
 ("11:10 – 12:10", "Lecture: RAG; fine-tuning; model evaluation\n" + lab_cell([15, 16]) +
  "\nOverview + cost/cleanup briefing; run self-paced", "60 min", "184–271"),
 ("12:10 – 1:10", "Lunch Break", "60 min", "—"),
 ("1:10 – 1:20", "Digital Attendance (PM)", "10 min", "—"),
 ("1:20 – 1:50", lab_cell([17, 18]) + "\nOverview; run self-paced (Lab 17 config only — do not provision)",
  "30 min", lab_slides([17, 18])),
 ("1:50 – 2:40", "DOMAIN 4 — Guidelines for Responsible AI (14%)\nLecture: responsible AI dimensions; "
  "transparency & explainability\n" + lab_cell([19]), "50 min", "272–297"),
 ("2:40 – 3:20", lab_cell([20, 21, 22]), "40 min", lab_slides([20, 21, 22])),
 ("3:20 – 3:35", "Tea Break", "15 min", "—"),
 ("3:35 – 4:25", "DOMAIN 5 — Security, Compliance & Governance (14%)\nLecture: securing AI; "
  "governance & compliance\n" + lab_cell([23, 24, 25]), "50 min", "298–374"),
 ("4:25 – 4:40", "Assessment Briefing — WSQ assessment instructions and rules", "15 min", "284"),
 ("4:40 – 5:40", "WSQ Written Assessment — Short-Answer Questions (WA-SAQ), 11 questions", "60 min",
  "368–374"),
 ("5:40 – 6:40", "WSQ Practical Assessment (CS) — lab-based practical tasks A1–A5", "60 min", "—"),
 ("6:40", "Assessment submission & close", "—", "—"),
]

# CLSSGB schedule layout: Time | Duration | Topic / Activity  (+ Slides, retained per course)
HDR = ["Time", "Duration", "Topic / Activity", "Slides"]

# --------------------------------------------------------------- rendering
def h(doc, text, level):
    doc.add_heading(text, level=level)

def para(doc, text, bold=False, size=10, color=DARK, after=4):
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(after)
    r = p.add_run(text); r.bold = bold; r.font.size = Pt(size); r.font.color.rgb = color
    r.font.name = "Arial"; return p

def bullets(doc, items):
    for it in items:
        p = doc.add_paragraph(style="List Bullet"); p.paragraph_format.space_after = Pt(3)
        r = p.add_run(it); r.font.size = Pt(10); r.font.name = "Arial"

def info_table(doc, rows):
    t = doc.add_table(rows=0, cols=2); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for k, v in rows:
        cells = t.add_row().cells
        cells[0].text = ""; r = cells[0].paragraphs[0].add_run(k)
        r.bold = True; r.font.size = Pt(9.5); r.font.name = "Arial"; _shade_cell(cells[0], "EEF3FB")
        cells[1].text = ""; rr = cells[1].paragraphs[0].add_run(v)
        rr.font.size = Pt(9.5); rr.font.name = "Arial"
    doc.add_paragraph()

def schedule_table(doc, rows):
    """rows are (time, activity, duration, slides); rendered CLSSGB-order Time|Duration|Activity|Slides."""
    t = doc.add_table(rows=0, cols=4); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hr = t.add_row().cells
    for i, htext in enumerate(HDR):
        hr[i].text = ""; r = hr[i].paragraphs[0].add_run(htext)
        r.bold = True; r.font.size = Pt(9); r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        _shade_cell(hr[i], "1F6FEB")
    for time, act, dur, sl in rows:
        cells = t.add_row().cells
        for i, val in enumerate((time, dur, act, sl)):
            cells[i].text = ""
            for j, ln in enumerate(str(val).split("\n")):
                p = cells[i].paragraphs[0] if j == 0 else cells[i].add_paragraph()
                rr = p.add_run(ln); rr.font.size = Pt(9); rr.font.name = "Arial"
                if ln.startswith("DOMAIN "): rr.bold = True; rr.font.color.rgb = BRAND
    doc.add_paragraph()

def lab_reference(doc):
    """CLSSGB 'Lab Reference' table: Domain | Weighting | Labs | Slides."""
    t = doc.add_table(rows=0, cols=4); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hr = t.add_row().cells
    for i, htext in enumerate(["Exam Domain / Topic", "Weighting", "Labs", "Slides"]):
        hr[i].text = ""; r = hr[i].paragraphs[0].add_run(htext)
        r.bold = True; r.font.size = Pt(9); r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        _shade_cell(hr[i], "1F6FEB")
    for dnum, dname, wt in DOMAINS:
        dl = [l for l in LABS if l[1] == dnum]
        labs = ", ".join(f"Lab {l[0]}" for l in dl)
        slides = ", ".join(sorted({l[5] for l in dl}, key=lambda s: int(s.split("–")[0])))
        cells = t.add_row().cells
        for i, val in enumerate((f"DOMAIN {dnum}: {dname}", f"{wt}%", labs, slides)):
            cells[i].text = ""; rr = cells[i].paragraphs[0].add_run(val)
            rr.font.size = Pt(8.5); rr.font.name = "Arial"
            if i == 0: rr.bold = True
    doc.add_paragraph()

def main():
    doc = Document()
    style_headings(doc)
    doc.styles["Normal"].font.name = "Arial"; doc.styles["Normal"].font.size = Pt(10)

    add_cover_page(doc, "LESSON PLAN", TITLE, VERSION, course_code=CODE, org_logo=ORG_LOGO)
    add_version_control(doc, VERSIONS)
    add_toc(doc)

    h(doc, "Course Information", 1)
    info_table(doc, [
        ("Course Title", "AWS Certified AI Practitioner (AIF-C01)"),
        ("Course Code", CODE),
        ("Training Provider", "Tertiary Infotech Academy Pte Ltd (UEN 201200696W)"),
        ("Duration", "2 days — 7 training hours per day (14 training hours + 2 assessment hours)"),
        ("Daily Timing", "9:00 AM – 6:00 PM (1-hour lunch; tea breaks within training). Day 2 runs to "
                         "6:40 PM to include the assessment."),
        ("Mode", "Instructor-led, with demonstrations and hands-on labs in the learner's own AWS "
                 "account"),
        ("Prerequisites", "Basic IT literacy; an AWS account with Amazon Bedrock model access requested"),
        ("Tools", "AWS Management Console, AWS CLI, Amazon Bedrock, SageMaker, Amazon Q Business, "
                  "Amazon Macie, and the 25 course labs"),
    ])
    para(doc, "Course Overview", bold=True, size=11, color=BRAND)
    para(doc, "This 2-day hands-on course prepares participants for the AWS Certified AI Practitioner "
              "(AIF-C01) certification. Through instructor-led sessions and 25 structured labs, "
              "participants gain practical skills across the five official exam domains: Fundamentals "
              "of AI and ML (20%); Fundamentals of Generative AI (24%); Applications of Foundation "
              "Models (28%); Guidelines for Responsible AI (14%); and Security, Compliance and "
              "Governance for AI Solutions (14%).")

    h(doc, "Learning Outcomes", 1)
    for lo in [
        "LO1 — Implement AI applications with Amazon Q Business and AWS AI models.",
        "LO2 — Deploy AWS AI Bedrock workflows according to plan and machine learning techniques.",
        "LO3 — Identify and report issues with AI applications, data and implementation procedures.",
        "LO4 — Maintain data interoperability during AI development per data-management principles.",
        "LO5 — Perform data cleaning techniques to optimise AWS foundation models.",
    ]:
        doc.add_paragraph(lo, style="List Bullet")

    h(doc, "Learning Reinforcement", 1)
    para(doc, "Learning is reinforced continuously in class rather than through theory alone:")
    bullets(doc, [
        "Every concept is followed by a hands-on lab that applies it in the learner's own AWS account.",
        "Each lab ends with a verification step so learners confirm their own output before moving on.",
        "Lab outputs build toward the practical assessment — the same techniques are re-used in the "
        "case-study tasks (A1–A5).",
        "Labs that create billing resources include a cost warning and a cleanup step.",
        "Day 2 closes with the WSQ written and practical assessments and a recap against the learning "
        "outcomes.",
    ])

    h(doc, "Course Schedule", 1)
    h(doc, "Day 1 — Domains 1 & 2 (Fundamentals of AI/ML and Generative AI)", 2)
    schedule_table(doc, DAY1)
    h(doc, "Day 2 — Domains 3, 4 & 5 + Assessment", 2)
    schedule_table(doc, DAY2)

    h(doc, "Lab Reference (aligned to the exam domains)", 1)
    para(doc, "All 25 hands-on labs mirror the slide deck and Learner Guide. Labs tagged [Demo] are "
              "walked through in class; labs tagged [Self-paced] are completed in the learner's own "
              "AWS account (several create billing resources — always complete the cleanup step).")
    lab_reference(doc)

    h(doc, "Assessment", 1)
    para(doc, "Participants are assessed by two WSQ instruments on Day 2 afternoon:")
    doc.add_paragraph("Written Assessment — Short-Answer Questions (WA-SAQ): 11 open-ended knowledge "
                      "questions (K1–K11), 1 hour, open book.", style="List Bullet")
    doc.add_paragraph("Practical Assessment (Case Study): lab-based practical tasks mapped to abilities "
                      "A1–A5, 1 hour, open book. Each task is completed using the course labs.",
                      style="List Bullet")
    para(doc, "A minimum competency grade of Competent (C) in both instruments is required to satisfy "
              "WSQ requirements.")
    para(doc, "Total Training Hours: 14 hrs  ·  Total Assessment Hours: 2 hrs", bold=True)

    add_page_numbers(doc, left_text=f"{TITLE} · {CODE}")
    enable_update_fields(doc)

    # courseware/ was renamed to Examples/ during a reorg; write where the current AWS files live.
    outdir = os.environ.get("OUTDIR") or "courseware"
    out = os.path.join(REPO, outdir, f"LP-{TITLE}.docx")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    doc.save(out)
    inclass = sum(l[4] for l in LABS if l[6] == "Demo")
    print("wrote", out)
    print(f"  labs: {len(LABS)}  | demo(in-class) mins: {inclass}  | self-paced mins: {sum(l[4] for l in LABS)-inclass}")

if __name__ == "__main__":
    main()
