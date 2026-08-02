# Lab authoring spec — TGS-2024049338 AWS Certified AI Practitioner (AIF-C01)

Every lab MUST match the house format used by the SAA-C03 course repo
(`tertiarycourses/TGS-2024048315---AWS-Certified-Solutions-Architect-Associate-Training`).

Repo root: `c:\Users\ADMIN\Desktop\TGS-2024049338-AWS Certified AI Practitioner Training`
Labs live in: `labs/<folder-name>/`

---

## 1. Files per lab (ALL required)

```
labs/lab-NN-slug/
├── index.json          manifest
├── intro.md            title + description + "What you will do" bullets
├── lab.md              complete single-file lab (the primary readable artifact)
├── finish.md           "Well done!" + checklist + key takeaways + next lab
└── stepN/text.md       one folder per step, N = 1..last
```

The LAST step is always **Clean up**.

---

## 2. `index.json` — copy this schema exactly

```json
{
  "title": "Lab 06 — Amazon Bedrock Getting Started",
  "description": "One sentence, plain text, no markdown.",
  "difficulty": "beginner",
  "time": "30",
  "details": {
    "steps": [
      { "title": "Step 1: Enable model access", "text": "step1/text.md" },
      { "title": "Step 2: Explore the model catalogue", "text": "step2/text.md" },
      { "title": "Step 3: Clean up", "text": "step3/text.md" }
    ],
    "intro": { "text": "intro.md" },
    "finish": { "text": "finish.md" }
  },
  "backend": { "imageid": "ubuntu" }
}
```

- `difficulty`: `beginner` or `intermediate`
- `time`: minutes as a STRING, no unit
- Step titles use `Step N: Title` (colon). Section headings in markdown use `Step N — Title` (em dash).

---

## 3. `intro.md`

```markdown
# Lab NN — Title

One-sentence description (same as index.json description).

**What you will do:**
- Action-verb bullet
- Action-verb bullet
- (one per major step, excluding cleanup)
```

---

## 4. `lab.md` — the main artifact

```markdown
# Lab NN — Title

One-sentence description.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain N — <Official domain name> (NN%)
**Task statement:** N.N <Official task statement text>
**WSQ mapping:** LU<n> · Topic <n> <topic name> · <K codes> · <A code> · <LO code>
**Slide reference:** v11 deck slides <range>
**Estimated time:** NN minutes

**Learning objectives:**
- ...

---

## Step 1 — Title

<content>

---

## Step 2 — Title

...

---

## Step N — Clean up

<content>
```

Then close with:

```markdown
---

## Verification

- [ ] checklist item
- [ ] checklist item

## Discussion questions

1. ...
2. ...
3. ...

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.
```

---

## 5. `stepN/text.md`

The SAME content as that step's section in `lab.md`, but standalone:

```markdown
# Step N — Title

<identical body to the matching section in lab.md>
```

`lab.md` and the step files MUST NOT diverge.

---

## 6. `finish.md`

```markdown
# Well done!

You have completed Lab NN — Title:

✅ Step 1 title
✅ Step 2 title
...

**Key takeaways:**

- Exam-relevant point
- Exam-relevant point
- Exam-relevant point

**Next:** Lab NN+1 — Title
```

For the final lab (25) use: `**Next:** You have completed all 25 labs — review the exam guide and attempt the practice exams.`

---

## 7. ACCURACY RULES — these matter more than volume

1. **Never invent URLs.** Permitted: `https://aws.amazon.com/free/`,
   `https://console.aws.amazon.com/<service>/`, `https://skillbuilder.aws/`,
   `https://aws.amazon.com/certification/certified-ai-practitioner/`.
   Do NOT fabricate Skill Builder deep links, lab ARNs or blog URLs.
2. **Never invent pricing, quotas, model version strings or Region-availability claims.**
   Say "check the Model access page for models available in your Region".
3. **Console UI drifts.** Write "in the left navigation, choose **X**" rather than
   asserting pixel-exact layouts. If unsure of an exact label, describe the capability.
4. **CLI blocks are encouraged** where a real command exists (`aws bedrock ...`,
   `aws sagemaker ...`). Do not invent flags — omit the CLI block if unsure.
