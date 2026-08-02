# Step 6 — Clean up

> ### IMPORTANT — SageMaker bills continuously
> **SageMaker notebook instances, Studio applications and spaces, and inference endpoints
> are charged for every hour they exist, whether or not you are using them.** They do
> **not** stop by themselves. An explainability job deploys a shadow endpoint to obtain
> predictions; if the job failed midway that endpoint can be left running and will keep
> billing until you delete it.

**If you took Path 2 only, you created nothing and there is nothing to delete.** Read 6.1
anyway — the failure modes are exam-relevant.

### 6.1 Delete SageMaker resources (Path 1 only)

Go to the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/) and work
through the left navigation:

- [ ] **Endpoints** — delete every endpoint. **Delete the endpoint itself, not just the
      endpoint configuration.** Check the list even if you never deliberately created one:
      the Clarify shadow endpoint appears here.
- [ ] **Endpoint configurations** — delete after the endpoints.
- [ ] **Models** — delete model entries created for this lab.
- [ ] **Processing jobs** — confirm the explainability job shows **Completed**, **Stopped**
      or **Failed**, not **InProgress**. Stop any still running.
- [ ] **Notebook instances** — **Stop** first, then **Delete**. A stopped instance still
      incurs storage charges; a deleted one does not.
- [ ] **Studio apps and spaces** — shut down running apps, spaces and kernel sessions.
      **Closing the browser tab does not shut them down.**
- [ ] **Online explainability** — if you attached explainability to a real-time endpoint in
      3.3, that endpoint is billing continuously. Delete it.

Useful CLI checks:

```bash
aws sagemaker list-endpoints --region us-east-1
aws sagemaker list-processing-jobs --status-equals InProgress --region us-east-1
aws sagemaker list-apps --region us-east-1
```

### 6.2 Clear storage

- [ ] Delete Clarify explainability outputs from your S3 prefix if you no longer need them.
- [ ] Remove any dataset uploaded solely for this lab.

### 6.3 Check every Region you used

- [ ] Resources in another Region do not appear in your current view. If you switched
      Regions at any point, check **each** one.

### 6.4 Final confirmation

- [ ] Open **AWS Billing → Bills** or Cost Explorer the following day and confirm no
      unexpected SageMaker charges are accruing.

### 6.5 Keep your artefacts

Keep your written answers from 4.1, 4.2 and 5.3 — especially the plain-language refusal
reason from question 4. That single sentence is the whole point of explainability, and you
will reuse this material when you complete the caveats and limitations sections of the model
card in Lab 22.
