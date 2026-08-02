# Step 3 — Enable Amazon Macie

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
