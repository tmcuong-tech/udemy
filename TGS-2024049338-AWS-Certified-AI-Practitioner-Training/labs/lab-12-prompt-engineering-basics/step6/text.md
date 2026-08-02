# Step 6 — Clean up

**Good news: this lab is serverless.** Amazon Bedrock on-demand inference leaves behind no instance, endpoint, cluster or collection. There is nothing to delete and nothing accruing an hourly charge from this lab.

Still, complete these steps:

1. **Close the playground tab.** An open playground is one stray keypress away from another billed request.
2. **Understand what you were charged for.** On-demand Bedrock billing is based on **tokens processed — input and output**. Your few-shot prompt was billed for its examples on *every* invocation. Consult the official Amazon Bedrock pricing page for current rates; do not rely on figures quoted from memory or from older course material.
3. **Leave model access as it is.** Model access is a persistent, per-account, per-Region setting. Having access enabled does **not** generate charges — only invocations do. In a shared or corporate account, follow your organisation's policy on which models may remain enabled.
4. **Set up cost visibility.** If this is your own account, enable AWS Budgets or a billing alert so unexpected usage is surfaced early. Do this once; it protects every remaining lab in this course.
5. **Keep your prompts.** Save the four prompts and your results table. Lab 13 builds directly on the structured prompt from this lab, and Lab 14 hardens it against misuse.

### Nothing to delete — but check anyway

If you explored beyond this lab's steps, look for these, because unlike on-demand inference they **do** bill continuously until deleted:

- **Provisioned throughput** for a model (Bedrock console → provisioned throughput)
- **Custom models** you created or imported
- **Knowledge bases** and their underlying vector store — an Amazon OpenSearch Serverless collection bills continuously whether or not you query it
- **SageMaker notebook instances, Studio apps or inference endpoints**

If you did not create any of these, you have nothing to remove.

**Checkpoint:** Playground closed, no provisioned throughput or custom models exist in your account, and a billing alert is in place.
