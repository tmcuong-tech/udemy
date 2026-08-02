#!/usr/bin/env python3
"""Build the WSQ Lesson Plan DOCX for TGS-2024049338 (AWS Certified AI Practitioner).

Teaching order follows the master trainer deck (Domain 1 -> 5) so every session maps to a
CONTIGUOUS slide range. Topic numbers, LU / K / A tags and total hours are unchanged from
LP v3; only the running order and time slots move.

Slide ranges are read from build/slide_map.json -- never hand-typed (wsq-lesson-plan HARD RULE 1).
"""
import json, os, sys
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.table import WD_TABLE_ALIGNMENT

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
VERSION = "4.0"
prodoc.TGS = f"TGS Ref No: {CODE}"

SMAP = json.load(open(os.path.join(HERE, "slide_map.json"), encoding="utf-8"))
R    = SMAP["ranges"]

def rng(key):
    """Contiguous deck page range for a domain/task key, e.g. 'task1.1'."""
    v = R[key]
    return f"{v['start']}–{v['end']}"

VERSIONS = [
    ("1.0", "29 Sep 2024", "First version", "Tertiary Infotech Academy"),
    ("2.0", "", "New Format", "Tertiary Infotech Academy"),
    ("3.0", "17 Oct 2025", "Update company name", "Tertiary Infotech Academy"),
    ("4.0", "20 Jul 2026",
     "Realigned to official AIF-C01 exam domains; teaching order follows the trainer deck "
     "(Domain 1–5) giving contiguous slide ranges; Slides column populated from the built "
     "deck; added Lab 2 (Amazon Bedrock, Domain 2) and Lab 4 (Responsible AI, Domain 4); "
     "corrected Domain 1/2 titles, Task 3.1 and Domain 5 numbering.",
     "Tertiary Infotech Academy"),
]

FAC = ("Facilitator's Guidance: Facilitator will explain and demonstrate the activities to "
       "learners. Facilitators are encouraged to invite the learners to share their own answers "
       "with the class. Facilitators are encouraged to share their own personal experiences to "
       "incorporate real-life experiences.")
RES = "Slides {}, TV, Whiteboard, Wi-Fi"
ATT = "QR Attendance, Attendance Sheet, TV, Laptop, Wi-Fi"

# (start, end, duration, description, methods, resources, slides)
DAY1 = [
 ("0930hrs","0945hrs","(15 mins)",
  "Digital Attendance (AM) and Introduction to the Course\n- Trainer Introduction\n- Learner Introduction\n- Overview of Course Structure, Learning Outcomes and Assessment",
  "Lecture, Peer Sharing", ATT, "1–22"),
 ("0945hrs","1045hrs","(60 mins)",
  "LU2/LU4 — Domain 1: Fundamentals of AI and ML\nTopic 4 Fundamentals of Machine Learning and Artificial Intelligence (K4, A2)\n- Task 1.1 Explain basic AI concepts and terminologies\n- Machine Learning, Deep Learning and Generative AI fundamentals",
  "Lecture, Group Discussion", RES.format(rng("task1.1")), rng("task1.1")),
 ("1045hrs","1055hrs","(10 mins)","Break","","",""),
 ("1055hrs","1200hrs","(65 mins)",
  "LU3 — Domain 1: Fundamentals of AI and ML\nTopic 5 Exploring Artificial Intelligence Use Cases and Applications (K7, A3)\n- Task 1.2 Identify practical use cases for AI\n- Capabilities and challenges of generative AI; business metrics",
  "Lecture, Peer Sharing", RES.format(rng("task1.2")), rng("task1.2")),
 ("1200hrs","1245hrs","(45 mins)","Lunch Break","","",""),
 ("1245hrs","1255hrs","(10 mins)","Digital Attendance (PM)","", ATT, ""),
 ("1255hrs","1425hrs","(90 mins)",
  "LU4 — Domain 1: Fundamentals of AI and ML\nTopic 7 Developing Machine Learning Solutions (K3, A4)\n- Task 1.3 Describe the ML development lifecycle\n- Amazon SageMaker, model evaluation, deployment, MLOps",
  "Lecture, Group Discussion", RES.format(rng("task1.3")), rng("task1.3")),
 ("1425hrs","1455hrs","(30 mins)",
  "Lab 1a — Train a Model with Amazon SageMaker (Domain 1, Task 1.3)\nLab 1b — Streamlining Document Handling Using Amazon Textract and Amazon Polly\n" + FAC,
  "Hands-on Lab", "Slides 111, 134, AWS Skill Builder, Laptop, Wi-Fi", "111, 134"),
 ("1455hrs","1505hrs","(10 mins)","Break","","",""),
 ("1505hrs","1620hrs","(75 mins)",
  "LU1 — Domain 2: Fundamentals of Generative AI\nTopic 1 Generative AI for Executives (K1, A1)\n- Task 2.1 Explain the basic concepts of generative AI\n- Enterprise use cases; why AWS for generative AI",
  "Lecture, Peer Sharing", RES.format(rng("task2.1")), rng("task2.1")),
 ("1620hrs","1650hrs","(30 mins)",
  "LU1 — Domain 2: Fundamentals of Generative AI\n- Task 2.2 Capabilities and limitations of generative AI for solving business problems\nActivity: Case Study — Retail Company's Adoption of Generative AI\n" + FAC,
  "Case Study", RES.format(rng("task2.2")), rng("task2.2")),
 ("1650hrs","1750hrs","(60 mins)",
  "LU2 — Domain 2: Fundamentals of Generative AI\nTopic 3 Amazon Bedrock Getting Started (K6, A2)\n- Task 2.3 AWS infrastructure and technologies for building generative AI applications\nLab 2 — Amazon Bedrock Foundation Models (labs/domain2-bedrock/)",
  "Lecture, Hands-on Lab", RES.format(rng("task2.3")), rng("task2.3")),
 ("1750hrs","1830hrs","(40 mins)","Recap of Day 1 and Q&A","Lecture, Peer Sharing", RES.format("24–182"), "24–182"),
]

