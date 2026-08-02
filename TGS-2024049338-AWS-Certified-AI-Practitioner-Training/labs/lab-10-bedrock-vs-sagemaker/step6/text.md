# Step 6 — Clean up

This lab was deliberately designed so that **browsing is all that was required**. If you followed it as written, nothing billable was created. Verify that rather than assuming it.

## 1. SageMaker — the expensive one

If you deployed a JumpStart model despite the warnings, **delete the endpoint now**. It bills per instance-hour continuously, whether or not it receives a single request.

```bash
# Endpoints — these bill per instance-hour until deleted
aws sagemaker list-endpoints --region us-east-1

# Delete any endpoint from this lab
aws sagemaker delete-endpoint --region us-east-1 --endpoint-name <name>

# The endpoint config and model are free to keep, but tidy them anyway
aws sagemaker list-endpoint-configs --region us-east-1
aws sagemaker delete-endpoint-config --region us-east-1 --endpoint-config-name <name>
```

> **Deleting the model or the endpoint config does not stop the charge. Only deleting the *endpoint* does.** This is the single most common and most expensive cleanup mistake in AWS AI training.

Also check for anything that bills by the hour whether idle or not:

```bash
# Notebook instances — bill while "InService", even with no notebook open
aws sagemaker list-notebook-instances --region us-east-1
```

If you opened **SageMaker Studio**, shut down the running applications from within Studio (**File → Shut Down**, or the running terminals and kernels panel). A Studio application keeps billing after you close the browser tab — closing the tab is not shutting it down.

## 2. Bedrock

On-demand inference is serverless — nothing to delete. Confirm you created nothing that is not:

```bash
aws bedrock list-provisioned-model-throughputs --region us-east-1
aws bedrock list-custom-models --region us-east-1
```

Both should be empty. Close the playground tab.

## 3. Comprehend

Real-time analysis in the console creates no persistent resource. If you went further and started a **custom classifier**, a **custom entity recogniser**, an **endpoint**, or an **analysis job**, delete them — custom Comprehend endpoints bill continuously in the same way SageMaker endpoints do.

## 4. Keep your work

The **decision table** from Step 4 and the **ten classified scenarios** from Step 5 are the deliverables of this lab and are among the most exam-relevant notes in Domain 2. Keep them.

## 5. Set a budget

If this is your own account and you have not already, create an **AWS Budget** or billing alert. This lab's cleanup list is exactly the category of resource that surfaces as a surprise at month end rather than at the moment you create it.

**Checkpoint:** `list-endpoints` and `list-notebook-instances` return nothing from this lab, no Studio application is running, Bedrock shows no provisioned throughput or custom models, and your tables are saved.
