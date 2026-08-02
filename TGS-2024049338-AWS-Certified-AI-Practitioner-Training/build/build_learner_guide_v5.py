#!/usr/bin/env python3
"""Learner Guide v4.0 for TGS-2024049338 in the CLSSGB house learner-guide layout.

Follows Examples/LG-Certified Lean Six Sigma Green Belt (CLSSGB).docx exactly:
  cover -> version control -> TOC -> Introduction -> Course Learning Outcomes
  -> Before You Start -> one H1 per exam domain (weighting in the heading) with each
  lab as an H2 in concise prose (Objective / Goal / What you'll build / At a glance /
  Step-by-step numbered list) -> Quick Reference -> Consolidating What You Learned
  -> Glossary.

Concise, prose-based. Per-lab title/time/slides/steps are read from the lab files
(labs/lab-NN-*/index.json + lab.md) - never hand-typed. Objective/Goal/What-you'll-build
are faithful one-line rephrasings of each lab's own description and steps.
"""
import json, os, re, sys, glob
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH


def add_header_logo(doc, logo_path, width_in=1.25):
    """Put the org logo in the running page header (top of every page after the cover)."""
    if not logo_path or not os.path.isfile(logo_path):
        return
    sec = doc.sections[0]
    sec.different_first_page_header_footer = True
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
VERSION = "4.0"
prodoc.TGS = f"TGS Ref No: {CODE}"
ORG_LOGO = next((x for x in (
    os.path.join(REPO, ".claude/skills/tertiary-lesson-plan/assets/tertiary-infotech-logo.png"),
    os.path.expanduser("~/.claude/skills/tertiary-lesson-plan/assets/tertiary-infotech-logo.png"),
) if os.path.isfile(x)), None)

DARK  = RGBColor(0x11, 0x18, 0x27)
BRAND = RGBColor(0x1F, 0x6F, 0xEB)

VERSIONS = [
    ("1.0", "29 Sep 2024", "First version", "Tertiary Infotech Academy"),
    ("2.0", "17 Oct 2025", "Update company name", "Tertiary Infotech Academy"),
    ("3.0", "20 Jul 2026", "Realigned to AIF-C01 exam domains", "Tertiary Infotech Academy"),
    ("4.0", "21 Jul 2026",
     "Reformatted to the current house learner-guide layout: concise per-lab format grouped by "
     "exam domain, with Before-You-Start, Quick Reference and Glossary. Slide references retained.",
     "Tertiary Infotech Academy"),
]

DOMAINS = [
    (1, "Fundamentals of AI and ML", 20, range(1, 6)),
    (2, "Fundamentals of Generative AI", 24, range(6, 12)),
    (3, "Applications of Foundation Models", 28, range(12, 19)),
    (4, "Guidelines for Responsible AI", 14, range(19, 23)),
    (5, "Security, Compliance and Governance for AI Solutions", 14, range(23, 26)),
]
SELF_PACED = {4, 5, 11, 15, 16, 17, 18, 20, 23, 24}