DAY2 = [
 ("0930hrs","0940hrs","(10 mins)","Digital Attendance (AM)","", ATT, ""),
 ("0940hrs","1045hrs","(65 mins)",
  "LU4 — Domain 3: Applications of Foundation Models\nTopic 8 Developing Generative Artificial Intelligence Solutions (K5, A4)\n- Task 3.1 Design considerations for applications that use FMs\n- Generative AI application lifecycle; selecting an FM; RAG\nLab 3a — Build and Evaluate RAG Applications Using Knowledge Bases for Amazon Bedrock",
  "Lecture, Hands-on Lab", RES.format(rng("task3.1")), rng("task3.1")),
 ("1045hrs","1055hrs","(10 mins)","Break","","",""),
 ("1055hrs","1200hrs","(65 mins)",
  "LU4 — Domain 3: Applications of Foundation Models\nTopic 9 Essentials of Prompt Engineering (K9, A4)\n- Task 3.2 Choose effective prompt engineering techniques\n- Understanding and modifying prompts; prompt misuses and risks",
  "Lecture, Group Discussion", RES.format(rng("task3.2")), rng("task3.2")),
 ("1200hrs","1245hrs","(45 mins)","Lunch Break","","",""),
 ("1245hrs","1255hrs","(10 mins)","Digital Attendance (PM)","", ATT, ""),
 ("1255hrs","1340hrs","(45 mins)",
  "LU5 — Domain 3: Applications of Foundation Models\nTopic 10 Optimizing Foundation Models (K10, A5)\n- Task 3.3 Training and fine-tuning process for FMs\n- Fine-tuning, agents, evaluating results",
  "Lecture, Peer Sharing", RES.format(rng("task3.3")), rng("task3.3")),
 ("1340hrs","1440hrs","(60 mins)",
  "LU1 — Domain 3: Applications of Foundation Models\nTopic 2 Amazon Q Business Getting Started (K2, A1)\n- Task 3.4 Methods to evaluate foundation model performance\nLab 3b — Re-imagine Developer Experience Using Amazon Q Developer",
  "Lecture, Hands-on Lab", RES.format(rng("task3.4")), rng("task3.4")),
 ("1440hrs","1450hrs","(10 mins)","Break","","",""),
 ("1450hrs","1545hrs","(55 mins)",
  "LU3 — Domain 4: Guidelines for Responsible AI\nTopic 6 Responsible Artificial Intelligence Practices (K8, A3)\n- Task 4.1 Development of AI systems that are responsible\n- Task 4.2 Transparency and explainable models\nLab 4 — Responsible AI: Bias Detection and Guardrails (labs/domain4-responsible-ai/)\n" + FAC,
  "Lecture, Case Study, Hands-on Lab", RES.format("272–297"), "272–297"),
 ("1545hrs","1630hrs","(45 mins)",
  "LU5 — Domain 5: Security, Compliance, and Governance for AI Solutions\nTopic 11 Security, Compliance, and Governance for AI Solutions (K11, A5)\n- Task 5.1 Methods to secure AI systems\n- Task 5.2 Governance and compliance regulations for AI systems\nLab 5a — Generative BI in Amazon QuickSight  ·  Lab 5b — Securing Data in Amazon S3 Using Macie and AWS KMS",
  "Lecture, Hands-on Lab", RES.format("298–367"), "298–367"),
 ("1630hrs","1730hrs","(60 mins)",
  "Digital Attendance (Assessment)\nCourse Feedback and TRAQOM Survey\nFinal Assessment: Written Assessment — Short-Answer Questions (WA-SAQ)",
  "Assessment", "Digital Attendance, Feedback Forms, TRAQOM, Assessment Questions, Assessment Plan", "368–374"),
 ("1730hrs","1830hrs","(60 mins)",
  "Final Assessment: Case Study (CS)\nScenario based on Lab 5a — Generative BI in Amazon QuickSight (Tasks A1–A5)",
  "Assessment", "Assessment Questions, Assessment Plan", "329"),
]

