# Well done!

You have completed Lab 11 — Amazon Q Business Getting Started:

✅ What Amazon Q Business is and what it will cost
✅ Prepare documents in Amazon S3
✅ Create the Amazon Q Business application
✅ Connect the S3 data source and sync
✅ Ask questions grounded in your documents
✅ Test the boundaries of grounding
✅ Clean up

**Key takeaways:**

- **Amazon Q Business is a managed generative AI assistant for enterprise data.** It sits above Bedrock: Bedrock gives you a model and you build the RAG pipeline; Q Business gives you the finished, cited, permission-aware application.
- You trade control for speed. You cannot choose the model, the prompt, the chunking strategy or the embedding model — and you write no code and manage no vector store.
- **Connectors are a large part of the value** — ingestion, incremental sync and permission mapping you would otherwise build and maintain.
- **Permission-aware retrieval is the strongest argument for buying rather than building.** Two employees asking the same question correctly get different answers. A hand-built index does not know who is asking.
- **Citations make checking cheap enough to actually do** — Lab 09's mitigation, built in by default.
- **Grounding guarantees the answer matches the indexed documents. It guarantees nothing about whether those documents are current.** A failed or unscheduled sync produces confident, cited, out-of-date answers. Someone must own the sync.
- **Q Business bills for as long as the application exists**, not per question. Closing the browser stops nothing — only deleting the application does, and you should verify the deletion from the API.

**Next:** Lab 12 — Prompt Engineering Basics — Zero-Shot and Few-Shot
