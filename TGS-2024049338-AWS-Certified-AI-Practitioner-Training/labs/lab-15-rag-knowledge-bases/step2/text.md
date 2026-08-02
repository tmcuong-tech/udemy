# Step 2 — How RAG works

**Retrieval Augmented Generation** solves one specific problem: the model does not know your data. Its training data has a cutoff and never included your internal documents.

RAG does **not** teach the model anything. It **finds relevant text at query time and puts it in the prompt**. The model is unchanged. That single sentence answers a large share of exam questions on this topic.

### The two pipelines

RAG has an offline pipeline that runs when documents change, and an online pipeline that runs on every query. Confusing the two is a common error.

**Ingestion — offline, runs on sync:**

```
Documents in S3
      ↓  chunk
Text chunks
      ↓  embedding model
Vectors  (a list of numbers per chunk)
      ↓  index
Vector store
```

**Retrieval and generation — online, runs per query:**

```
User query
      ↓  same embedding model
Query vector
      ↓  similarity search against the vector store
Top-K most similar chunks
      ↓  inserted into the prompt as context
Foundation model
      ↓
Answer, with citations back to the source chunks
```

### The four moving parts

**1. Chunking.** Documents are split into pieces. Whole documents are not used because the context window is finite, retrieval precision is better on smaller units, and you pay tokens for everything you insert.

The tension: chunks too **small** lose the context that makes them meaningful; chunks too **large** dilute the match and waste tokens on irrelevant text. **Overlap** — repeating some text between adjacent chunks — stops a fact being sliced in half at a boundary. Bedrock knowledge bases offer strategies including fixed-size chunking with configurable size and overlap, and options for hierarchical and semantic chunking. Check the console for the strategies available in your Region. Lab 16 tests these directly.

**2. Embeddings.** An embedding model converts text into a vector — a list of numbers positioning that text in a high-dimensional space where semantically similar text sits close together. This is why RAG finds a chunk about "maximum liability" when you asked about "how much you cover" with no shared keywords. Contrast with keyword search, which would miss it.

**Critical:** the **same** embedding model must embed the documents and the queries. Vectors from different models are not comparable. Changing the embedding model means **re-embedding everything**.

**3. Vector store.** A database that indexes vectors and answers "which stored vectors are nearest to this one" quickly. Bedrock knowledge bases can create an OpenSearch Serverless collection for you, or use a vector store you already run — options typically include Amazon Aurora PostgreSQL with pgvector, Amazon OpenSearch Service, Pinecone and Redis Enterprise Cloud. Check the console for what is offered in your Region.

**This component is the cost.** The embedding and generation calls are per-token; the vector store is provisioned infrastructure billing by the hour.

**4. Retrieval and generation.** At query time the top-K chunks are retrieved and inserted into a prompt template alongside the question. The model answers **from that context**. Because you know which chunks were inserted, you can attach **citations** — the property that makes RAG auditable and distinguishes it sharply from fine-tuning.

### RAG versus fine-tuning

The most reliably examined comparison in Domain 3:

| | RAG | Fine-tuning |
|---|---|---|
| Changes model weights | No | Yes |
| Adds new facts | Yes | Poorly — it teaches form more than fact |
| Update a fact | Re-sync the document, seconds | Retrain, hours to days |
| Citations | Yes, natural | No |
| Cost profile | Vector store hourly + tokens per query | Training cost + hosting cost |
| Access control | Can filter by user permissions at retrieval | No — knowledge is baked in for everyone |
| Best at | Current, private, frequently changing facts | Style, tone, format, domain vocabulary, task shape |

The heuristic: **RAG for what the model should know; fine-tuning for how the model should behave.** Lab 17 works through this decision in full.

**Checkpoint:** You can draw both pipelines, explain why one embedding model must serve both sides, and state which component is the hourly cost.
