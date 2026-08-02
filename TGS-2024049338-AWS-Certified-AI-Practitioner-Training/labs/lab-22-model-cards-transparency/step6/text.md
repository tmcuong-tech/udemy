# Step 6 — Clean up

> ### IMPORTANT — SageMaker bills continuously
> **SageMaker notebook instances, Studio applications and spaces, and inference endpoints
> are charged for every hour they exist, whether or not you are using them.** They do
> **not** stop by themselves. Model cards themselves are metadata and cost essentially
> nothing — but if you opened Studio to reach the console, or attached a model with a live
> endpoint, those are billing right now.

### 6.1 Delete the model card

1. Go to the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/).
2. In the left navigation, under the governance section, choose **Model cards**.
3. Select `aif-lab22-loan-approval-card`.
4. Choose **Delete** and confirm.

Or from the CLI:

```bash
aws sagemaker list-model-cards --region us-east-1
aws sagemaker delete-model-card --model-card-name aif-lab22-loan-approval-card --region us-east-1
```

> **In production you would not do this.** A model card is a governance record with an audit
> trail, and deleting it destroys the evidence of what was known and decided. You are
> deleting it here only because this is a training account.

### 6.2 Shut down anything that bills

Check the left navigation and clear:

- [ ] **Studio apps and spaces** — shut down running apps, spaces and kernel sessions.
      **Closing the browser tab does not shut them down.** This is the most likely charge
      from this lab.
- [ ] **Endpoints** — delete any endpoint. **Delete the endpoint itself, not just the
      endpoint configuration.**
- [ ] **Notebook instances** — **Stop** first, then **Delete**.
- [ ] **Model Monitor schedules** — if you created a monitoring schedule while exploring
      Step 4, delete it. Monitoring schedules run processing jobs on compute repeatedly and
      will bill indefinitely.
- [ ] **Models** — delete any model entry created for this lab.

Useful CLI checks:

```bash
aws sagemaker list-apps --region us-east-1
aws sagemaker list-endpoints --region us-east-1
aws sagemaker list-monitoring-schedules --region us-east-1
```

### 6.3 Domain 4 sweep

This is the last lab in Domain 4. Confirm nothing survives from Labs 19 to 21:

- [ ] Lab 19 — `aif-lab19-guardrail` deleted from the Bedrock console.
- [ ] Lab 20 — no Clarify processing job InProgress, no stranded shadow endpoint.
- [ ] Lab 21 — no explainability job InProgress, no online-explainability endpoint.
- [ ] Any S3 objects from Clarify outputs or uploaded datasets removed.

### 6.4 Check every Region and confirm billing

- [ ] Resources in another Region do not appear in your current view. If you switched
      Regions at any point, check **each** one.
- [ ] Open **AWS Billing → Bills** or Cost Explorer the following day and confirm no
      unexpected SageMaker or Bedrock charges are accruing.

### 6.5 Keep your artefacts

Delete the AWS resources, but **keep your completed model card content** — the intended use
and out-of-scope list from Step 1, the risk rating justification from Step 2, the
disaggregated evaluation and caveats from Step 3, and the composition exercise from Step 5.

Across Domain 4 you have produced a guardrail findings table, a bias issue report, a
plain-language decision explanation and a model card. That set is a defensible
responsible-AI posture for one system — and it is the evidence that you can identify and
report issues with AI applications and their data.
