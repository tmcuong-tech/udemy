# Well done!

You have completed Lab 15 — RAG with Knowledge Bases for Amazon Bedrock:

✅ Cost warning, and prepare the S3 data source
✅ How RAG works
✅ Create the knowledge base
✅ Sync the data source
✅ Retrieve and generate, and read the citations
✅ Compare against the no-context baseline
✅ Clean up

**Key takeaways:**

- **RAG changes the prompt, not the model.** Relevant text is found at query time and inserted as context. No weights are modified and nothing is learned.
- The **ingestion pipeline** runs offline on sync: chunk, embed, index. The **query pipeline** runs per request: embed the query, retrieve top-K by vector similarity, insert as context, generate.
- The **same embedding model** must embed documents and queries — vectors from different models are not comparable. Changing it means re-embedding everything.
- **Creating a knowledge base does not ingest anything.** You must sync the data source, and chunking configuration cannot be changed on an existing data source.
- **Citations give traceability.** You can verify each claim against its source chunk — a structural advantage RAG has over fine-tuning, which has no equivalent.
- **RAG reduces hallucination but does not eliminate it.** The model can still over-extend a partial match or blend retrieved context with training knowledge. Contextual grounding checks in Guardrails exist for this.
- An ungrounded model answers **confidently and wrongly** — fluent, specific, indistinguishable from correct. That is why grounding is an engineering requirement.
- **RAG for what the model should know; fine-tuning for how it should behave.**
- **Retrieval is where access control belongs.** Never rely on a prompt instruction to make a model withhold something it was given. And treat retrieved content as untrusted — anyone who can write to the data source can influence another user's session.
- **The vector store is the cost.** It is provisioned infrastructure billing hourly, separate from per-token inference, and it survives deletion of the knowledge base. Always verify with `list-collections`, in every Region you used.

**Next:** Lab 16 — Vector Stores and Retrieval Quality
