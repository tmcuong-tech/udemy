# AWS Certified AI Practitioner (AIF-C01) Lab Index

Twenty-five hands-on labs aligned to the five official exam domains of the [AWS Certified AI Practitioner (AIF-C01)](https://aws.amazon.com/certification/certified-ai-practitioner/) certification.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/))
**Default region:** `us-east-1` unless a lab states otherwise
**Additional practice:** [AWS Skill Builder](https://skillbuilder.aws/)

> **Always complete the cleanup step.** Several services in these labs bill continuously from the moment they are created, whether or not you use them — SageMaker inference endpoints, notebook instances and Studio applications, OpenSearch Serverless collections, and Amazon Kendra indexes are the worst offenders. Closing a browser tab does not stop them. Amazon Macie discovery jobs are charged by the volume of data inspected and cannot be un-run. Finish every lab with its Clean up step, then check Cost Explorer the following day.

## Domain 1 — Fundamentals of AI and ML (20%)

| Lab | Title | Key skills | Time |
|---|---|---|---|
| [01](lab-01-ai-ml-terminology/) | AI, ML and Deep Learning Terminology | ai vs ml vs deep learning, supervised and unsupervised learning, inference, model terminology | 30 min |
| [02](lab-02-data-types-labeling/) | Data Types and Labelling for ML | structured and unstructured data, labelled vs unlabelled data, training and validation splits, data quality | 35 min |
| [03](lab-03-aws-ai-services-tour/) | AWS Managed AI Services Tour | rekognition, comprehend, transcribe, polly, textract, service selection by use case | 40 min |
| [04](lab-04-sagemaker-train-deploy/) | Train and Deploy a Model with SageMaker | training jobs, execution roles, model artifacts, endpoint deployment, endpoint cleanup | 45 min |
| [05](lab-05-ml-pipeline-data-prep/) | The ML Pipeline and Data Preparation | ml lifecycle stages, feature engineering, data cleaning, exploratory data analysis, data wrangler | 40 min |

## Domain 2 — Fundamentals of Generative AI (24%)

| Lab | Title | Key skills | Time |
|---|---|---|---|
| [06](lab-06-bedrock-getting-started/) | Amazon Bedrock Getting Started | model access, bedrock console, playground, invoking a foundation model, region availability | 30 min |
| [07](lab-07-fm-comparison-parameters/) | Comparing Foundation Models and Inference Parameters | temperature, top-p, max tokens, stop sequences, model comparison, output determinism | 35 min |
| [08](lab-08-tokens-embeddings/) | Tokens, Embeddings and Vector Representations | tokenisation, context windows, embedding models, vector similarity, semantic search | 35 min |
| [09](lab-09-genai-capabilities-limits/) | Generative AI Capabilities and Limitations | hallucination, non-determinism, knowledge cutoffs, cost and latency trade-offs, suitability assessment | 30 min |
| [10](lab-10-bedrock-vs-sagemaker/) | Choosing Bedrock, SageMaker JumpStart or a Managed Service | service selection, managed vs custom trade-offs, jumpstart, build vs buy decisions | 35 min |
| [11](lab-11-amazon-q-business/) | Amazon Q Business Getting Started | q business applications, data source connectors, enterprise search, user access controls | 40 min |

## Domain 3 — Applications of Foundation Models (28%)

| Lab | Title | Key skills | Time |
|---|---|---|---|
| [12](lab-12-prompt-engineering-basics/) | Prompt Engineering Basics — Zero-Shot and Few-Shot | zero-shot prompting, few-shot examples, instruction clarity, output formatting | 35 min |
| [13](lab-13-advanced-prompting/) | Advanced Prompting and Prompt Templates | chain-of-thought, role prompting, prompt templates, negative prompting, reusable patterns | 40 min |
| [14](lab-14-prompt-risks-injection/) | Prompt Misuse, Injection and Defences | prompt injection, jailbreaking, prompt leaking, input validation, defensive system prompts | 35 min |
| [15](lab-15-rag-knowledge-bases/) | RAG with Knowledge Bases for Amazon Bedrock | retrieval augmented generation, knowledge bases, data sources, chunking, grounded responses | 45 min |
| [16](lab-16-vector-stores-retrieval/) | Vector Stores and Retrieval Quality | vector databases, opensearch serverless, chunk size tuning, retrieval evaluation, citations | 40 min |
| [17](lab-17-fine-tuning-customization/) | Fine-Tuning and Model Customisation | fine-tuning vs rag, continued pre-training, training data format, customisation cost trade-offs | 40 min |
| [18](lab-18-model-evaluation/) | Evaluating Foundation Model Performance | model evaluation jobs, automatic and human evaluation, benchmark datasets, business metrics | 40 min |

## Domain 4 — Guidelines for Responsible AI (14%)

| Lab | Title | Key skills | Time |
|---|---|---|---|
| [19](lab-19-bedrock-guardrails/) | Amazon Bedrock Guardrails | content filters, denied topics, word filters, pii masking, contextual grounding checks | 40 min |
| [20](lab-20-bias-detection-clarify/) | Bias Detection with SageMaker Clarify | pre-training and post-training bias metrics, facets, fairness assessment, bias reports | 40 min |
| [21](lab-21-explainability/) | Explainability and Feature Attribution | feature attribution, shap values, interpretable vs black-box models, explaining predictions | 35 min |
| [22](lab-22-model-cards-transparency/) | Model Cards and Transparency | sagemaker model cards, intended use documentation, risk ratings, transparency reporting | 30 min |

## Domain 5 — Security, Compliance, and Governance for AI Solutions (14%)

| Lab | Title | Key skills | Time |
|---|---|---|---|
| [23](lab-23-securing-ai-iam-kms/) | Securing AI Workloads with IAM and KMS | shared responsibility model, least-privilege iam policies, kms customer managed keys, encryption at rest and in transit, vpc endpoints | 40 min |
| [24](lab-24-macie-data-protection/) | Data Protection with Amazon Macie | sensitive data discovery, managed and custom data identifiers, macie findings, pii controls for training data and prompts | 35 min |
| [25](lab-25-cloudtrail-governance/) | Governance, Audit and Model Lineage | cloudtrail event inspection, model invocation logging, aws config compliance rules, model lineage, model registry approval | 35 min |

## Lab folder contents

Every lab folder follows the same structure:

```
labs/lab-NN-slug/
├── index.json          manifest: title, description, difficulty, time, step list
├── intro.md            title, one-sentence description, "What you will do" bullets
├── lab.md              the complete lab in a single file — the primary readable artifact
├── finish.md           completion checklist, key takeaways, pointer to the next lab
├── step1/text.md       step 1, standalone
├── step2/text.md       step 2, standalone
└── stepN/text.md       ... the last step is always Clean up
```

- **`index.json`** is the manifest consumed by the lab platform. `time` is minutes as a string with no unit; `difficulty` is `beginner` or `intermediate`. Step titles use the form `Step N: Title`.
- **`intro.md`** opens the lab with its title, the one-sentence description that also appears in `index.json`, and a "What you will do" bullet for each major step excluding cleanup.
- **`lab.md`** contains the full lab: a header block with the exam domain, task statement, WSQ mapping, slide reference and learning objectives; every step as a `## Step N — Title` section; then a Verification checklist and Discussion questions.
- **`stepN/text.md`** holds exactly the same body as the matching section of `lab.md`, formatted to stand alone. The two must never diverge.
- **`finish.md`** confirms what was completed, lists the exam-relevant key takeaways, and points to the next lab.
- **The final step of every lab is Clean up**, listing the specific commands needed to remove every billable resource the lab created.

Read `lab.md` if you are working through a lab in one sitting. The `stepN` files exist for platforms that present one step per screen.

## WSQ mapping

Labs map to the WSQ Learning Units, Knowledge (K) and Ability (A) statements of TSC `ICT-TEM-3034-1.1` — *Artificial Intelligence Application in Product Development*.

| Lab | Domain / Task | LU | Topic | K | A | LO |
|---|---|---|---|---|---|---|
| 01 | D1 / 1.1 | LU2 | Topic 4 Fundamentals of ML and AI | K4 | A2 | LO2 |
| 02 | D1 / 1.1 | LU2 | Topic 4 Fundamentals of ML and AI | K4 | A2 | LO2 |
| 03 | D1 / 1.2 | LU3 | Topic 5 Exploring AI Use Cases | K7 | A3 | LO3 |
| 04 | D1 / 1.3 | LU4 | Topic 7 Developing ML Solutions | K3 | A4 | LO4 |
| 05 | D1 / 1.3 | LU4 | Topic 7 Developing ML Solutions | K3 | A4 | LO4 |
| 06 | D2 / 2.1 | LU2 | Topic 3 Amazon Bedrock Getting Started | K6 | A2 | LO2 |
| 07 | D2 / 2.1 | LU2 | Topic 3 Amazon Bedrock Getting Started | K6 | A2 | LO2 |
| 08 | D2 / 2.1 | LU2 | Topic 3 Amazon Bedrock Getting Started | K6 | A2 | LO2 |
| 09 | D2 / 2.2 | LU3 | Topic 5 Exploring AI Use Cases | K7 | A3 | LO3 |
| 10 | D2 / 2.3 | LU2 | Topic 3 Amazon Bedrock Getting Started | K6 | A2 | LO2 |
| 11 | D2 / 2.3 | LU1 | Topic 2 Amazon Q Business Getting Started | K2 | A1 | LO1 |
| 12 | D3 / 3.2 | LU4 | Topic 9 Essentials of Prompt Engineering | K9 | A4 | LO4 |
| 13 | D3 / 3.2 | LU4 | Topic 9 Essentials of Prompt Engineering | K9 | A4 | LO4 |
| 14 | D3 / 3.2 | LU4 | Topic 9 Essentials of Prompt Engineering | K9 | A4 | LO4 |
| 15 | D3 / 3.1 | LU4 | Topic 8 Developing GenAI Solutions | K5 | A4 | LO4 |
| 16 | D3 / 3.1 | LU4 | Topic 8 Developing GenAI Solutions | K5 | A4 | LO4 |
| 17 | D3 / 3.3 | LU5 | Topic 10 Optimizing Foundation Models | K10 | A5 | LO5 |
| 18 | D3 / 3.4 | LU5 | Topic 10 Optimizing Foundation Models | K10 | A5 | LO5 |
| 19 | D4 / 4.1 | LU3 | Topic 6 Responsible AI Practices | K8 | A3 | LO3 |
| 20 | D4 / 4.1 | LU3 | Topic 6 Responsible AI Practices | K8 | A3 | LO3 |
| 21 | D4 / 4.2 | LU3 | Topic 6 Responsible AI Practices | K8 | A3 | LO3 |
| 22 | D4 / 4.2 | LU3 | Topic 6 Responsible AI Practices | K8 | A3 | LO3 |
| 23 | D5 / 5.1 | LU5 | Topic 11 Security, Compliance and Governance | K11 | A5 | LO5 |
| 24 | D5 / 5.1 | LU5 | Topic 11 Security, Compliance and Governance | K11 | A5 | LO5 |
| 25 | D5 / 5.2 | LU5 | Topic 11 Security, Compliance and Governance | K11 | A5 | LO5 |

**Learning units:**

- **LU1** — Introduction to Generative AI
- **LU2** — AWS Bedrock and Machine Learning
- **LU3** — Applications of AI and Responsible AI
- **LU4** — Applications of AI and Responsible AI
- **LU5** — Optimization and Security of AI Solutions

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.
