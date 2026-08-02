# Step 6 — Clean up

**Good news: on-demand Bedrock inference is serverless.** Running this lab does not leave behind an instance, an endpoint or a cluster that bills you by the hour. There is nothing you must delete to stop a meter.

That said, do the following:

1. **Close the playground tab.** A stray keystroke in an open playground submits another billable request.

2. **Decide what to do about model access.** Access granted in Step 2 is a **persistent account setting** — it stays granted in that Region until you change it. In a shared or corporate account, follow your organisation's policy on which models may remain enabled. Leave your models enabled if you are continuing to Labs 07 and 08, which need them.

   > Enabled access by itself does **not** generate charges. **Invocations** do.

3. **Check that you did not create anything billable while exploring.** If, while looking around the console, you created any of the following, delete it now — these are **not** serverless and continue to incur charges until removed:
   - **Provisioned Throughput** for a model (billed for a committed term — this is the most expensive accidental click in the Bedrock console)
   - A **custom model** / fine-tuning job
   - A **Knowledge Base**, and any vector store it created for you, such as an **OpenSearch Serverless collection**
   - A **model evaluation job**

   To check from the CLI:

   ```bash
   aws bedrock list-provisioned-model-throughputs --region us-east-1
   aws bedrock list-custom-models --region us-east-1
   ```

   Both should return an empty list after this lab.

4. **Turn on cost visibility.** If this is your own account, set up an **AWS Budget** or a billing alert so that unexpected usage surfaces early rather than at the end of the month.

5. **Do not quote pricing from memory.** Consult the official Amazon Bedrock pricing page for current rates before doing any cost estimation for a real project.

**Checkpoint:** The playground is closed, no provisioned throughput or custom models exist, and you have made a conscious decision about which models stay enabled.
