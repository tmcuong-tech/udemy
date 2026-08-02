# Step 5 — Where this leads: vector stores and RAG

You have now built, by hand, the core of a semantic search engine. Scale it up and it becomes the retrieval half of a **RAG** (Retrieval Augmented Generation) system — the subject of Labs 15 and 16.

## The pipeline

**Indexing — done once, ahead of time:**

1. **Chunk** the documents. A 40-page policy PDF is split into passages, because you want to retrieve the relevant paragraph, not the whole file.
2. **Embed** each chunk with an embedding model — exactly the call you made in Step 3.
3. **Store** each vector, alongside its source text and metadata, in a **vector store** — a database that can search by vector proximity. On AWS this might be an OpenSearch Serverless collection, Aurora with pgvector, or another supported store.

**Query time — done on every user question:**

4. **Embed the question** with the **same** embedding model.
5. **Search** the store for the nearest vectors — this is your cosine calculation from Step 4, done efficiently over millions of vectors.
6. **Assemble a prompt** containing the retrieved chunks plus the question, and send it to a **text generation** model.
7. The model answers **grounded in the retrieved text**, and can cite where the answer came from.

## Four things that follow directly from what you just did

**The same model must be used for both sides.** Vectors from two different embedding models are not comparable — they are coordinates in different spaces. If you change embedding model, you must **re-embed your entire corpus**. This is a real migration cost, and a common exam point.

**Embedding models and text models are different tools.** An embedding model cannot write you a paragraph. A text model cannot give you a vector to store. Both appear in the Bedrock catalogue; they have different output modalities, as you saw in Lab 06.

**Retrieved chunks are input tokens.** Everything you retrieve is pasted into the prompt and billed on every call, and it competes for the context window (Step 2). This is why RAG systems retrieve the top few chunks rather than everything that scored above a threshold — retrieval quality beats retrieval quantity.

**Chunk size is a trade-off.** Chunks that are too large dilute the meaning of the vector and waste tokens. Chunks that are too small lose the context needed to answer. Lab 16 makes you tune this.

## Beyond search

The same vectors support:

- **Recommendation** — "items similar to this one" is a nearest-neighbour query
- **Clustering and topic discovery** — group vectors that sit close together
- **Deduplication** — near-identical documents produce near-identical vectors
- **Classification** — embed the input, compare against labelled examples

**Checkpoint:** You can describe the seven-step RAG pipeline and explain why changing the embedding model forces a full re-index.