# Faithful one-line Objective / Goal / What-you'll-build per lab, rephrased from each
# lab's own index.json description + steps (no invented AWS facts).
LG = {
 1: ("Build a precise vocabulary for AI, ML, deep learning and generative AI and locate each in the AWS console.",
     "These four terms nest inside one another; using them precisely is the foundation the exam and every later lab build on.",
     "A layered AI / ML / deep-learning / generative-AI concept map tied to the AWS services that embody each layer."),
 2: ("Classify structured, semi-structured and unstructured data and produce a labelled image dataset.",
     "Model quality starts with data; knowing data types and labelled versus unlabelled data is prerequisite to any ML work.",
     "An S3-hosted dataset plus a SageMaker Ground Truth labelling job and its output manifest."),
 3: ("Use Amazon Comprehend, Translate, Polly, Transcribe and Rekognition from the console.",
     "AWS managed AI services solve common tasks with no model training; matching each to a use case is core exam knowledge.",
     "A worked example in each of the five managed AI services and a service-to-use-case matching table."),
 4: ("Train, deploy and evaluate a binary classifier with SageMaker built-in XGBoost, then delete every billing resource.",
     "Walking the full train-deploy-infer loop makes the ML lifecycle concrete and shows where cost accrues.",
     "A trained XGBoost model served from a real-time SageMaker endpoint."),
 5: ("Design a complete ML pipeline for a churn scenario, from business framing to monitoring.",
     "Every production model follows the same pipeline; being able to place each stage is essential to the exam and to real work.",
     "An end-to-end ML pipeline design grounded in the SageMaker console, from data prep and feature engineering to deployment and monitoring."),
 6: ("Enable foundation model access in Amazon Bedrock and run your first prompt.",
     "Bedrock is the gateway to foundation models on AWS; model access and the playground underpin every generative-AI lab that follows.",
     "An access-enabled Bedrock account, a tour of the model catalogue and a first playground prompt."),
 7: ("Compare foundation models on one prompt, then vary temperature, top-P and max tokens.",
     "Model choice and inference parameters shape every generative output and are directly tested.",
     "A side-by-side model comparison and a record of how each inference parameter changes the output."),
 8: ("Turn text into tokens, generate embeddings and measure semantic similarity.",
     "Tokens drive cost and context limits, and embeddings power search and RAG; both are recurring exam concepts.",
     "A token-count analysis and embedding vectors compared for semantic similarity."),
 9: ("Exercise what generative AI does well, produce a hallucination, and apply mitigations.",
     "Knowing both the capabilities and the limitations of generative AI is a whole exam task statement.",
     "A documented hallucination example with grounding and human-review mitigations applied."),
 10:("Compare Bedrock, SageMaker JumpStart and managed services and classify ten scenarios.",
     "Choosing the right AWS AI layer for a task is a frequent exam decision.",
     "A decision table and ten business scenarios classified against it."),
 11:("Create an Amazon Q Business application answering questions from your own documents with citations.",
     "Amazon Q Business shows managed, grounded generative AI in action over enterprise content.",
     "A Q Business application connected to S3 documents, returning cited answers."),
 12:("Run one task at zero-shot, one-shot and few-shot and record how quality changes.",
     "Prompt engineering is the largest exam domain and shot count is its most basic lever.",
     "The same classification task at three shot levels with a quality comparison."),
 13:("Apply system prompts, roles, chain-of-thought and negative prompting, then package a template.",
     "Advanced prompting techniques and reusable templates are core to applying foundation models.",
     "A tested, reusable prompt template for a rule-heavy triage task."),
 14:("Probe your own triage application for prompt risks and build a five-layer defence.",
     "Prompt injection and misuse are named exam risks; layered defence is the expected mitigation.",
     "A threat model plus a five-layer defence covering prompt hardening, input validation, output filtering, Guardrails and least privilege."),
 15:("Build a RAG pipeline over your own documents with Knowledge Bases for Amazon Bedrock.",
     "RAG is the primary way to ground a model in private data and a heavily tested concept.",
     "A Bedrock knowledge base returning cited answers, proven against an ungrounded baseline."),
 16:("Tune chunk size, overlap, top-K and metadata filtering, and diagnose retrieval failures.",
     "Retrieval quality decides RAG quality; telling a retrieval failure from a generation failure is a practical skill.",
     "A tuned retrieval configuration and a diagnosis of a bad answer."),
 17:("Prepare a fine-tuning dataset and configure a Bedrock custom model job without submitting it.",
     "Knowing when to fine-tune versus prompt, RAG or continue pre-training is an exam decision with real cost consequences.",
     "A fine-tuning dataset, a configured custom-model job (not submitted) and a customisation decision table."),
 18:("Run a Bedrock automatic model evaluation and place metrics in a full evaluation strategy.",
     "Evaluating model performance across automatic metrics, human review and business metrics is a distinct exam task.",
     "An automatic evaluation job result interpreted alongside ROUGE, BLEU, BERTScore, benchmarks and business metrics."),
 19:("Create a Bedrock guardrail with content, denied-topic, word and PII filters and test it.",
     "Guardrails are the AWS control for responsible generative AI and are directly examinable.",
     "A configured Bedrock guardrail with a record of which policy blocks each test prompt."),
 20:("Frame a fairness question and compare pre- and post-training bias metrics with SageMaker Clarify.",
     "Detecting bias is a responsible-AI requirement the exam expects you to reason about.",
     "A fairness framing and a pre / post-training bias comparison from a Clarify job or guided report."),
 21:("Produce global and local SHAP explanations and decide when interpretability must win.",
     "Explainability underpins trust in AI and is a responsible-AI exam topic.",
     "A Clarify SHAP feature-attribution report with a performance-versus-interpretability decision."),
 22:("Create a SageMaker model card and distinguish it from Model Monitor and the Model Registry.",
     "Model cards document intended use and risk; they are the transparency artefacts the exam names.",
     "A completed SageMaker model card, compared with AWS AI Service Cards."),
 23:("Secure an AI workload with least-privilege IAM, customer managed KMS keys and VPC endpoints.",
     "Securing AI workloads and knowing the shared-responsibility boundary is a whole exam domain.",
     "A scoped IAM policy, a KMS-encrypted data bucket and private VPC-endpoint access to Bedrock."),
 24:("Use Amazon Macie to discover synthetic personal data in S3 and turn findings into controls.",
     "Keeping PII out of training data and prompts is a governance requirement Macie enforces.",
     "A Macie discovery job, its findings, and the data controls they drive."),
 25:("Inspect CloudTrail events, add AWS Config compliance rules and use the SageMaker Model Registry.",
     "Audit, compliance and model lineage are the governance controls that close the AI lifecycle.",
     "A CloudTrail audit trail, AWS Config compliance rules and a Model Registry approval workflow."),
}

