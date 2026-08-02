# Well done!

You have completed Lab 08 — Tokens, Embeddings and Vector Representations:

✅ Tokens are not words
✅ Tokens drive cost and the context window
✅ Generate an embedding
✅ Semantic similarity — compare the vectors
✅ Where this leads — vector stores and RAG
✅ Clean up

**Key takeaways:**

- Models read **tokens**, not words. Roughly ¾ of a word per token in English, but rare words, timestamps, code and non-Latin scripts fragment into far more tokens than their word count suggests.
- Tokens drive **two separate constraints**: **cost** (input and output priced separately, billed on every call) and the **context window** (a hard per-request ceiling covering input *and* output that you cannot raise).
- Chat costs grow per turn because the conversation history is resent; long system prompts are paid for on every single call.
- An **embedding** converts any text into a **fixed-length vector**. Individual coordinates mean nothing — meaning lives in the direction of the whole vector, and only surfaces when vectors are compared.
- **Cosine similarity** ranks by meaning, not by shared words. What matters is the ranking of scores relative to each other, not the absolute value.
- Embeddings plus a vector store are the retrieval half of **RAG**. The **same embedding model must be used to index and to query** — changing it forces a full re-index of the entire corpus.
- Embedding calls are serverless, but **vector stores are not**: OpenSearch Serverless collections, Kendra indexes and Aurora clusters bill continuously.

**Next:** Lab 09 — Generative AI Capabilities and Limitations
