# Step 4 — Sync the data source

Creating a knowledge base does not ingest anything. Documents are only chunked, embedded and indexed when you **sync** the data source. This trips people up constantly: the knowledge base exists, queries return nothing, and the sync was never run.

### Run the sync

1. Open your knowledge base in the console.
2. In the **data source** section, select your S3 data source and choose **Sync**.
3. Wait for it to complete. Three small text files take a short time; a large corpus can take considerably longer.
4. When it finishes, read the sync result. It reports how many documents were scanned, ingested and failed. **Confirm three documents were ingested and zero failed.**

If any document failed, the usual causes are an unsupported file type, an empty file, or the service role lacking `s3:GetObject` on the bucket.

### What just happened

For each document, in order:

1. It was **read** from S3.
2. It was **split into chunks** by your chosen strategy.
3. Each chunk was sent to the **embedding model** and converted to a vector.
4. Each vector was **written to the vector store** along with the chunk text and metadata identifying its source document.

Step 4 is why citations are possible. The source location travels with the vector, so a retrieved chunk can always be traced back to the file it came from.

You were billed for embedding tokens during this sync. That is a one-off per-sync cost, quite separate from the hourly vector store cost that has been accruing since Step 3.

### Inspect the retrieval directly

Before generating any answer, look at raw retrieval on its own. Separating retrieval from generation is the most valuable diagnostic habit in RAG work, and Lab 16 depends on it.

Use the CLI:

```bash
aws bedrock-agent-runtime retrieve \
  --knowledge-base-id <YOUR_KB_ID> \
  --retrieval-query '{"text":"How long do I have to file a damage claim?"}' \
  --region us-east-1
```

Or use the console's test window, which offers an option to show the retrieved source chunks alongside the generated response.

Examine the result carefully:

- **How many chunks came back?** That is your top-K, at its default.
- **What is in each chunk?** Read the actual text. Does the chunk containing the 7-day claim window also carry enough surrounding context to be understandable alone?
- **Is there a relevance score?** Higher means the chunk's vector was closer to the query's vector. Scores are comparable within one knowledge base and one embedding model; they are not an absolute measure of correctness.
- **Which source document is cited?** The location metadata should point at `claims-policy.txt`.

### Try a query that spans documents

```bash
aws bedrock-agent-runtime retrieve \
  --knowledge-base-id <YOUR_KB_ID> \
  --retrieval-query '{"text":"What happens if a Gold tier perishable shipment is late?"}' \
  --region us-east-1
```

This question requires facts from **three** documents: the Gold tier service credit, the temperature-controlled shipping rules, and the priority claims handling for temperature excursions.

Look at what came back. Did retrieval pull chunks from all three files, or did it return three chunks from whichever document matched most strongly overall? **Multi-document questions are where naive RAG most often falls short** — not because the model reasoned badly, but because the right chunks were never retrieved. Note what you observe; you will address it with top-K in Lab 16.

**Checkpoint:** Sync completed with three documents ingested and zero failures, and you have inspected raw retrieval output including chunk text, scores and source attribution.