GLOSSARY = [
 ("Artificial intelligence (AI)", "The broad field of building systems that perform tasks normally requiring human intelligence."),
 ("Machine learning (ML)", "A subset of AI in which a model learns patterns from data rather than following hand-written rules."),
 ("Deep learning", "ML using multi-layer neural networks; the basis of modern language and vision models."),
 ("Generative AI", "AI that produces new content — text, images, code — from a foundation model."),
 ("Foundation model (FM)", "A large model pre-trained on broad data that can be adapted to many downstream tasks."),
 ("Large language model (LLM)", "A foundation model trained on text that predicts and generates language."),
 ("Amazon Bedrock", "AWS managed service giving API access to foundation models, knowledge bases and guardrails."),
 ("Amazon SageMaker", "AWS service for building, training, tuning and deploying machine learning models."),
 ("Amazon Q Business", "A managed generative-AI assistant that answers questions grounded in your enterprise documents."),
 ("Token", "The unit of text a model reads and generates; token counts drive cost and the context window."),
 ("Embedding", "A numeric vector representing meaning, used to measure semantic similarity and power retrieval."),
 ("Vector store", "A database of embeddings queried by similarity; the retrieval backbone of RAG."),
 ("RAG", "Retrieval augmented generation — grounding a model's answer in documents retrieved at query time."),
 ("Prompt engineering", "Designing prompts — instructions, context and examples — to steer a model's output."),
 ("Zero/one/few-shot", "Prompting with no, one, or several worked examples of the task in the prompt."),
 ("Temperature / top-P", "Inference parameters that control randomness and the token sampling pool of the output."),
 ("Fine-tuning", "Customising a foundation model further on your own labelled data."),
 ("Hallucination", "A fluent but factually wrong model output; mitigated by grounding and human review."),
 ("Bedrock Guardrails", "Configurable content, denied-topic, word and PII filters applied to Bedrock model calls."),
 ("SageMaker Clarify", "A tool that measures bias metrics and produces SHAP feature-attribution explanations."),
 ("Model card", "A document recording a model's intended use, risk rating, training details and evaluation."),
 ("Responsible AI", "Building AI that is fair, explainable, transparent, safe and privacy-respecting."),
 ("Shared responsibility model", "AWS secures the cloud; the customer secures what they build and put in it."),
 ("IAM / KMS", "AWS Identity and Access Management for least-privilege access; Key Management Service for encryption keys."),
 ("Amazon Macie", "A service that discovers and reports sensitive data such as PII stored in Amazon S3."),
 ("AWS CloudTrail", "Records AWS API calls, providing the audit trail for who did what and when."),
]

