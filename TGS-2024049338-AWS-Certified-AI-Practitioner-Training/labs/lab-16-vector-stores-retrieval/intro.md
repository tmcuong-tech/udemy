# Lab 16 — Vector Stores and Retrieval Quality

Tune the retrieval half of a RAG pipeline — chunk size, overlap, top-K and metadata filtering — and learn to tell a retrieval failure from a generation failure.

> ## ⚠️ COST WARNING
>
> This lab uses the Lab 15 knowledge base, backed by a **vector store** that bills continuously by the hour until deleted, whether or not you query it. **Complete this lab in one sitting and do the Clean up step in full** — deleting the knowledge base does not reliably delete the collection underneath.

**Prerequisite:** Lab 15.

**What you will do:**
- Build a five-question test set and measure retrieval quality separately from answer correctness
- Work through the chunk size trade-off and what overlap actually fixes
- Tune top-K and observe a confidently incomplete answer at K=1
- Apply metadata filtering, and use it as the access control boundary in a RAG system
- Follow a diagnostic procedure for a wrong RAG answer, in cost order
