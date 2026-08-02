# TGS-2024049338 — AWS Certified AI Practitioner Training

> **Course:** WSQ — AWS Certified AI Practitioner Training  
> **Course Code:** TGS-2024049338  
> **Certification:** [AWS Certified AI Practitioner (AIF-C01)](https://aws.amazon.com/certification/certified-ai-practitioner/)

These are the official hands-on lab exercises for the WSQ AWS Certified AI Practitioner Training course delivered by [**Tertiary Infotech Academy Pte Ltd**](https://www.tertiarycourses.com.sg/).

A complete set of **25 step-by-step labs** aligned to the five official **AIF-C01 exam domains**. Every lab runs in your own AWS account and includes a cleanup step.

---

## How to use

1. Create a free tier AWS account: https://aws.amazon.com/free/
2. Secure it before you start — enable MFA on root, create an IAM admin user, set a billing alarm.
3. Install and configure the AWS CLI (see [labs/tools.md](labs/tools.md)):
   ```bash
   aws configure
   aws sts get-caller-identity
   ```
4. Set the working region:
   ```bash
   export AWS_DEFAULT_REGION=us-east-1
   export AWS_PAGER=""
   export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
   ```
5. Request Amazon Bedrock model access before Lab 06 — approval is not always instant.
6. Work through the labs in order — each domain builds on the previous one.

> ⚠️ **Always complete the cleanup step.** SageMaker notebook instances, Studio apps and inference endpoints, OpenSearch Serverless collections, Kendra indexes and Amazon Q Business applications bill continuously whether or not you use them. Deleting a Bedrock knowledge base does **not** reliably delete the vector store beneath it — check every Region you used.

---

## Lab catalogue

### Domain 1 — Fundamentals of AI and ML (20%)

| Lab | Topic | What you practise |
|-----|-------|-------------------|
| [01](labs/lab-01-ai-ml-terminology/) | AI, ML and Deep Learning Terminology | define artificial intelligence, machine learning, deep learning and generative ai, and explain how they nest inside one another, classify a described workload as supervised, unsupervised or reinforcement learning, and name the common sub-types of each, use the terms algorithm, training, model, inference, parameter and hyperparameter precisely |
| [02](labs/lab-02-data-types-labeling/) | Data Types and Labelling for ML | classify a dataset as structured, semi-structured or unstructured, and as tabular, time-series, image or text, store and organise ml datasets in amazon s3 using key prefixes, explain why only labelled data can train a supervised model, and what makes labelling costly and error-prone |
| [03](labs/lab-03-aws-ai-services-tour/) | AWS Managed AI Services Tour | use amazon comprehend to extract sentiment, entities, key phrases, language and pii from free text, perform neural machine translation with amazon translate and describe how custom terminology controls brand terms, synthesise speech with amazon polly and control pronunciation and pacing with ssml |
| [04](labs/lab-04-sagemaker-train-deploy/) | Train and Deploy a Model with SageMaker | explain the sagemaker cost model and identify which resources bill continuously versus per job, create a notebook instance and describe the role of the sagemaker execution role, prepare tabular data into train, validation and test splits in the format a built-in algorithm requires |
| [05](labs/lab-05-ml-pipeline-data-prep/) | The ML Pipeline and Data Preparation | translate a business goal into an ml question, with distinct model metrics and business metrics, describe the stages of the ml lifecycle and name the aws service that supports each, perform the checks that make up exploratory data analysis, and detect target leakage |

### Domain 2 — Fundamentals of Generative AI (24%)

| Lab | Topic | What you practise |
|-----|-------|-------------------|
| [06](labs/lab-06-bedrock-getting-started/) | Amazon Bedrock Getting Started | enable access to foundation models in the amazon bedrock console for a chosen region, explain why model availability is specific to an aws account and region, navigate the model catalogue and identify a model's provider, modality and model id |
| [07](labs/lab-07-fm-comparison-parameters/) | Comparing Foundation Models and Inference Parameters | compare the output of two or more foundation models given one identical prompt, explain why a fair comparison holds the prompt, the parameters and the conversation history constant, describe what temperature does to the model's next-token probability distribution |
| [08](labs/lab-08-tokens-embeddings/) | Tokens, Embeddings and Vector Representations | explain the difference between words and tokens, and why the two counts diverge, describe how token counts drive both cost and the context window, and keep the two distinct, generate an embedding vector from a bedrock embedding model |
| [09](labs/lab-09-genai-capabilities-limits/) | Generative AI Capabilities and Limitations | demonstrate summarisation, generation, translation and code capabilities in the bedrock playground, identify the common property that predicts whether a generative ai task will succeed, deliberately produce a hallucination and record it verbatim with evidence that it is false |
| [10](labs/lab-10-bedrock-vs-sagemaker/) | Choosing Bedrock, SageMaker JumpStart or a Managed Service | distinguish managed ai services, amazon bedrock and amazon sagemaker by what you manage and what you control, run the same task through a managed ai service and a foundation model and compare the outputs, identify a task only a foundation model can perform, and one only sagemaker can host |
| [11](labs/lab-11-amazon-q-business/) | Amazon Q Business Getting Started | explain what amazon q business is and how it differs from amazon bedrock, create a q business application and connect an amazon s3 data source, run a sync and interpret the sync history |

### Domain 3 — Applications of Foundation Models (28%)

| Lab | Topic | What you practise |
|-----|-------|-------------------|
| [12](labs/lab-12-prompt-engineering-basics/) | Prompt Engineering Basics — Zero-Shot and Few-Shot | identify the four components of a prompt — instructions, context, input data and output indicator — in any prompt you are shown, write a zero-shot prompt and explain when zero-shot is sufficient, write one-shot and few-shot prompts, and explain that in-context learning does not change model weights |
| [13](labs/lab-13-advanced-prompting/) | Advanced Prompting and Prompt Templates | distinguish a system prompt from a user prompt, and explain why one is trusted and the other is not, use role assignment to constrain tone, depth and framing in very few tokens, apply chain-of-thought prompting to a multi-rule task and state its cost, latency and reliability trade-offs |
| [14](labs/lab-14-prompt-risks-injection/) | Prompt Misuse, Injection and Defences | explain why a foundation model cannot separate instructions from data, and why that is the root cause of prompt injection, define prompt injection, jailbreaking, prompt leaking, poisoning and hijacking, and tell them apart, distinguish direct from indirect injection and explain why indirect injection is the more serious risk |
| [15](labs/lab-15-rag-knowledge-bases/) | RAG with Knowledge Bases for Amazon Bedrock | describe the rag ingestion pipeline — chunk, embed, index — and the query pipeline — embed, retrieve top-k, generate, explain that rag changes the prompt, not the model's weights, create a knowledge base over an s3 data source, choose an embedding model, and sync it |
| [16](labs/lab-16-vector-stores-retrieval/) | Vector Stores and Retrieval Quality | measure retrieval quality separately from answer correctness, and use that split to locate a fault, explain the chunk size trade-off and what overlap fixes, with concrete examples, compare fixed-size, hierarchical and semantic chunking, and say why hierarchical resolves the trade-off rather than compromising |
| [17](labs/lab-17-fine-tuning-customization/) | Fine-Tuning and Model Customisation | compare prompt engineering, rag, fine-tuning and continued pre-training on weights, data, labelling, time, cost and citations, state the supervised versus unsupervised distinction between fine-tuning and continued pre-training, prepare a valid jsonl training and validation dataset and apply the data quality rules that decide success |
| [18](labs/lab-18-model-evaluation/) | Evaluating Foundation Model Performance | explain why generative output resists the accuracy metrics used for classification, state for rouge, bleu, bertscore, perplexity and f1 the task each belongs to, its orientation, and its limitation, explain why no automatic metric detects hallucination |

### Domain 4 — Guidelines for Responsible AI (14%)

| Lab | Topic | What you practise |
|-----|-------|-------------------|
| [19](labs/lab-19-bedrock-guardrails/) | Amazon Bedrock Guardrails | configure an amazon bedrock guardrail with content filters, denied topics, word filters and sensitive-information filters, explain what each policy group controls and which failure mode it covers, distinguish mask from block behaviour for pii and justify the choice per entity type |
| [20](labs/lab-20-bias-detection-clarify/) | Bias Detection with SageMaker Clarify | express a fairness question as facet, facet value, label and positive label value, explain class imbalance and difference in proportions of labels and the phase they belong to, distinguish the post-training bias metric families and explain why error-rate gaps matter most |
| [21](labs/lab-21-explainability/) | Explainability and Feature Attribution | distinguish global from local explanations and match each to its audience and purpose, explain shap feature attribution, including why contributions are signed and additive, explain why the shap baseline determines what an explanation means, and why it must be documented |
| [22](labs/lab-22-model-cards-transparency/) | Model Cards and Transparency | create a sagemaker model card and complete intended use, out-of-scope uses, owner and review date, assign a risk rating based on consequence and autonomy, and justify it with evidence, record training provenance, time period, population coverage and known data gaps |

### Domain 5 — Security, Compliance and Governance for AI Solutions (14%)

| Lab | Topic | What you practise |
|-----|-------|-------------------|
| [23](labs/lab-23-securing-ai-iam-kms/) | Securing AI Workloads with IAM and KMS | locate the boundary of the aws shared responsibility model for amazon bedrock and amazon sagemaker, write an iam policy that grants only the required actions on only the required bedrock and sagemaker resources, choose correctly between aws owned, aws managed and customer managed kms keys, and explain what key rotation does |
| [24](labs/lab-24-macie-data-protection/) | Data Protection with Amazon Macie | explain the three ways personal data leaks through an ai system: memorisation in a trained model, exposure through prompts and logs, and retrieval from a rag knowledge base, distinguish amazon macie from amazon comprehend by what each inspects and where, enable macie and use its no-cost bucket inventory to assess scope before incurring discovery charges |
| [25](labs/lab-25-cloudtrail-governance/) | Governance, Audit and Model Lineage | identify aws cloudtrail as the service that records who called a bedrock or sagemaker api, which action, and when, distinguish cloudtrail from amazon bedrock model invocation logging, cloudwatch and aws config by the question each answers, read a cloudtrail event record and extract the identity, action, timestamp, source ip and outcome |

---

## Courseware

| Artifact | File |
|---|---|
| Master trainer slides (374 slides) | [`courseware/`](courseware/) — `.pptx` + `.pdf` |
| Learner Guide | [`courseware/`](courseware/) — `.docx` + `.pdf` |
| Lesson Plan | [`courseware/`](courseware/) — `.docx` + `.pdf` |
| Full lab walkthrough | [LEARNER GUIDE.md](LEARNER%20GUIDE.md) |
| Lab index | [labs/README.md](labs/README.md) |

> Assessment instruments (WA-SAQ and Case Study) and their answer keys are **not** in this repository. They are trainer-only and live in the course Google Drive folder.

---

## Exam domain weighting

| Domain | Weight | Labs |
|---|---|---|
| 1 — Fundamentals of AI and ML | 20% | 01–05 |
| 2 — Fundamentals of Generative AI | 24% | 06–11 |
| 3 — Applications of Foundation Models | 28% | 12–18 |
| 4 — Guidelines for Responsible AI | 14% | 19–22 |
| 5 — Security, Compliance and Governance for AI Solutions | 14% | 23–25 |

---

## Repository structure

```
TGS-2024049338---AWS-Certified-AI-Practitioner-Training/
├── LEARNER GUIDE.md      full walkthrough of every lab
├── README.md
├── build/                generators for the deck, guide, lesson plan and labs
├── courseware/           slides, Learner Guide, Lesson Plan (docx + pdf)
└── labs/                 25 hands-on labs, one folder each
    ├── README.md         lab index with WSQ mapping
    ├── tools.md          AWS CLI setup
    └── lab-NN-slug/
        ├── index.json    manifest: title, time, steps
        ├── intro.md      what you will do
        ├── lab.md        the full lab
        ├── finish.md     recap and key takeaways
        └── stepN/text.md one file per step
```

---

## License

This material is provided for **educational use** as part of the WSQ course **TGS-2024049338**. © Tertiary Infotech Academy Pte Ltd. All rights reserved.
