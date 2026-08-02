# Step 4 — Create a custom data identifier and run a discovery job

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
