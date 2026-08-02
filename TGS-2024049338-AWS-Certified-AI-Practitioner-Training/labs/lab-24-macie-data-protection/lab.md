# Lab 24 — Data Protection with Amazon Macie

Use Amazon Macie to discover synthetic personal data in an S3 bucket, read the findings and connect them to the controls that keep PII out of training data and prompts.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 5 — Security, Compliance, and Governance for AI Solutions (14%)
**Task statement:** 5.1 Explain methods to secure AI systems.
**WSQ mapping:** LU5 · Topic 11 Security, Compliance and Governance · K11 · A5 · LO5
**Slide reference:** v11 deck slides 299–333
**Estimated time:** 35 minutes

> **COST WARNING:** Amazon Macie sensitive data discovery jobs are **charged by the volume of data inspected**, and a job that has run cannot be un-run. This lab scans three files totalling a few kilobytes. Never point a discovery job at a bucket whose size you have not checked first. Macie also charges a monthly per-bucket monitoring fee while it is enabled — you will disable it in Step 6.

> **SYNTHETIC DATA ONLY:** every name, email address, phone number and identifier used in this lab is invented for teaching. Email addresses use the reserved `example.com` domain and phone numbers use the reserved `555-01xx` fiction range. **No real personal data appears anywhere in this lab, and you must not substitute any.**

**Learning objectives:**
- Explain the three ways personal data leaks through an AI system: memorisation in a trained model, exposure through prompts and logs, and retrieval from a RAG knowledge base
- Distinguish Amazon Macie from Amazon Comprehend by what each inspects and where
- Enable Macie and use its no-cost bucket inventory to assess scope before incurring discovery charges
- Create a custom data identifier for an organisation-specific format and scope a discovery job to control cost
- Interpret a Macie finding, including severity, affected resource and occurrence locations
- Map each finding to a preventive, detective, runtime or corrective control

---

## Step 1 — Why PII must never reach training data or prompts

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

---

## Step 2 — Create a bucket and upload synthetic sample data

> **SYNTHETIC DATA ONLY.** Every value below is fabricated for teaching. The names are invented, the email addresses use the reserved `example.com` domain which cannot receive mail, and the identifiers are made-up strings. **Do not replace any of it with real personal data.**

## Create the bucket

```bash
aws s3api create-bucket \
  --bucket macie-lab-data-<your-initials>-<random-number> \
  --region us-east-1

aws s3api put-public-access-block \
  --bucket macie-lab-data-<your-initials>-<random-number> \
  --public-access-block-configuration \
    "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

Use the same bucket name throughout. Substitute it wherever you see `<bucket>` below.

## File 1 — a "customer export" that should never have been used for training

Create `customer_export.csv`:

```csv
record_id,full_name,email,phone,employee_ref,notes
1001,Marigold Thistlewick,marigold.thistlewick@example.com,+1-555-0142,EMP-ZZ-4417,Requested account closure
1002,Barnaby Quillfeather,barnaby.quillfeather@example.com,+1-555-0177,EMP-ZZ-8802,Escalated billing dispute
1003,Persimmon Vandergrift,persimmon.vandergrift@example.com,+1-555-0198,EMP-ZZ-1250,Upgraded to premium tier
1004,Cornelius Pemberwick,cornelius.pemberwick@example.com,+1-555-0121,EMP-ZZ-6634,Reported login failure
1005,Ottoline Frostwhistle,ottoline.frostwhistle@example.com,+1-555-0165,EMP-ZZ-3391,Requested data export
1006,Fitzwilliam Grimsdale,fitzwilliam.grimsdale@example.com,+1-555-0189,EMP-ZZ-7728,Cancelled subscription
1007,Hyacinth Ravensworth,hyacinth.ravensworth@example.com,+1-555-0133,EMP-ZZ-2065,Password reset request
1008,Ignatius Bellweather,ignatius.bellweather@example.com,+1-555-0154,EMP-ZZ-9143,Feedback on new feature
```

The names are deliberately absurd — that is the point. If any of them matched a real person it would be coincidence, and the `555-01xx` phone range is reserved for fiction. `example.com` is reserved by RFC 2606 and can never be registered.

## File 2 — a "support transcript" of the kind that ends up in a RAG knowledge base

Create `support_transcript.txt`:

```
Ticket ZZ-88213 — Support transcript (SYNTHETIC TEST DATA)

