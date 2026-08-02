# Step 7 — Clean up

This lab used only Bedrock **on-demand inference**, which is serverless. There is no instance, endpoint, cluster or collection left behind and nothing accruing an hourly charge.

1. **Close the playground tab** so a stray keypress does not submit another billed request.
2. **Note what you were billed for.** On-demand Bedrock billing is on **tokens processed, input and output**. This lab was more expensive per call than Lab 12 for two reasons worth internalising: chain-of-thought generates substantially more **output** tokens, and a long system prompt is re-sent on **every** call. Consult the official Amazon Bedrock pricing page for current rates rather than any figure from memory.
3. **If you saved anything in Bedrock prompt management,** decide whether to keep it. Stored prompts are configuration, not compute — they do not bill hourly — but tidy them up if you were only experimenting.
4. **Leave model access as it is.** It is a persistent per-account, per-Region setting and generates no charge by itself. Only invocations cost money.
5. **Confirm no billable resource was created.** In the Bedrock console check that you have no **provisioned throughput**, no **custom models**, and no **knowledge bases**. Unlike on-demand inference these bill continuously until deleted — a knowledge base's underlying OpenSearch Serverless collection in particular bills whether or not you ever query it. If you did not create any, there is nothing to remove.
6. **Save your template.** Store the system prompt, the user prompt template and your edge case suite somewhere you can retrieve them. **Lab 14 attacks this exact template and hardens it**, so you will want it.

**Checkpoint:** Playground closed, template and edge case results saved, and you have confirmed no provisioned throughput, custom model or knowledge base exists in your account.