5. **Cost warnings are mandatory** wherever a resource bills continuously —
   SageMaker notebook instances, Studio apps, inference endpoints, OpenSearch
   Serverless collections, Kendra indexes. Call these out prominently in Clean up.
6. Conceptual objectives become **guided walkthroughs**; label any illustrative
   figures explicitly as teaching data, never as real measurements.
7. Every lab must be genuinely completable by a beginner in its stated time.

---

## 8. WSQ mapping reference (approved codes — use verbatim)

| LU | Topics | K codes | A code | LO |
|---|---|---|---|---|
| LU1 Introduction to Generative AI | T1 Generative AI for Executives; T2 Amazon Q Business Getting Started | K1, K2 | A1 | LO1 |
| LU2 AWS Bedrock and Machine Learning | T3 Amazon Bedrock Getting Started; T4 Fundamentals of ML and AI | K4, K6 | A2 | LO2 |
| LU3 Applications of AI and Responsible AI | T5 Exploring AI Use Cases; T6 Responsible AI Practices | K7, K8 | A3 | LO3 |
| LU4 Applications of AI and Responsible AI | T7 Developing ML Solutions; T8 Developing GenAI Solutions; T9 Essentials of Prompt Engineering | K3, K5, K9 | A4 | LO4 |
| LU5 Optimization and Security of AI Solutions | T10 Optimizing Foundation Models; T11 Security, Compliance and Governance | K10, K11 | A5 | LO5 |

## 9. Deck slide ranges (from build/slide_map.json — do not hand-type others)

| Task | Slides | Task | Slides |
|---|---|---|---|
| 1.1 | 25–51 | 3.2 | 210–235 |
| 1.2 | 52–83 | 3.3 | 236–247 |
| 1.3 | 84–135 | 3.4 | 248–271 |
| 2.1 | 137–164 | 4.1 | 273–284 |
| 2.2 | 165–172 | 4.2 | 285–297 |
| 2.3 | 173–182 | 5.1 | 299–333 |
| 3.1 | 184–209 | 5.2 | 334–374 |

---

## 10. The 25-lab catalogue

### Domain 1 — Fundamentals of AI and ML (20%) — 5 labs
| # | Folder | Title | Task | Slides | LU/K/A/LO | Time |
|---|---|---|---|---|---|---|
| 01 | `lab-01-ai-ml-terminology` | AI, ML and Deep Learning Terminology | 1.1 | 25–51 | LU2 · T4 · K4 · A2 · LO2 | 30 |
| 02 | `lab-02-data-types-labeling` | Data Types and Labelling for ML | 1.1 | 25–51 | LU2 · T4 · K4 · A2 · LO2 | 35 |
| 03 | `lab-03-aws-ai-services-tour` | AWS Managed AI Services Tour | 1.2 | 52–83 | LU3 · T5 · K7 · A3 · LO3 | 40 |
| 04 | `lab-04-sagemaker-train-deploy` | Train and Deploy a Model with SageMaker | 1.3 | 84–135 | LU4 · T7 · K3 · A4 · LO4 | 45 |
| 05 | `lab-05-ml-pipeline-data-prep` | The ML Pipeline and Data Preparation | 1.3 | 84–135 | LU4 · T7 · K3 · A4 · LO4 | 40 |

### Domain 2 — Fundamentals of Generative AI (24%) — 6 labs
| # | Folder | Title | Task | Slides | LU/K/A/LO | Time |
|---|---|---|---|---|---|---|
| 06 | `lab-06-bedrock-getting-started` | Amazon Bedrock Getting Started | 2.1 | 137–164 | LU2 · T3 · K6 · A2 · LO2 | 30 |
| 07 | `lab-07-fm-comparison-parameters` | Comparing Foundation Models and Inference Parameters | 2.1 | 137–164 | LU2 · T3 · K6 · A2 · LO2 | 35 |
| 08 | `lab-08-tokens-embeddings` | Tokens, Embeddings and Vector Representations | 2.1 | 137–164 | LU2 · T3 · K6 · A2 · LO2 | 35 |
| 09 | `lab-09-genai-capabilities-limits` | Generative AI Capabilities and Limitations | 2.2 | 165–172 | LU3 · T5 · K7 · A3 · LO3 | 30 |
| 10 | `lab-10-bedrock-vs-sagemaker` | Choosing Bedrock, SageMaker JumpStart or a Managed Service | 2.3 | 173–182 | LU2 · T3 · K6 · A2 · LO2 | 35 |
| 11 | `lab-11-amazon-q-business` | Amazon Q Business Getting Started | 2.3 | 173–182 | LU1 · T2 · K2 · A1 · LO1 | 40 |

