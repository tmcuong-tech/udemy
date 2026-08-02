# Step 7 — Clean up

> ### IMPORTANT — leave nothing running
> Guardrail storage itself is negligible, but **model invocations are billable** and any
> SageMaker or other compute you started while exploring bills continuously. Resources do
> not stop by themselves. Complete every step below before you close your browser.

### 7.1 Delete the Bedrock guardrail

1. Go to the [Amazon Bedrock console](https://console.aws.amazon.com/bedrock/).
2. In the left navigation, choose **Guardrails**.
3. Select `aif-lab19-guardrail`.
4. Choose **Delete** and confirm. If the guardrail has published versions, delete those as
   part of the deletion flow.
5. Refresh the list and confirm it no longer appears.

Or from the CLI, using the ID you recorded in Step 5:

```bash
aws bedrock delete-guardrail --guardrail-identifier <your-guardrail-id> --region us-east-1
```

### 7.2 Check the Region you actually worked in

- [ ] Resources in another Region will not appear in your current view. If you switched
      Regions at any point, check **each** one.

### 7.3 Final confirmation

- [ ] `aif-lab19-guardrail` no longer appears in the Guardrails list.
- [ ] No other Bedrock or SageMaker resources were left behind from exploring.
- [ ] Open **AWS Billing → Bills** or Cost Explorer the following day and confirm no
      unexpected charges are accruing.

### 7.4 Keep your artefacts

Delete the AWS resources, but **keep the completed findings table and your reflection**.
Those are the evidence that you can identify and report issues with an AI application — the
deliverable, not the guardrail itself.
