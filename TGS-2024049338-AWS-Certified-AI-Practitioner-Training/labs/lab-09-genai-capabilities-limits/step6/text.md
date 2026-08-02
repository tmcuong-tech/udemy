# Step 6 — Clean up

This lab used the **serverless** Bedrock playground only. No endpoint, index or instance was created, so nothing is billing by the hour.

1. **Clear the conversation and close the playground tab.** You ran a lot of prompts in this lab, and an open playground is one keystroke away from another billable request.

2. **Reset any inference parameters** you changed while testing non-determinism, so a later lab does not inherit them.

3. **Keep your written records.** The hallucination record from Step 3 and the limitations and mitigations tables from Steps 4 and 5 are the deliverables of this lab and appear in the verification checklist. They are also the most directly exam-relevant notes you will produce in Domain 2.

4. **Handle the outputs responsibly.** If you generated bias examples in Step 4, do not circulate them out of context — they are teaching artefacts produced from a handful of runs, not a measurement of any model's fairness. Any real claim about bias requires a defined metric and many samples (Lab 20).

5. **Confirm nothing billable was created.** If you explored beyond the playground into Knowledge Bases, Guardrails evaluation, model evaluation jobs, provisioned throughput or custom models, remove what you created:

   ```bash
   aws bedrock list-provisioned-model-throughputs --region us-east-1
   aws bedrock list-custom-models --region us-east-1
   ```

   Both should return an empty list.

   > If you created a **Knowledge Base** while exploring the grounding section, delete it — and check separately for an **OpenSearch Serverless collection**, which may have been created alongside it and which bills continuously whether you query it or not.

6. **Leave model access enabled** if you are continuing to Lab 10. Enabled access costs nothing; invocations are billed on tokens processed.

**Checkpoint:** Playground closed, parameters reset, your written records kept, and no Knowledge Base, vector store, provisioned throughput or custom model exists in your account.