### Domain 3 — Applications of Foundation Models (28%) — 7 labs
| # | Folder | Title | Task | Slides | LU/K/A/LO | Time |
|---|---|---|---|---|---|---|
| 12 | `lab-12-prompt-engineering-basics` | Prompt Engineering Basics — Zero-Shot and Few-Shot | 3.2 | 210–235 | LU4 · T9 · K9 · A4 · LO4 | 35 |
| 13 | `lab-13-advanced-prompting` | Advanced Prompting and Prompt Templates | 3.2 | 210–235 | LU4 · T9 · K9 · A4 · LO4 | 40 |
| 14 | `lab-14-prompt-risks-injection` | Prompt Misuse, Injection and Defences | 3.2 | 210–235 | LU4 · T9 · K9 · A4 · LO4 | 35 |
| 15 | `lab-15-rag-knowledge-bases` | RAG with Knowledge Bases for Amazon Bedrock | 3.1 | 184–209 | LU4 · T8 · K5 · A4 · LO4 | 45 |
| 16 | `lab-16-vector-stores-retrieval` | Vector Stores and Retrieval Quality | 3.1 | 184–209 | LU4 · T8 · K5 · A4 · LO4 | 40 |
| 17 | `lab-17-fine-tuning-customization` | Fine-Tuning and Model Customisation | 3.3 | 236–247 | LU5 · T10 · K10 · A5 · LO5 | 40 |
| 18 | `lab-18-model-evaluation` | Evaluating Foundation Model Performance | 3.4 | 248–271 | LU5 · T10 · K10 · A5 · LO5 | 40 |

### Domain 4 — Guidelines for Responsible AI (14%) — 4 labs
| # | Folder | Title | Task | Slides | LU/K/A/LO | Time |
|---|---|---|---|---|---|---|
| 19 | `lab-19-bedrock-guardrails` | Amazon Bedrock Guardrails | 4.1 | 273–284 | LU3 · T6 · K8 · A3 · LO3 | 40 |
| 20 | `lab-20-bias-detection-clarify` | Bias Detection with SageMaker Clarify | 4.1 | 273–284 | LU3 · T6 · K8 · A3 · LO3 | 40 |
| 21 | `lab-21-explainability` | Explainability and Feature Attribution | 4.2 | 285–297 | LU3 · T6 · K8 · A3 · LO3 | 35 |
| 22 | `lab-22-model-cards-transparency` | Model Cards and Transparency | 4.2 | 285–297 | LU3 · T6 · K8 · A3 · LO3 | 30 |

### Domain 5 — Security, Compliance and Governance (14%) — 3 labs
| # | Folder | Title | Task | Slides | LU/K/A/LO | Time |
|---|---|---|---|---|---|---|
| 23 | `lab-23-securing-ai-iam-kms` | Securing AI Workloads with IAM and KMS | 5.1 | 299–333 | LU5 · T11 · K11 · A5 · LO5 | 40 |
| 24 | `lab-24-macie-data-protection` | Data Protection with Amazon Macie | 5.1 | 299–333 | LU5 · T11 · K11 · A5 · LO5 | 35 |
| 25 | `lab-25-cloudtrail-governance` | Governance, Audit and Model Lineage | 5.2 | 334–374 | LU5 · T11 · K11 · A5 · LO5 | 35 |

---

## 11. Official domain names (use verbatim)

- Domain 1 — Fundamentals of AI and ML (20%)
- Domain 2 — Fundamentals of Generative AI (24%)
- Domain 3 — Applications of Foundation Models (28%)
- Domain 4 — Guidelines for Responsible AI (14%)
- Domain 5 — Security, Compliance, and Governance for AI Solutions (14%)