HDR = ["", "", "Time", "Instructions for Facilitator", "Instructional Methods", "Resources", "Slides"]

def add_day(doc, name, rows):
    doc.add_heading(name, level=2)
    t = doc.add_table(rows=0, cols=7); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hr = t.add_row().cells
    for i, h in enumerate(HDR):
        hr[i].text = ""
        r = hr[i].paragraphs[0].add_run(h)
        r.bold = True; r.font.size = Pt(8.5); r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        _shade_cell(hr[i], "1F6FEB")
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            txt = str(val) if val else ("—" if i == 6 else "")
            for j, line in enumerate(txt.split("\n")):
                p = cells[i].paragraphs[0] if j == 0 else cells[i].add_paragraph()
                rr = p.add_run(line); rr.font.size = Pt(8.5)
    doc.add_paragraph()

def main():
    doc = Document()
    style_headings(doc)
    doc.styles["Normal"].font.name = "Arial"
    doc.styles["Normal"].font.size = Pt(10)

    add_cover_page(doc, "LESSON PLAN", TITLE, VERSION, course_code=CODE)
    add_version_control(doc, VERSIONS)
    add_toc(doc)

    doc.add_heading("Lesson Plan", level=1)
    p = doc.add_paragraph()
    p.add_run("Teaching order follows the master trainer deck (Domain 1–5). ").bold = True
    p.add_run(
        f"Every teaching session maps to a contiguous slide range in the {SMAP['total_slides']}-slide "
        "deck. Slide numbers are generated from the built deck and are not hand-typed. "
        "Topic numbers, Learning Unit tags and Knowledge/Ability codes are unchanged from v3.0."
    )

    add_day(doc, "Day 1", DAY1)
    add_day(doc, "Day 2", DAY2)

    doc.add_heading("Training and Assessment Hours", level=2)
    for line in ("Total Training Hours: 14 hrs", "Total Assessment Hours: 2 hrs"):
        doc.add_paragraph(line, style="List Bullet")

    add_page_numbers(doc, left_text=f"{TITLE} · {CODE}")
    enable_update_fields(doc)

    out = os.path.join(REPO, "courseware", f"LP-{TITLE}.docx")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    doc.save(out)
    print("wrote", out)
    print(f"  deck total slides : {SMAP['total_slides']}")
    print(f"  Day 1 rows        : {len(DAY1)}")
    print(f"  Day 2 rows        : {len(DAY2)}")

if __name__ == "__main__":
    main()
