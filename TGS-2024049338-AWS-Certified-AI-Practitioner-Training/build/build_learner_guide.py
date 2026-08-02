#!/usr/bin/env python3
"""Build the WSQ Learner Guide DOCX for TGS-2024049338 (AWS Certified AI Practitioner).

Teaching order mirrors build/build_lesson_plan.py: the master trainer deck order,
Domain 1 -> Domain 5. Slide ranges are read from build/slide_map.json -- never
hand-typed (wsq-learner-guide / wsq-lesson-plan HARD RULE).

Deliverable is the DOCX only. No Markdown mirror is written or left behind
(wsq-learner-guide HARD RULE 1).
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
VERSION = "3.0"
prodoc.TGS = f"TGS Ref No: {CODE}"

LMS = "https://lms-tms.tertiaryinfotech.com/"

SMAP = json.load(open(os.path.join(HERE, "slide_map.json"), encoding="utf-8"))
R    = SMAP["ranges"]

def rng(key):
    v = R[key]
    return f"{v['start']}–{v['end']}"

def span(*keys):
    """Contiguous span across several slide_map keys (deck order)."""
    starts = [R[k]["start"] for k in keys]
    ends   = [R[k]["end"] for k in keys]
    return f"{min(starts)}–{max(ends)}"

VERSIONS = [
    ("1.0", "29 Sep 2024", "First version", "Tertiary Infotech Academy"),
    ("2.0", "17 Oct 2025", "Update company name", "Tertiary Infotech Academy"),
    ("3.0", "20 Jul 2026",
     "Realigned to official AIF-C01 exam domains; teaching order follows the trainer deck "
     "(Domain 1-5); added Lab 2 (Amazon Bedrock) and Lab 4 (Responsible AI); slide "
     "references generated from the built deck",
     "Tertiary Infotech Academy"),
]

OVERVIEW = (
    'The "AWS Certified AI Practitioner Training (AIF-C01)" provides foundational knowledge of '
    'Generative AI, AWS AI models, and machine learning techniques. The course covers key AWS '
    'services like Amazon Q Business and Bedrock, responsible AI practices, and developing AI '
    'solutions using SageMaker. Participants learn to implement AI applications, deploy '
    'workflows, optimize models, and ensure data interoperability while addressing security, '
    'compliance, and governance. This training equips learners with practical skills to apply AI '
    'in real-world scenarios, aligning with best practices for responsible AI on AWS and '
    'preparing them for the AWS Certified AI Practitioner exam.'
)

# ---------------------------------------------------------------- Learning outcomes
# (LU, LU title, [(topic, codes)], LO text, [K/A statements])
LEARNING_OUTCOMES = [
    ("LU1", "Introduction to Generative AI",
     [("Topic 1 Generative AI for Executives", "K1, A1"),
      ("Topic 2 Amazon Q Business Getting Started", "K2, A1")],
     "LO1 - Implement AI applications with Amazon Q business and AWS AI models.",
     ["K1: Background and basics of AI.",
      "K2: Fundamental concepts and methods of statistics and programming for data science.",
      "A1: Implement AI applications in collaboration with technology service providers."]),
    ("LU2", "AWS Bedrock and Machine Learning",
     [("Topic 3 Amazon Bedrock Getting Started", "K6, A2"),
      ("Topic 4 Fundamentals of Machine Learning and Artificial Intelligence", "K4, A2")],
     "LO2 - Deploy AWS AI Bedrock workflows according to plan and machine learning techniques.",
     ["K4: Machine learning techniques and applications.",
      "K6: Software development methodologies.",
      "A2: Deploy AI workflows according to plan."]),
    ("LU3", "Applications of AI and Responsible AI",
     [("Topic 5 Exploring AI Use Cases and Applications", "K7, A3"),
      ("Topic 6 Responsible AI Practices", "K8, A3")],
     "LO3 - Identify and report issues with AI applications and data and implementation procedures.",
     ["K7: Types of AI applications.",
      "K8: AI implementation procedures.",
      "A3: Identify and report any issues with the AI applications and data collected."]),
    ("LU4", "Applications of AI and Responsible AI",
     [("Topic 7 Developing Machine Learning Solutions", "K3, A4"),
      ("Topic 8 Developing Generative AI Solutions", "K5, A4"),
      ("Topic 9 Essentials of Prompt Engineering", "K9, A4")],
     "LO4 - Maintain data interoperability during AI development in accordance to principles of "
     "data management.",
     ["K3: Mathematics and computing theories.",
      "K5: Principles of data management.",
      "K9: Interoperability of data.",
      "A4: Maintain data interoperability during the development of AI."]),
    ("LU5", "Optimization and Security of AI Solutions",
     [("Topic 10 Optimizing Foundation Models", "K10, A5"),
      ("Topic 11 Security, Compliance, and Governance for AI Solutions", "K11, A5")],
     "LO5 - Perform data cleaning techniques to optimize AWS Foundation models.",
     ["K10: Data cleaning techniques.",
      "K11: Principles of clean data sets.",
      "A5: Perform data cleaning techniques."]),
]

# ---------------------------------------------------------------- Exam domains
# (domain no, title, weight, slide-range keys spanning the domain, mapped topics)
DOMAINS = [
    (1, "Fundamentals of AI and ML", "20%",
     ("domain1", "task1.1", "task1.2", "task1.3"),
     "Topic 4 Fundamentals of Machine Learning and Artificial Intelligence; "
     "Topic 5 Exploring AI Use Cases and Applications; "
     "Topic 7 Developing Machine Learning Solutions"),
    (2, "Fundamentals of Generative AI", "24%",
     ("domain2", "task2.1", "task2.2", "task2.3"),
     "Topic 1 Generative AI for Executives; Topic 3 Amazon Bedrock Getting Started"),
    (3, "Applications of Foundation Models", "28%",
     ("domain3", "task3.1", "task3.2", "task3.3", "task3.4"),
     "Topic 8 Developing Generative AI Solutions; Topic 9 Essentials of Prompt Engineering; "
     "Topic 10 Optimizing Foundation Models; Topic 2 Amazon Q Business Getting Started"),
    (4, "Guidelines for Responsible AI", "14%",
     ("domain4", "task4.1", "task4.2"),
     "Topic 6 Responsible AI Practices"),
    (5, "Security, Compliance, and Governance for AI Solutions", "14%",
     ("domain5", "task5.1", "task5.2"),
     "Topic 11 Security, Compliance, and Governance for AI Solutions"),
]

# ---------------------------------------------------------------- Body: topics per domain
# (topic heading, slide-range key, tags, [bullets])
BODY = {
1: [
  ("Topic 4 Fundamentals of Machine Learning and Artificial Intelligence", "task1.1",
   "LU2 / LU4 · K4, A2 · Task 1.1 Explain basic AI concepts and terminologies",
   ["Artificial intelligence: definition, benefits and where it is applied",
    "Core AI capabilities: prediction and forecasting, anomaly detection, computer vision, "
    "translation, natural language processing and content creation",
    "Machine learning fundamentals and the data it consumes: structured, semi-structured, "
    "unstructured and time-series data",
    "Model training and inference (inferencing)",
    "Learning paradigms: supervised learning, unsupervised learning and reinforcement learning",
    "Model fit: overfitting and underfitting, and how they affect model performance",
    "Comparing machine learning to deep learning; introduction to large language models"]),
  ("Topic 5 Exploring Artificial Intelligence Use Cases and Applications", "task1.2",
   "LU3 · K7, A3 · Task 1.2 Identify practical use cases for AI",
   ["When to consider AI/ML for a business problem — and when not to",
    "Machine learning problem types: classification, regression and unsupervised learning",
    "AWS AI services by capability: Amazon Rekognition (computer vision), Amazon Comprehend "
    "(text and document analysis), Amazon Polly (language AI)",
    "Customer experience use cases and the business metrics used to judge them",
    "Human-in-the-loop labelling: Amazon Mechanical Turk and Amazon Augmented AI (A2I)",
    "Applied use cases: fraud detection and prevention, conversational AI for self-service, "
    "preventive maintenance, recommendation, computer vision and demand forecasting"]),
  ("Topic 7 Developing Machine Learning Solutions", "task1.3",
   "LU4 · K3, A4 · Task 1.3 Describe the ML development lifecycle",
   ["The ML lifecycle end to end, and the data pipeline that feeds it",
    "Defining the problem and choosing model options; Amazon SageMaker JumpStart",
    "Processing data with AWS Glue, the AWS Glue Data Catalog, AWS Glue DataBrew and "
    "Amazon SageMaker Canvas",
    "Training, tuning and evaluating: SageMaker Ground Truth, SageMaker Training, "
    "SageMaker Experiments and Automatic Model Tuning",
    "Deploying the model: SageMaker model deployment and SageMaker inference options",
    "Monitoring the model in production; what MLOps is; SageMaker Model Building Pipelines, "
    "repositories and orchestration tools",
    "Evaluation metrics: confusion matrix, accuracy, precision, recall (TPR), F1 score, "
    "false positive rate, specificity (TNR), ROC and AUC-ROC",
    "Regression model errors; bias and variance; AI/ML business metrics"]),
],
2: [
  ("Topic 1 Generative AI for Executives", "task2.1",
   "LU1 · K1, A1 · Task 2.1 Explain the basic concepts of generative AI",
   ["What generative AI is, and how it differs from traditional AI",
    "Generative AI for images: text-to-image, image-to-image and image-to-text; "
    "diffusion models",
    "Core generative AI concepts: prompt engineering, vectors, tokenization, context window, "
    "embeddings and self-attention",
    "Large language models and diffusion models",
    "Amazon SageMaker JumpStart for generative AI",
    "Generative AI architecture; the AI project lifecycle and the generative AI project "
    "lifecycle"]),
  ("Topic 1 Generative AI for Executives — Capabilities and Limitations", "task2.2",
   "LU1 · K1, A1 · Task 2.2 Understand the capabilities and limitations of generative AI "
   "for solving business problems",
   ["Advantages of generative AI for business problems",
    "Framing prompt engineering questions; interpretability",
    "Generative AI performance metrics and generative AI model types",
    "Business metric analysis for an ML solution",
    "Case study activity: a retail company's adoption of generative AI"]),
  ("Topic 3 Amazon Bedrock Getting Started", "task2.3",
   "LU2 · K6, A2 · Task 2.3 Describe AWS infrastructure and technologies for building "
   "generative AI applications",
   ["Transfer models and the AWS Cloud Adoption Framework",
    "The AWS AI stack and its security layers",
    "Critical components of AI systems",
    "Pricing models for generative AI workloads on AWS",
    "Foundation models available through Amazon Bedrock"]),
],
3: [
  ("Topic 8 Developing Generative Artificial Intelligence Solutions", "task3.1",
   "LU4 · K5, A4 · Task 3.1 Describe design considerations for applications that use "
   "foundation models",
   ["Design, architecture and complexity considerations for FM-based applications",
    "Inference and inference parameters; the role of the prompt",
    "Building generative AI applications on AWS with Amazon Bedrock as a fully managed service",
    "Selecting a foundation model",
    "Retrieval Augmented Generation (RAG): RAG in action on Amazon Bedrock",
    "Vector databases for RAG: types, and AWS services for vector search",
    "Amazon Bedrock Agents and the agent workflow"]),
  ("Topic 9 Essentials of Prompt Engineering", "task3.2",
   "LU4 · K9, A4 · Task 3.2 Choose effective prompt engineering techniques",
   ["What prompt engineering is; how text is generated in an LLM",
    "Prompt engineering techniques: zero-shot prompting and few-shot prompting",
    "Prompt templates and worked examples",
    "Prompt template injections (the “ignoring the prompt template” attack) and "
    "protecting against prompt injections",
    "Prompt engineering strategies, tasks and tactics; latent space",
    "Prompt engineering risks and limitations"]),
  ("Topic 10 Optimizing Foundation Models", "task3.3",
   "LU5 · K10, A5 · Task 3.3 Describe the training and fine-tuning process for foundation "
   "models",
   ["The training process for foundation models",
    "Fine-tuning techniques; fine-tuning a model on Amazon Bedrock",
    "Fine-tuning: good to know, and typical use cases",
    "Data preparation for fine-tuning",
    "AWS services for data preparation"]),
  ("Topic 2 Amazon Q Business Getting Started", "task3.4",
   "LU1 · K2, A1 · Task 3.4 Describe methods to evaluate foundation model performance",
   ["Model performance and how it is measured",
    "Evaluating a model on Amazon Bedrock, including automatic evaluation",
    "ROUGE (Recall-Oriented Understudy for Gisting Evaluation) and other generative AI "
    "performance metrics",
    "AWS services for evaluation; model integration and the generative AI application stack",
    "Amazon Q and Amazon Q Business",
    "Amazon Q Developer and its IDE extensions; PartyRock"]),
],
4: [
  ("Topic 6 Responsible Artificial Intelligence Practices", "task4.1",
   "LU3 · K8, A3 · Task 4.1 Explain the development of AI systems that are responsible",
   ["What responsible AI means in practice",
    "The effect of bias and variance; class imbalance",
    "Responsible datasets and responsible practices for model selection",
    "Amazon SageMaker Clarify: processing jobs and pre-training bias analysis",
    "Generative AI risks",
    "Guardrails for Amazon Bedrock; foundation model evaluations"]),
  ("Topic 6 Responsible Artificial Intelligence Practices — Transparency and Explainability",
   "task4.2",
   "LU3 · K8, A3 · Task 4.2 Recognize the importance of transparency and explainable models",
   ["Model transparency; interpretability compared to performance",
    "Open source AI models; model transparency on AWS",
    "SageMaker Clarify model explainability",
    "Human-centered AI and Amazon Augmented AI",
    "Transparency and model safety",
    "Reinforcement learning from human feedback (RLHF); Amazon SageMaker Ground Truth"]),
],
5: [
  ("Topic 11 Security, Compliance, and Governance for AI Solutions — Securing AI Systems",
   "task5.1",
   "LU5 · K11, A5 · Task 5.1 Explain methods to secure AI systems",
   ["The AWS Shared Responsibility Model: security of the cloud and security in the cloud",
    "AWS IAM: features, root account best practices, multi-factor authentication, users, "
    "policies, groups, roles and resource-based policies; AWS IAM Identity Center",
    "Logging with AWS CloudTrail; Amazon S3 Block Public Access; "
    "Amazon SageMaker Role Manager",
    "AWS Key Management Service; encryption at rest and in transit; Amazon Macie",
    "Amazon SageMaker and VPCs; VPC interface endpoints (AWS PrivateLink)",
    "AI system vulnerabilities and their mitigations",
    "Amazon SageMaker Model Monitor; monitoring data quality and detecting anomalies",
    "Version control and governance tooling: SageMaker Model Registry, Model Cards, "
    "ML Lineage Tracking, Feature Store and the Model Dashboard"]),
  ("Topic 11 Security, Compliance, and Governance for AI Solutions — Governance and Compliance",
   "task5.2",
   "LU5 · K11, A5 · Task 5.2 Recognize governance and compliance regulations for AI systems",
   ["AWS Artifact, compliance programs and the Customer Compliance Center",
    "Emerging AI compliance standards and emerging risk management; "
    "the Algorithmic Accountability Act",
    "AWS Audit Manager; Guardrails for Amazon Bedrock",
    "AWS Config, Amazon Inspector and AWS Trusted Advisor",
    "What data governance is, and data governance strategies",
    "Discovery and understanding with AWS Glue DataBrew; data curation with AWS Glue",
    "Protection with AWS Lake Formation and Amazon S3 Lifecycle policies",
    "Determining your scope and building an AI governance strategy",
    "Course wrap-up: practice exams, revision flashcards and Q&A"]),
],
}

# ---------------------------------------------------------------- Labs (from labs/README.md)
# (lab, domain/task, LU, topic, K, A, LO, slide, where)
LABS = [
    ("Lab 1a Train a Model with Amazon SageMaker", "D1 · 1.3", "LU4",
     "Topic 7 Developing ML Solutions", "K3", "A4", "LO4", "111", "AWS Skill Builder"),
    ("Lab 1b Streamlining Document Handling Using Amazon Textract and Amazon Polly",
     "D1 · 1.2", "LU3", "Topic 5 AI Use Cases & Applications", "K7", "A3", "LO3", "134",
     "AWS Skill Builder"),
    ("Lab 2 Amazon Bedrock Foundation Models (authored)", "D2 · 2.1–2.3", "LU2",
     "Topic 3 Amazon Bedrock Getting Started", "K6, K4", "A2", "LO2", "182",
     "labs/domain2-bedrock/"),
    ("Lab 3a Build and Evaluate RAG Applications Using Knowledge Bases for Amazon Bedrock",
     "D3 · 3.1", "LU4", "Topic 8 Developing Generative AI Solutions", "K5", "A4", "LO4",
     "204", "AWS Skill Builder"),
    ("Lab 3b Re-imagine Developer Experience Using Amazon Q Developer", "D3 · 3.4", "LU1",
     "Topic 2 Amazon Q Business Getting Started", "K2", "A1", "LO1", "270",
     "AWS Skill Builder"),
    ("Lab 4 Responsible AI: Bias Detection & Guardrails (authored)", "D4 · 4.1–4.2",
     "LU3", "Topic 6 Responsible AI Practices", "K8", "A3", "LO3", "297",
     "labs/domain4-responsible-ai/"),
    ("Lab 5a Generative BI in Amazon QuickSight", "D5 · 5.1", "LU5",
     "Topic 10 Optimizing Foundation Models", "K10", "A5", "LO5", "329", "AWS Skill Builder"),
    ("Lab 5b Securing Data in Amazon S3 Using Macie and AWS KMS", "D5 · 5.2", "LU5",
     "Topic 11 Security, Compliance & Governance", "K11", "A5", "LO5", "362",
     "AWS Skill Builder"),
    ("Escape Room for AWS Exam Prep (revision)", "—", "—", "—", "—",
     "—", "—", "364", "AWS Skill Builder"),
]

REFERENCES = [
    "Trainer Slides",
    "Lesson Plan (LP)",
    "Assessment Plan (AP)",
    "Assessment Questions and Answers",
    "Facilitator Guide (FG)",
    "Learner Guide (LG)",
    "Course Proposal (CP)",
]

# ---------------------------------------------------------------- helpers
def add_table(doc, headers, rows, widths_pt=9):
    t = doc.add_table(rows=0, cols=len(headers))
    t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hr = t.add_row().cells
    for i, h in enumerate(headers):
        hr[i].text = ""
        r = hr[i].paragraphs[0].add_run(h)
        r.bold = True; r.font.size = Pt(widths_pt); r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        _shade_cell(hr[i], "1F6FEB")
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            for j, line in enumerate(str(val).split("\n")):
                p = cells[i].paragraphs[0] if j == 0 else cells[i].add_paragraph()
                rr = p.add_run(line); rr.font.size = Pt(widths_pt)
    doc.add_paragraph()
    return t


def main():
    doc = Document()
    style_headings(doc)
    doc.styles["Normal"].font.name = "Arial"
    doc.styles["Normal"].font.size = Pt(11)

    add_cover_page(doc, "Learner Guide", TITLE, VERSION, course_code=CODE)
    add_version_control(doc, VERSIONS)
    add_toc(doc)

    # 1. Course Overview -------------------------------------------------
    doc.add_heading("Course Overview", level=1)
    doc.add_paragraph(OVERVIEW)
    p = doc.add_paragraph()
    p.add_run("Course Code: ").bold = True
    p.add_run(f"{CODE}  ·  Conducted by Tertiary Infotech Academy Pte Ltd (UEN 201200696W)")
    p = doc.add_paragraph()
    p.add_run("Trainer deck: ").bold = True
    p.add_run(f"{SMAP['total_slides']} slides. All slide references in this guide are generated "
              "from the built deck.")

    # 2. Learning Outcomes -----------------------------------------------
    doc.add_heading("Learning Outcomes", level=1)
    doc.add_paragraph(
        "The table below maps each Learning Unit to the Topics taught, the Knowledge (K) and "
        "Ability (A) statements assessed, and the Learning Outcome (LO) achieved.")
    rows = []
    for lu, lutitle, topics, lo, ka in LEARNING_OUTCOMES:
        topic_txt = "\n".join(f"{t} ({c})" for t, c in topics)
        rows.append([f"{lu}\n{lutitle}", topic_txt, lo, "\n".join(ka)])
    add_table(doc, ["Learning Unit", "Topics (K / A)", "Learning Outcome",
                    "Knowledge and Ability Statements"], rows, widths_pt=8.5)

    # 3. Exam Domain Alignment -------------------------------------------
    doc.add_heading("Exam Domain Alignment", level=1)
    doc.add_paragraph(
        "The course is aligned to the five official AWS Certified AI Practitioner (AIF-C01) "
        "exam domains. Domain weightings are from the official AIF-C01 Exam Guide. Slide "
        "ranges are read from the built trainer deck.")
    rows = [[f"Domain {n}", title, weight, span(*keys), topics]
            for n, title, weight, keys, topics in DOMAINS]
    add_table(doc, ["Domain", "Title", "Weight", "Slides", "Topics taught"], rows, widths_pt=8.5)

    # 4. Learning Units and Topics ---------------------------------------
    doc.add_heading("Learning Units and Topics", level=1)
    doc.add_paragraph(
        "Topics are presented in trainer deck order (Domain 1 to Domain 5), matching the "
        "Lesson Plan. Each topic shows its slide range and its Learning Unit, Knowledge and "
        "Ability tags.")
    for n, title, weight, keys, _topics in DOMAINS:
        doc.add_heading(f"Domain {n}: {title} ({weight})", level=2)
        pp = doc.add_paragraph()
        pp.add_run("Slides: ").bold = True
        pp.add_run(span(*keys))
        for tname, key, tags, bullets in BODY[n]:
            doc.add_heading(tname, level=3)
            pp = doc.add_paragraph()
            pp.add_run("Slides: ").bold = True
            pp.add_run(rng(key))
            pp.add_run("   ·   ")
            pp.add_run(tags).italic = True
            for b in bullets:
                doc.add_paragraph(b, style="List Bullet")

    # 5. Lab Activities ---------------------------------------------------
    doc.add_heading("Lab Activities", level=1)
    doc.add_paragraph(
        "Every exam domain carries at least one lab. Labs 2 and 4 are authored in the course "
        "repository; the remaining labs are AWS Skill Builder labs that run on AWS-hosted "
        "infrastructure. Learners sign in to AWS Skill Builder with a Builder ID.")
    add_table(doc,
              ["Lab", "Domain / Task", "LU", "Topic", "K", "A", "LO", "Slide", "Where to find it"],
              [list(l) for l in LABS], widths_pt=7.5)
    doc.add_paragraph(
        "Lab 5a (Generative BI in Amazon QuickSight) is the scenario used in the Case Study (CS) "
        "assessment. Its five CS tasks map to A1–A5. Complete Lab 5a before attempting the "
        "Case Study.")
    doc.add_paragraph(
        "Skill Builder labs run in AWS-provided sandbox accounts at no cost to the learner. The "
        "authored labs (2 and 4) run in the learner's own AWS account and can incur charges — "
        "follow the Clean Up section at the end of each authored lab. SageMaker notebook "
        "instances and inference endpoints bill continuously until deleted.")

    # 6. Assessment --------------------------------------------------------
    doc.add_heading("Assessment", level=1)
    doc.add_paragraph("The course is assessed by two components, both open book:")
    add_table(doc,
              ["Component", "Format", "Duration", "Conditions"],
              [["Written Assessment (WA-SAQ)", "11 short-answer questions", "1 hr", "Open book"],
               ["Case Study (CS)",
                "5 tasks (A1–A5) based on the Amazon QuickSight Generative BI lab (Lab 5a)",
                "1 hr", "Open book"]],
              widths_pt=9)
    doc.add_paragraph(f"Both components are submitted on the LMS at {LMS}")

    # 7. References --------------------------------------------------------
    doc.add_heading("References", level=1)
    for i, ref in enumerate(REFERENCES, 1):
        doc.add_paragraph(f"{i}. {ref}")

    add_page_numbers(doc, left_text=f"{TITLE} · {CODE}")
    enable_update_fields(doc)

    out = os.path.join(REPO, "courseware", f"LG-{TITLE}.docx")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    doc.save(out)
    print("wrote", out)
    return out


if __name__ == "__main__":
    main()
