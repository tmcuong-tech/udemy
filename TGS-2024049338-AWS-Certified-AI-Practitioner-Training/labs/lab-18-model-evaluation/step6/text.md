# Step 6 — Clean up

This is the last lab of Domain 3, so clean up this lab **and** verify that nothing from Labs 15, 16 and 17 survived.

### 1. Stop any running evaluation job

An evaluation job bills for the inference it performs. If one is still running and you no longer need it:

```bash
aws bedrock list-evaluation-jobs --region us-east-1
```

```bash
aws bedrock stop-evaluation-job --job-identifier <JOB_NAME_OR_ARN> --region us-east-1
```

A **completed** job is a stored record, not a running resource — it is not accruing charges. You may keep completed jobs for reference; delete them from the console if you prefer a tidy account.

### 2. Remove the S3 data

Evaluation results can be sizeable if the dataset was large. Yours is small, but tidy up:

```bash
aws s3 rm s3://<your-bucket>/eval/ --recursive
aws s3 rm s3://<your-bucket>-eval-results --recursive
aws s3 rb s3://<your-bucket>-eval-results
```

**Keep a local copy of `eval-prompts.jsonl` and your reference answers.** A curated evaluation dataset is genuinely valuable — it is the asset that makes every future change measurable, and rebuilding one is tedious.

### 3. Delete the IAM role

If the console created a service role for the evaluation job, remove it from <https://console.aws.amazon.com/iam/>. It does not bill, but it holds S3 and Bedrock invoke permissions with no remaining purpose.

### 4. Domain 3 final sweep — do this properly

Run every command below, **in every Region you worked in during Labs 15 to 18**. Region-scoped resources in a Region you switched away from are invisible in the console and still billing.

```bash
aws bedrock-agent list-knowledge-bases --region us-east-1
aws opensearchserverless list-collections --region us-east-1
aws bedrock list-custom-models --region us-east-1
aws bedrock list-model-customization-jobs --region us-east-1
aws bedrock list-provisioned-model-throughputs --region us-east-1
aws bedrock list-evaluation-jobs --region us-east-1
```

The two that bill continuously and therefore matter most:

- **`list-collections`** — an OpenSearch Serverless collection from Lab 15 or 16 bills by the hour, whether or not you query it, and **survives deletion of the knowledge base**.
- **`list-provisioned-model-throughputs`** — provisioned throughput from Lab 17 bills for its duration and may carry a term commitment.

If either returns anything of yours, delete it now. Return to Lab 16 Step 6 or Lab 17 Step 6 for the exact commands.

### 5. Check the bill tomorrow

Open the Billing and Cost Management console **the following day** and review yesterday's spend by service. Domain 3 was the expensive part of this course; this is your confirmation that it is properly finished.

Look specifically for **Amazon OpenSearch Service** and **Amazon Bedrock** line items. An unexpected OpenSearch charge means a collection survived somewhere — check every Region.

### Final checklist

- [ ] No running evaluation jobs
- [ ] Evaluation dataset and results removed from S3, local copy of the dataset kept
- [ ] IAM service role deleted
- [ ] **No knowledge bases, in any Region**
- [ ] **No OpenSearch Serverless collections, in any Region**
- [ ] **No provisioned model throughputs, in any Region**
- [ ] No custom models or customisation jobs
- [ ] Billing check scheduled for tomorrow

**Checkpoint:** All six list commands return nothing of yours in every Region you used, your evaluation dataset is saved locally, and Domain 3 has left no billing resource behind.
