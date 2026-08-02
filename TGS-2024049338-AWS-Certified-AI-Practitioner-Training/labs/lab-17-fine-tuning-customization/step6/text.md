# Step 6 — Clean up

If you followed the lab, **you created almost nothing** — which was the point. Verify that, then remove the small amount that does exist.

### 1. Verify nothing expensive was created

Run all three. **All three must return empty.**

```bash
aws bedrock list-model-customization-jobs --region us-east-1
aws bedrock list-custom-models --region us-east-1
aws bedrock list-provisioned-model-throughputs --region us-east-1
```

Check **every Region you opened the console in**, since these are Region-scoped and it is easy to have switched Regions while looking for customisation support.

### 2. If a training job is running — stop it now

If `list-model-customization-jobs` shows a job in progress, it is accruing training charges. Stop it:

```bash
aws bedrock stop-model-customization-job \
  --job-identifier <JOB_NAME_OR_ARN> \
  --region us-east-1
```

Or use the console: open the custom models area, select the job, and stop it. Then re-run the list command to confirm.

### 3. If a custom model exists — delete it

A custom model is a stored artefact. Delete it in the console, or:

```bash
aws bedrock delete-custom-model --model-identifier <MODEL_NAME> --region us-east-1
```

### 4. If provisioned throughput exists — this is urgent

**This is the expensive one and it bills continuously.**

```bash
aws bedrock list-provisioned-model-throughputs --region us-east-1
```

If anything is listed, delete it immediately:

```bash
aws bedrock delete-provisioned-model-throughput \
  --provisioned-model-id <PROVISIONED_MODEL_ID> \
  --region us-east-1
```

**If it was purchased with a commitment term, deletion may not stop the committed charges.** If this has happened in your own account, check the Billing console to understand your exposure and contact AWS Support. Do not assume that deleting the resource ends the obligation.

Re-run the list command and confirm it is empty.

### 5. Remove the training data

The JSONL files are tiny, but tidy up:

```bash
aws s3 rm s3://<your-bucket>/finetune/ --recursive
```

If the bucket has no other purpose, remove it entirely:

```bash
aws s3 rb s3://<your-bucket>
```

**If your training data contained anything sensitive**, deleting it from S3 is the right step here. Note the broader point from Step 2 though: had you actually trained on it, the data would be reflected in the model's weights and deleting the source file would not remove it. That asymmetry — RAG context is transient, training data is permanent — is a governance distinction worth carrying forward.

### 6. Remove the IAM role

If the console created a service role while you walked the configuration, delete it from <https://console.aws.amazon.com/iam/>. It does not bill, but it has S3 and Bedrock permissions with no remaining purpose.

### 7. Confirm the knowledge base from Labs 15 and 16 is gone

The most common source of an unexpected bill at this point in the course is a leftover vector store:

```bash
aws bedrock-agent list-knowledge-bases --region us-east-1
aws opensearchserverless list-collections --region us-east-1
```

Both should be empty, in every Region you used. If not, return to Lab 16 Step 6.

### Final checklist

- [ ] No model customisation jobs, in any Region
- [ ] No custom models, in any Region
- [ ] **No provisioned model throughputs, in any Region**
- [ ] Training and validation JSONL removed from S3
- [ ] IAM service role deleted
- [ ] No knowledge bases and no OpenSearch Serverless collections remaining

**Checkpoint:** All three Bedrock list commands return empty in every Region you used, and the Labs 15–16 knowledge base and vector store are confirmed gone.