Agent: Thank you for contacting support. May I have your name?
Customer: Marigold Thistlewick.
Agent: And a contact email for the case?
Customer: marigold.thistlewick@example.com
Agent: I can see the account. The best callback number we have is
       +1-555-0142 — is that still correct?
Customer: Yes. My internal reference is EMP-ZZ-4417 if that helps.
Agent: Noted. I have escalated the case and you will hear back within
       two business days.
```

This file is the realistic threat. A CSV in a data lake is at least obviously structured data that someone might review. A support transcript looks like harmless prose, gets indexed into a knowledge base without a second thought, and quietly makes every detail in it retrievable through a chatbot.

## File 3 — a clean control file

Create `product_catalogue.csv`:

```csv
sku,product_name,category,unit_price,in_stock
SKU-4410,Ceramic Mug,Kitchenware,12.50,true
SKU-4411,Steel Kettle,Kitchenware,44.00,true
SKU-4412,Linen Napkin Set,Kitchenware,18.75,false
SKU-4413,Bamboo Cutting Board,Kitchenware,29.90,true
```

Including a file with no personal data lets you confirm Macie is discriminating rather than flagging everything. A detection tool that fires on every object is as useless as one that fires on none.

## Upload

```bash
aws s3 cp customer_export.csv    s3://<bucket>/raw/
aws s3 cp support_transcript.txt s3://<bucket>/raw/
aws s3 cp product_catalogue.csv  s3://<bucket>/raw/
aws s3 ls s3://<bucket>/raw/
```

All three objects should be listed. Keep the total tiny — the next step explains why data volume is the thing you are billed on.

---

## Step 3 — Enable Amazon Macie

> **COST WARNING — read before you click.**
> Amazon Macie bills on two separate dimensions:
> 1. **Automated S3 bucket inventory and evaluation**, charged per bucket monitored per month.
> 2. **Sensitive data discovery jobs, charged by the volume of data inspected.** This is the one that surprises people. Pointing a discovery job at a production data lake containing terabytes can produce a very large bill from a single click, and the job cannot be un-run.
>
> Macie offers a free trial period for new accounts, but **do not rely on it** — check the Amazon Macie pricing page and your account's trial status in the Macie console before running any job.
>
> **In this lab you will scan three tiny files, a few kilobytes in total.** Never point a discovery job at a bucket whose size you have not checked. Before scanning any real bucket, look at its size in the S3 console or Macie's own bucket inventory first.

## Enable the service

In the console, open `https://console.aws.amazon.com/macie/` and choose the option to enable Macie. Macie is a **regional** service — enabling it in `us-east-1` does not enable it elsewhere, and it can only scan buckets in the Region where it is enabled.

From the CLI:

```bash
aws macie2 enable-macie --region us-east-1
```

Confirm:

```bash
aws macie2 get-macie-session --region us-east-1
```

The response shows `"status": "ENABLED"` and the `findingPublishingFrequency`.

## Look at the automated bucket inventory first

Once enabled, Macie immediately builds an inventory of every S3 bucket in the Region — **at no per-gigabyte charge, because it is reading metadata, not object contents.** In the left navigation choose the S3 buckets view.

For each bucket you get:

- Total object count and total size — check this *before* scheduling a job
- Whether the bucket is publicly accessible
- Whether it is encrypted, and with which type of key
- Whether it is shared with other AWS accounts
- Object counts by file type, and how many objects Macie *can* classify

This inventory alone is valuable. "Which of my buckets are unencrypted and publicly readable?" is a question most organisations cannot answer quickly, and answering it costs nothing beyond the per-bucket monitoring charge.

Find your `macie-lab-data-...` bucket in the list and note its size. It should be a few kilobytes. That is the number that determines what the next step costs.

## Understand automated discovery versus a discovery job

Macie provides two different mechanisms and the exam may distinguish them:

