# Step 6 — Clean up

> ### IMPORTANT — SageMaker bills continuously
> **SageMaker notebook instances, Studio applications and spaces, and inference endpoints
> are charged for every hour they exist, whether or not you are using them.** They do
> **not** stop by themselves. An endpoint left running overnight, over a weekend or over a
> term break keeps accruing charges until you delete it. This is the single most common
> source of unexpected AWS bills in training accounts.

**If you completed Path 2 only, you created nothing and there is nothing to delete.** Read
Section 6.1 anyway — the failure modes it describes are exam-relevant and career-relevant.

### 6.1 Delete SageMaker resources (Path 1 only)

Go to the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/) and work
through the left navigation:

- [ ] **Endpoints** — delete every endpoint. **Delete the endpoint itself, not just the
      endpoint configuration** — deleting only the configuration leaves the endpoint running
      and billing. A Clarify job can strand a shadow endpoint if it failed midway, so check
      even if you never created one deliberately.
- [ ] **Endpoint configurations** — delete after the endpoints.
- [ ] **Models** — delete model entries created for this lab.
- [ ] **Processing jobs** — confirm the Clarify job shows **Completed**, **Stopped** or
      **Failed**, not **InProgress**. Stop any still running.
- [ ] **Notebook instances** — **Stop** first, then **Delete**. A stopped instance still
      incurs storage charges; a deleted one does not.
- [ ] **Studio apps and spaces** — shut down running apps, spaces and kernel sessions.
      **Closing the browser tab does not shut them down.**

Useful CLI checks:

```bash
aws sagemaker list-endpoints --region us-east-1
aws sagemaker list-notebook-instances --region us-east-1
aws sagemaker list-processing-jobs --status-equals InProgress --region us-east-1
```

### 6.2 Clear storage

- [ ] Delete Clarify output objects from your S3 output prefix if you no longer need the
      report.
- [ ] Remove any dataset you uploaded solely for this lab — particularly if it contained
      real personal data, which should not linger in a training account.

### 6.3 Check every Region you used

- [ ] Resources in another Region do not appear in your current view. If you switched
      Regions at any point, check **each** one.

### 6.4 Final confirmation

- [ ] Open **AWS Billing → Bills** or Cost Explorer the following day and confirm no
      unexpected SageMaker charges are accruing.

### 6.5 Keep your artefacts

Delete the AWS resources, but **keep your written answers from 5.2 and the issue report from
5.3**. Those are the deliverables that evidence the ability code.
