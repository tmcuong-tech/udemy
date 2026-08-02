# Step 5 — Model lineage and deployment approval with SageMaker Model Registry

Governance of an AI system is not only about API calls and resource configuration. It also has to answer questions about the model itself:

- Which exact dataset produced this model?
- Which version is in production right now?
- **Who approved it, and when?**
- If it starts behaving badly, what do we roll back to?

The SageMaker Model Registry exists to answer these.

## Data and model lineage

**Lineage** is the recorded chain from raw data to deployed model:

```
raw dataset (S3 object, versioned)
      │
      ▼
processing job  ──► curated dataset
      │
      ▼
training job  ──► model artifact + hyperparameters + container image
      │
      ▼
registered model package (versioned)
      │
      ▼
endpoint (production)
```

Without lineage, "which data trained the model that made this decision?" is unanswerable — and under regimes that grant a right to an explanation, or when a customer requests erasure, that is a serious position to be in. SageMaker's lineage tracking builds this graph automatically from the jobs you run, and Model Cards (Lab 22) are where the human-readable summary lives.

## Create a model package group

A **model package group** is a container for successive versions of one logical model. Every retraining produces a new **model package version** inside it.

```bash
aws sagemaker create-model-package-group \
  --model-package-group-name ai-lab-governance-demo \
  --model-package-group-description "Governance and approval walkthrough" \
  --region us-east-1
```

```bash
aws sagemaker list-model-package-groups --region us-east-1 \
  --query 'ModelPackageGroupSummaryList[].{Name:ModelPackageGroupName,Created:CreationTime}' \
  --output table
```

Creating a group costs nothing — you are creating metadata, not compute.

In the console, open `https://console.aws.amazon.com/sagemaker/` and find the model registry in the left navigation. Open your group. It is empty, because registering a version requires a trained model artifact from a real training job (Lab 04). Inspect the structure rather than populating it.

## The approval workflow

This is the governance mechanism, and it is what the exam asks about. Every registered model version carries an **approval status**:

| Status | Meaning |
|---|---|
| `PendingManualApproval` | Registered, evaluated, **not** cleared for production |
| `Approved` | A human with the right permission signed off |
| `Rejected` | Explicitly blocked from deployment |

The pattern:

1. A training pipeline registers a new version with status `PendingManualApproval`. Automation can produce a model; it cannot approve one.
2. A reviewer inspects the evaluation metrics, the bias report from SageMaker Clarify (Lab 20) and the model card (Lab 22).
3. If satisfied, they change the status to `Approved`:

   ```bash
   aws sagemaker update-model-package \
     --model-package-arn <model-package-arn> \
     --model-approval-status Approved \
     --region us-east-1
   ```

4. A deployment pipeline is configured to deploy only `Approved` versions, so the approval is a genuine gate rather than a note in a ticket.

Two governance properties fall out of this:

- **Separation of duties.** `sagemaker:UpdateModelPackage` can be granted to a distinct role, so the person who trains a model is not the person who approves it. That separation is a control auditors specifically look for.
- **Auditability.** The approval is an API call, so **CloudTrail records who approved which model version and when.** Go back to Event history and filter by event source `sagemaker.amazonaws.com` — your `CreateModelPackageGroup` call is there now, with your identity and timestamp on it.

That closes the loop of this entire lab: the registry provides the gate, and CloudTrail provides the proof that the gate was used.

## Rollback

Because every version is retained with its artifact and metadata, rolling back a bad model is a matter of pointing an endpoint configuration at an earlier approved version. Compare that with an environment where models are overwritten in an S3 prefix and nobody is certain which file is live. **Version control for models is an availability control as much as a governance one.**

## The governance stack, assembled

You have now met the whole of Domain 5. Fix the mapping:

| Governance question | Service |
|---|---|
| Who may call this model? | IAM (Lab 23) |
| Is the data encrypted, with keys we control? | KMS (Lab 23) |
| Does traffic stay off the public internet? | VPC endpoints (Lab 23) |
| Is there sensitive data in our S3 buckets? | Amazon Macie (Lab 24) |
| Is PII blocked at inference time? | Bedrock Guardrails (Lab 19) |
| Who called the API, and when? | **CloudTrail** |
| What did they actually prompt the model with? | **Bedrock model invocation logging** |
| Are our resources configured compliantly? | **AWS Config** |
| Which data produced this model? | **SageMaker lineage tracking** |
| Which version is approved for production? | **SageMaker Model Registry** |
| Where do we get AWS's own audit reports? | **AWS Artifact** |

If you can reproduce that table from memory, you are ready for this domain.