# ---------------------------------------------------------------- lab reader
def read_lab(n):
    d = glob.glob(os.path.join(REPO, "labs", f"lab-{n:02d}-*"))[0]
    idx = json.load(open(os.path.join(d, "index.json"), encoding="utf-8"))
    title = re.sub(r"^Lab\s*\d+\s*[—–-]\s*", "", idx["title"]).strip()
    time = idx.get("time", "")
    labmd = open(os.path.join(d, "lab.md"), encoding="utf-8").read()
    m = re.search(r"\*\*Slide reference:\*\*.*?(\d+\s*[–—-]\s*\d+)", labmd)
    slides = m.group(1).replace(" ", "") if m else "—"
    steps = [re.sub(r"^Step\s*\d+\s*[:—–-]\s*", "", s["title"]).strip()
             for s in idx["details"]["steps"]]
    return title, time, slides, steps

# ---------------------------------------------------------------- rendering
def para(doc, text, bold=False, italic=False, size=11, color=DARK, after=4, style=None):
    p = doc.add_paragraph(style=style); p.paragraph_format.space_after = Pt(after)
    r = p.add_run(text); r.bold = bold; r.italic = italic
    r.font.size = Pt(size); r.font.color.rgb = color; r.font.name = "Arial"
    return p

def label_line(doc, label, rest):
    """A '<label>: <rest>' line with the label in bold."""
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(3)
    r = p.add_run(label + ": "); r.bold = True; r.font.size = Pt(11); r.font.name = "Arial"; r.font.color.rgb = DARK
    r2 = p.add_run(rest); r2.font.size = Pt(11); r2.font.name = "Arial"; r2.font.color.rgb = DARK
    return p

def bullets(doc, items):
    for it in items:
        p = doc.add_paragraph(style="List Bullet"); p.paragraph_format.space_after = Pt(3)
        r = p.add_run(it); r.font.size = Pt(11); r.font.name = "Arial"

def numbered(doc, items):
    for it in items:
        p = doc.add_paragraph(style="List Number"); p.paragraph_format.space_after = Pt(2)
        r = p.add_run(it); r.font.size = Pt(11); r.font.name = "Arial"

def glossary_table(doc, rows):
    t = doc.add_table(rows=0, cols=2); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hr = t.add_row().cells
    for i, htext in enumerate(["Term", "Meaning"]):
        hr[i].text = ""; r = hr[i].paragraphs[0].add_run(htext)
        r.bold = True; r.font.size = Pt(10); r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.name = "Arial"; _shade_cell(hr[i], "1F6FEB")
    for term, meaning in rows:
        cells = t.add_row().cells
        cells[0].text = ""; r = cells[0].paragraphs[0].add_run(term)
        r.bold = True; r.font.size = Pt(9.5); r.font.name = "Arial"; _shade_cell(cells[0], "EEF3FB")
        cells[1].text = ""; rr = cells[1].paragraphs[0].add_run(meaning)
        rr.font.size = Pt(9.5); rr.font.name = "Arial"
    doc.add_paragraph()