| | Automated sensitive data discovery | Sensitive data discovery job |
|---|---|---|
| Scope | Continuously samples objects across buckets | Buckets and prefixes you select |
| Control over what is scanned | Low — Macie chooses representative samples | Full — you pick buckets, prefixes, file types |
| Schedule | Ongoing, automatic | One-time or on a schedule you set |
| Cost profile | Designed to be lower via sampling | Charged on the full volume inspected |
| Best for | Broad, continuous visibility | Targeted audits, compliance evidence |

For an AI pipeline, the practical pattern is: leave automated discovery on for broad coverage, and run a targeted **job** against a specific prefix immediately before that data is used for training or knowledge base ingestion.

## Managed data identifiers

Macie ships with managed data identifiers — built-in detection logic for common sensitive data types, including names, email addresses, phone numbers, mailing addresses, credentials such as private keys, and country-specific identifiers like national ID and tax numbers.

Two things to understand about how they work:

- Detection is **not simple regex**. Many identifiers require supporting context — a nearby keyword, a plausible format, or a checksum. A nine-digit number sitting alone in a column may not be reported as a national ID, because Macie is deliberately tuned to limit false positives.
- You can add **custom data identifiers** with your own regular expression, optional proximity keywords and a character-count limit. This is how you detect organisation-specific formats — internal employee references, policy numbers, case IDs. The `EMP-ZZ-####` pattern in your sample data is exactly this kind of value, and you will use a custom identifier for it in Step 4.

---

## Step 4 — Create a custom data identifier and run a discovery job

## Create a custom data identifier for the internal reference format

Managed identifiers will not know what `EMP-ZZ-4417` means — that is an internal format specific to this fictional organisation. Custom data identifiers exist for exactly this.

In the Macie console, in the left navigation find **Custom data identifiers** and create a new one:

- **Name:** `internal-employee-reference`
- **Regular expression:** `EMP-ZZ-[0-9]{4}`
- **Keywords:** (optional) `employee_ref`, `internal reference`
- **Ignore words:** leave empty
- **Maximum match distance:** leave at the default

Macie provides a test box on the creation page. Paste `Customer reference EMP-ZZ-4417 was recorded` into it and confirm the identifier matches before saving. Testing before running is a habit worth forming — a discovery job that runs with a broken regex costs the same as one that works.

The keyword and match-distance settings control *precision*: requiring a keyword within a set number of characters of the match suppresses coincidental hits. Over-broad custom identifiers are the main cause of finding fatigue, where so many false positives accumulate that the team stops reading findings at all.

## Create the discovery job

> **Check the bucket size one more time.** You are about to authorise a job charged by data volume. Your bucket should be a few kilobytes.

In the left navigation choose **Jobs**, then create a job:

1. **Select S3 buckets** — choose your `macie-lab-data-...` bucket only. Do not select all buckets.
2. **Refine the scope** — this page is where cost is controlled. Set:
   - **Sampling depth:** 100% (safe here because the data is tiny; on a large bucket, reducing this reduces both coverage and cost proportionally)
   - **Includes:** add an S3 object prefix condition for `raw/`
   - You can also exclude by file extension, object size or last-modified date
3. **Job type** — choose **one-time job**. A scheduled job re-runs and re-bills on every run.
4. **Managed data identifiers** — keep the recommended set.
5. **Custom data identifiers** — select `internal-employee-reference`.
6. **Name** — `macie-lab-discovery-job`.
7. Review the summary, which shows the estimated volume to be scanned, and submit.

The job moves through `RUNNING` to `COMPLETE`. On three small files this takes a few minutes.

Monitor from the CLI:

```bash
aws macie2 list-classification-jobs --region us-east-1 \
  --query 'items[].{Name:name,Id:jobId,Status:jobStatus}' --output table
```

Note the `jobId` — you need it for cleanup.

## While it runs: what "sensitive data discovery" actually costs you elsewhere

Consider what would have happened without this step. The `raw/` prefix would have been used directly as a fine-tuning dataset or ingested into a knowledge base. Nobody would have opened `support_transcript.txt` — it is one file among thousands.

The cost of *not* scanning is not a bill; it is a model or a retrieval index that contains personal data you cannot enumerate, cannot delete on request, and cannot prove you controlled. When a data subject exercises a right to erasure, "we do not know whether their data is in the model" is not an answer a regulator accepts.

Running a discovery job before ingestion converts an unbounded, unknowable risk into a list of file paths you can act on. That is the whole argument for this control, and it is worth being able to state in one sentence.

