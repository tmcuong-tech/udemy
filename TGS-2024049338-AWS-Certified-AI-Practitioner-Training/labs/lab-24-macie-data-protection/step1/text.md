# Step 1 — Why PII must never reach training data or prompts

Amazon Macie is a managed data security service that uses machine learning and pattern matching to discover sensitive data in Amazon S3. Before you run it, be clear about the problem it solves for an AI workload.

## The three failure modes

**1. PII in training data becomes PII in the model.**
A model trained on records containing names, email addresses and account numbers can reproduce them at inference time. This is *memorisation*, and it is not a bug you can patch — the information is distributed through the weights. Once a model has memorised a customer's phone number, the only reliable remedies are retraining from clean data or blocking the output. Neither is cheap. Data minimisation before training is the only control that actually scales.

**2. PII in prompts leaves your control boundary.**
Every prompt sent to a foundation model is data leaving the application. Amazon Bedrock does not use your prompts to train the base models, and prompts are encrypted in transit — but they may still be written to your own model invocation logs, to CloudWatch, to an application database, or to a third-party observability tool. Under GDPR or Singapore's PDPA, a customer's medical detail pasted into a prompt and then written to a log file is a processing activity you must be able to account for.

**3. PII in a RAG knowledge base is retrievable by anyone who can query it.**
This is the one teams miss most often. If you index an S3 bucket of internal documents into a knowledge base and one spreadsheet contains employee salaries, then any user who can ask the chatbot a question can potentially retrieve them. The vector store has no concept of "this user may not see this row" unless you build it. **Filter at ingestion, not at generation.**

## Where Macie fits

Macie answers a question you usually cannot answer by inspection: *what sensitive data is actually sitting in these buckets?* On a bucket holding tens of thousands of files that no one has audited, this is not a question a human can answer manually.

Typical placement in an AI pipeline:

```
Raw data lands in S3
        │
        ▼
  [ Macie discovery job ]  ← you are here
        │
        ├── findings: PII detected → quarantine, redact, or exclude
        │
        ▼
Curated training / knowledge base bucket
        │
        ▼
Fine-tuning job  or  Knowledge base ingestion
```

Macie is a **detective** control — it tells you what is there. It does not block, redact or delete anything. Pair it with:

- **Preventive controls:** Amazon Comprehend PII detection and redaction to strip entities from text before storage; S3 bucket policies and Block Public Access; the KMS encryption from Lab 23.
- **Runtime controls:** Amazon Bedrock Guardrails, which can block or mask PII in prompts *and* responses (Lab 19).

A common exam trap: a question describes wanting to *find* sensitive data across many S3 buckets and offers both Macie and Comprehend. Macie discovers **in S3 at rest**; Comprehend detects entities **in text you pass to it**. Match the verb and the location.

## Safety rule for this lab

> **You will create only synthetic data.** Every name, email address and identifier you upload in Step 2 is invented for this exercise — no real person's data appears anywhere in this lab, and **you must not substitute real customer, employee or personal data for any of it.** Uploading real PII to a practice account to "make the test more realistic" would itself be the exact governance failure this lab teaches you to prevent.