def main():
    doc = Document()
    style_headings(doc)
    doc.styles["Normal"].font.name = "Arial"; doc.styles["Normal"].font.size = Pt(11)

    add_cover_page(doc, "Learner Guide", TITLE, VERSION, course_code=CODE, org_logo=ORG_LOGO)
    add_version_control(doc, VERSIONS)
    add_toc(doc)

    # ---- Introduction
    doc.add_heading("Introduction", 1)
    para(doc, "This Learner Guide accompanies the course AWS Certified AI Practitioner Training "
              "(AIF-C01), conducted by Tertiary Infotech Academy Pte Ltd. It is your hands-on companion "
              "to the slide deck: the deck teaches the concepts, and this guide turns each concept into "
              "a short lab you complete in your own AWS account. The labs are grouped under the five "
              "official AIF-C01 exam domains and run in order, so the skills accumulate toward both the "
              "exam and the practical assessment. Use each lab's Objective and Goal to see what you are "
              "building and why it matters, follow the numbered Step-by-step, and keep every output as "
              "revision material. The Slides line in each lab points back to the deck for the underlying "
              "theory.")

    # ---- Course Learning Outcomes
    doc.add_heading("Course Learning Outcomes", 1)
    for lo in [
        "LO1 — Implement AI applications with Amazon Q Business and AWS AI models.",
        "LO2 — Deploy AWS AI Bedrock workflows according to plan and machine learning techniques.",
        "LO3 — Identify and report issues with AI applications, data and implementation procedures.",
        "LO4 — Maintain data interoperability during AI development per data-management principles.",
        "LO5 — Perform data cleaning techniques to optimise AWS foundation models.",
    ]:
        doc.add_paragraph(lo, style="List Bullet")

    # ---- Before You Start (condensed from labs/tools.md)
    doc.add_heading("Before You Start", 1)
    para(doc, "What you need", bold=True, after=2)
    bullets(doc, [
        "An AWS account — a free-tier account is enough: https://aws.amazon.com/free/",
        "The AWS CLI installed and configured (run aws configure, then aws sts get-caller-identity to confirm).",
        "The course slides and this Learner Guide.",
    ])
    para(doc, "Secure your account first", bold=True, after=2)
    bullets(doc, [
        "Enable MFA on the root user.",
        "Create an IAM admin user and stop using root for daily work.",
        "Set a billing alarm so runaway resources surface early.",
    ])
    para(doc, "Set your working Region and conveniences", bold=True, after=2)
    bullets(doc, [
        "Work in us-east-1 unless a lab says otherwise — AI/ML features appear there first.",
        "Set AWS_DEFAULT_REGION=us-east-1 and AWS_PAGER=\"\" for a smoother CLI experience.",
    ])
    para(doc, "Amazon Bedrock model access", bold=True, after=2)
    bullets(doc, [
        "Labs 06 onward need foundation model access — request it before class.",
        "In the Bedrock console, choose Model access, then request the models you need.",
        "Approval is not always instant, and available models vary by Region.",
    ])
    para(doc, "Cost awareness", bold=True, after=2)
    bullets(doc, [
        "Most labs stay within the free tier, but several create resources that bill until deleted.",
        "Billing resources appear in Labs 04, 05, 20, 21, 22 (SageMaker), 15, 16 (OpenSearch Serverless), "
        "11 (Amazon Q Business) and 24 (Macie). Do not provision throughput in Lab 17.",
        "Always complete each lab's Clean up step, and verify OpenSearch collections in every Region with "
        "aws opensearchserverless list-collections.",
    ])
    para(doc, "Verify your setup", bold=True, after=2)
    bullets(doc, [
        "aws sts get-caller-identity — returns your account and identity.",
        "aws bedrock list-foundation-models — returns the models available in your Region.",
    ])

    # ---- Five domain sections, one lab each as H2
    for dnum, dname, wt, labrange in DOMAINS:
        doc.add_heading(f"DOMAIN {dnum} — {dname}  ({wt}%)", 1)
        for n in labrange:
            title, time, slides, steps = read_lab(n)
            obj, goal, build = LG[n]
            mode = "Self-paced" if n in SELF_PACED else "Demo"
            doc.add_heading(f"Lab {n} — {title}  [{mode}]", 2)
            label_line(doc, "Objective", obj)
            label_line(doc, "Goal", goal)
            para(doc, "What you'll build", bold=True, after=1)
            para(doc, build, after=4)
            para(doc, f"At a glance — Domain {dnum}, Duration {time} min, Slides {slides}.",
                 italic=True, after=4)
            para(doc, "Step-by-step", bold=True, after=2)
            numbered(doc, steps)

    # ---- Quick Reference
    doc.add_heading("Quick Reference — AWS AI Services & Bedrock", 1)
    para(doc, "Key services used across the labs", bold=True, after=2)
    bullets(doc, [
        "Amazon Bedrock — API access to foundation models, plus knowledge bases (RAG), Guardrails and "
        "model evaluation. Used from Lab 06 onward.",
        "Amazon SageMaker — train, deploy and evaluate models; Ground Truth (labelling), Clarify (bias and "
        "SHAP explainability), model cards and the Model Registry.",
        "Amazon Q Business — managed generative-AI assistant grounded in your own documents (Lab 11).",
        "Managed AI services — Comprehend, Translate, Polly, Transcribe and Rekognition (Lab 03).",
        "Amazon Macie — discovers PII in Amazon S3 (Lab 24).",
        "AWS CloudTrail + AWS Config — audit trail and continuous compliance for AI API activity (Lab 25).",
    ])
    para(doc, "CLI commands that appear in the labs", bold=True, after=2)
    bullets(doc, [
        "aws sts get-caller-identity — confirm the identity and account you are using.",
        "aws bedrock list-foundation-models — list foundation models available in the Region.",
        "aws bedrock-runtime invoke-model — call a model for inference.",
        "aws bedrock-agent list-knowledge-bases / aws bedrock-agent-runtime retrieve — RAG knowledge bases.",
        "aws sagemaker list-endpoints / list-notebook-instances — find billing resources to clean up.",
        "aws opensearchserverless list-collections — find vector stores left behind by knowledge bases.",
        "aws qbusiness list-applications — list Amazon Q Business applications.",
        "aws macie2 get-macie-session — check Macie status.",
        "aws s3 cp / aws s3 rm / aws s3 rb — move data and delete buckets during cleanup.",
    ])

    # ---- Consolidating What You Learned
    doc.add_heading("Consolidating What You Learned", 1)
    para(doc, "The five exam domains map directly onto the five practical-assessment abilities. Check "
              "that you can do each unaided:")
    bullets(doc, [
        "A1 (Domain 1) — Explain AI, ML, deep learning and generative AI, classify data and learning "
        "types, and match a task to an AWS AI service or SageMaker.",
        "A2 (Domain 2) — Enable Bedrock, compare foundation models, tune inference parameters, and reason "
        "about tokens, embeddings, capabilities and limitations.",
        "A3 (Domain 3) — Engineer prompts, build and tune a RAG pipeline, decide on fine-tuning, and "
        "evaluate model performance.",
        "A4 (Domain 4) — Apply Guardrails, detect bias with Clarify, produce SHAP explanations, and "
        "document a model with a model card.",
        "A5 (Domain 5) — Secure an AI workload with IAM, KMS and VPC endpoints, protect data with Macie, "
        "and govern it with CloudTrail, Config and the Model Registry.",
    ])
    para(doc, "Re-work the labs from memory and then apply the same techniques to a workload in your own "
              "organisation — being able to produce the artefacts unaided is the best consolidation.")

    # ---- Glossary
    doc.add_heading("Glossary", 1)
    para(doc, "Key AIF-C01 terms used across the labs.")
    glossary_table(doc, GLOSSARY)

    add_page_numbers(doc, left_text=f"{TITLE} · {CODE}")
    enable_update_fields(doc)

    outdir = "Examples" if os.path.isdir(os.path.join(REPO, "Examples")) else "courseware"
    out = os.path.join(REPO, outdir, f"LG-{TITLE}.docx")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    doc.save(out)
    print("wrote", out)

if __name__ == "__main__":
    main()
