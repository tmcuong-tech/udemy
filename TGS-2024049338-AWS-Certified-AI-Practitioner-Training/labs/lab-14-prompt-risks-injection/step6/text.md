# Step 6 — Clean up

### Delete the guardrail if you created one

If you created a guardrail in Step 5 and do not need it for Lab 19:

1. In the Bedrock console left navigation, choose **Guardrails**.
2. Select the guardrail you created and delete it.

A guardrail is configuration rather than provisioned compute, so it does not bill by the hour. Charges relate to usage when a guardrail evaluates content. Consult the official Amazon Bedrock pricing page for current rates. If you would rather keep it for **Lab 19 — Amazon Bedrock Guardrails**, keeping it is fine — just note that it exists so you do not lose track of it.

### Bedrock inference

On-demand inference is serverless. Nothing was provisioned and nothing bills by the hour. Close the playground tab so a stray keypress does not submit another billed request.

### Confirm no billable resource remains

Check the Bedrock console for anything created while exploring, because unlike on-demand inference these bill continuously until deleted:

- **Provisioned throughput** — bills for its whole committed term
- **Custom models**
- **Knowledge bases and their underlying vector store** — an OpenSearch Serverless collection bills continuously whether or not you query it

If you did not create these, there is nothing to remove.

### Handle your test artefacts responsibly

1. **Delete or clearly label your probe inputs.** If you keep them, keep them in a file marked as security test fixtures for an application you own. Do not leave them in a shared prompt library where someone may mistake them for examples to reuse elsewhere.
2. **Do not reuse these probes against systems you do not own.** This bears repeating at the end as well as the start. The techniques here are for hardening your own applications and for the exam; the same input sent to a third party's product is a different act entirely.
3. **Rotate anything real that was exposed.** In this lab the leaked string was fictional. If in your own work you ever discover a genuine credential inside a system prompt, treat it as compromised: rotate it, then remove it from the prompt permanently.

### Carry forward

Keep your defence table. **Lab 15 attaches a RAG knowledge base to a model**, and the moment you do that, every document in the data source joins your attack surface — which is exactly the indirect injection case from Step 2. The delimiting and validation habits you formed here apply directly to retrieved chunks.

**Checkpoint:** Guardrail deleted or deliberately retained for Lab 19, playground closed, no provisioned throughput or knowledge base in the account, and probe inputs stored responsibly or deleted.
