# Step 6 — Clean up

As in Lab 06, on-demand Bedrock inference is **serverless** — this lab leaves behind no instance, endpoint or cluster to delete.

1. **Reset your inference parameters** to their defaults before leaving the playground, so a later lab does not inherit an extreme temperature or a tiny max tokens value and confuse you.
2. **Clear the conversation and close the playground tab.** An open playground is one stray keystroke away from another billable request.
3. **Leave model access enabled** if you are continuing to Lab 08, which needs an embeddings model. Otherwise follow your organisation's policy on which models may remain enabled. Enabled access costs nothing; **invocations** are billed on tokens processed.
4. **Keep your tables.** The model comparison table and the parameter observation table are the deliverables of this lab and are referenced in the verification checklist.
5. **Confirm nothing billable was created while exploring.** If you clicked into Provisioned Throughput, custom models, model evaluation or Knowledge Bases, delete what you created — these bill continuously, unlike on-demand inference:

   ```bash
   aws bedrock list-provisioned-model-throughputs --region us-east-1
   aws bedrock list-custom-models --region us-east-1
   ```

   Both should return an empty list.

   > **Provisioned Throughput is the expensive mistake here.** It reserves model capacity for a committed term and bills for that term whether you send requests or not. On-demand inference is the correct choice for all of this course's labs.

6. **Do not estimate costs from memory.** Token pricing differs by model and by provider — a model that looked best in your comparison table may be several times the price of the runner-up. Consult the official Amazon Bedrock pricing page when the trade-off matters.

**Checkpoint:** Parameters reset, playground closed, no provisioned throughput or custom models exist, and both tables are filled in.
