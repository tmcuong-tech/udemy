# Step 5 — Read the findings and turn them into data controls

## Open the findings

When the job status reaches `COMPLETE`, choose **Findings** in the left navigation. Or from the CLI:

```bash
aws macie2 list-findings --region us-east-1
```

```bash
aws macie2 get-findings --region us-east-1 --finding-ids <finding-id>
```

Select a finding and work through its structure. Every Macie finding tells you:

- **Finding type** — sensitive data findings use types beginning `SensitiveData:S3Object/...` (for example a personal-information subtype). A separate family, `Policy:IAMUser/...`, covers bucket configuration problems such as public access or disabled encryption, and those are generated without any discovery job.
- **Severity** — Low, Medium or High, derived from the type and quantity of sensitive data found.
- **Resource affected** — the exact bucket, object key, size and encryption status.
- **Sensitive data detected** — the categories found, the count of occurrences per category, and the **location** of each occurrence: line and column for CSV, offset ranges for text.

That last field is the operationally useful one. It gives you `customer_export.csv`, column 2, rows 2 through 9 — precise enough to script a redaction against.

## What you should see, and what you might not

`customer_export.csv` and `support_transcript.txt` should produce findings; `product_catalogue.csv` should produce none. Expect email addresses and your custom `EMP-ZZ-` identifier to be detected reliably.

**If a category you expected is missing, that is a finding in itself, not a failure of the lab.** Macie's managed identifiers are tuned against false positives, and detection for personal names and some identifier types depends on surrounding context — a column header, nearby keywords, plausible formatting. In a small synthetic file that context is thin.

Sit with the implication rather than moving past it: **a detective control that reports nothing does not mean there is nothing there.** Macie reduces uncertainty; it does not eliminate it. Anyone who treats a clean Macie report as proof of a PII-free dataset has misunderstood the tool. This nuance appears in exam questions about the limits of automated discovery.

## Trace each finding to a control

Take each finding and decide what actually happens next. This is the reasoning the exam tests.

| Finding | Why it matters for AI | Control to apply |
|---|---|---|
| Email addresses in `customer_export.csv` | A fine-tuned model can memorise and reproduce them | Exclude the column, or redact with Amazon Comprehend PII detection, before the file reaches the training bucket |
| Personal data in `support_transcript.txt` | Prose files get indexed into RAG knowledge bases without review; anyone who can query the bot can retrieve them | Keep the file out of the knowledge base data source prefix entirely; filter at ingestion |
| Custom `EMP-ZZ-` references | Internal identifiers are re-identification keys — harmless alone, linkable to a person when joined with another dataset | Tokenise or hash before storage; treat as PII in your data classification |
| No findings in `product_catalogue.csv` | Confirms the control discriminates rather than flagging everything | Safe to promote to the curated bucket |

Notice that not one of these remediations is performed by Macie. Macie produced the list; **you** decide and implement. Every exam question that describes Macie *blocking*, *redacting* or *deleting* data is describing something Macie does not do.

## Wire findings into a workflow

Macie automatically publishes findings to **Amazon EventBridge** and to **AWS Security Hub**. That is what makes it operational rather than a report you read once:

- An EventBridge rule matching Macie findings can trigger a Lambda function that moves the offending object to a quarantine bucket, or blocks a pipeline stage.
- Security Hub aggregates Macie findings alongside GuardDuty, Inspector and Config, giving one compliance view.
- Findings can be exported to an S3 bucket for long-term retention — worth knowing, because **findings are retained in Macie for a limited period (90 days)**. If you need audit evidence beyond that window you must configure the export yourself.

The gap between a *detection* and a *prevention* is the automation you build. Macie tells you the data is there; EventBridge plus Lambda is what stops it reaching your training job.

## Connect back to the AI pipeline

Position the full set of controls you now know:

- **Before storage:** Amazon Comprehend detects and redacts PII entities in text.
- **At rest in S3:** Macie discovers what is actually there; KMS encryption (Lab 23) protects it; IAM restricts who reads it.
- **At inference:** Amazon Bedrock Guardrails (Lab 19) blocks or masks PII in both prompts and model responses.
- **After the fact:** CloudTrail records who accessed what (Lab 25).

No single one of these is sufficient. A question offering only one control for an end-to-end data-protection requirement is usually testing whether you notice that layered controls are the correct answer.