---

## Step 5 — Read the findings and turn them into data controls

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

---

## Step 6 — Clean up

> **Disable Macie.** While Macie is enabled it charges a monthly fee per S3 bucket it monitors, prorated, whether or not you run any job. Leaving it on across a whole account with many buckets is the most likely way to be surprised by a bill from this lab. Discovery jobs themselves are charged once, on the volume already scanned — you cannot un-run a job, but you can stop future ones.

## 1. Cancel the discovery job

A one-time job that has already completed will not run again, but cancel it explicitly so nothing is left in a schedulable state:

```bash
aws macie2 update-classification-job \
  --job-id <job-id> \
  --job-status CANCELLED \
  --region us-east-1
```

Verify no job is in a running or paused state:

```bash
aws macie2 list-classification-jobs --region us-east-1 \
  --query 'items[].{Name:name,Status:jobStatus}' --output table
```

## 2. Delete the custom data identifier

```bash
aws macie2 list-custom-data-identifiers --region us-east-1
aws macie2 delete-custom-data-identifier \
  --id <custom-data-identifier-id> \
  --region us-east-1
```

## 3. Empty and delete the S3 bucket

Delete this bucket even though its contents are synthetic. A bucket named after a data-protection lab, containing files that *look* like a customer export, is exactly the kind of artefact that confuses a future audit of your own account.

```bash
aws s3 rm s3://macie-lab-data-<your-initials>-<random-number>/ --recursive
aws s3api delete-bucket --bucket macie-lab-data-<your-initials>-<random-number>
```

Delete the local copies too:

```bash
rm customer_export.csv support_transcript.txt product_catalogue.csv
```

## 4. Disable Macie

```bash
aws macie2 disable-macie --region us-east-1
```

Understand what this does: disabling Macie **permanently deletes all of your findings and job records** in that Region. If you needed any of it as audit evidence you would have had to export it to S3 first (Step 5). For this lab there is nothing worth keeping, but on a real account confirm exports are in place before you disable.

Confirm the session is gone:

```bash
aws macie2 get-macie-session --region us-east-1
```

This should now return a resource-not-found error. That error is the success condition.

## 5. Check the other Regions

Macie is regional, and it is easy to enable it in a second Region by accident while clicking through the console. If you switched Regions at any point during the lab, check there too:

```bash
aws macie2 get-macie-session --region <other-region>
```

## 6. Verify the spend

Open the **Billing and Cost Management** console the next day and filter Cost Explorer to Amazon Macie. Given three files of a few kilobytes and a session lasting under an hour, the charge should be negligible or zero under a free trial — but confirming it rather than assuming it is the habit that matters.

---

## Verification

- [ ] I can state in one sentence why PII in a fine-tuning dataset is harder to remediate than PII in a database
- [ ] All three sample files are uploaded, and I confirmed every value in them is synthetic
- [ ] I checked my bucket's size in the Macie bucket inventory **before** creating the discovery job
- [ ] My custom data identifier matched the test string in the console before I saved it
- [ ] The discovery job reached `COMPLETE` and was scoped to one bucket and one prefix
- [ ] I opened a finding and located the affected object key and the occurrence locations within it
- [ ] `product_catalogue.csv` produced no findings, confirming the control discriminates
- [ ] The job is cancelled, the custom identifier and bucket are deleted, and `get-macie-session` returns not-found

## Discussion questions

1. A colleague argues that scanning is unnecessary because "the bucket is encrypted and private." Explain why encryption and access control do not address the problem Macie solves.
2. Your discovery job returns no findings on a 400 GB knowledge base source bucket. Give three reasons this result might be misleading, and say what you would do before declaring the data clean.
3. You must detect an internal policy-number format across a data lake. Compare a Macie custom data identifier with a scheduled Lambda function that greps the objects. Which would you choose, and what does each cost you?
4. Design an EventBridge-driven workflow that stops PII reaching a Bedrock knowledge base. At which point in the ingestion pipeline does it intervene, and what happens to the offending object?
5. A data subject requests erasure of their personal data. Your model was fine-tuned six months ago on a dataset that included them. Walk through what you can and cannot do, and explain which control in this lab would have made the request answerable.

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.
