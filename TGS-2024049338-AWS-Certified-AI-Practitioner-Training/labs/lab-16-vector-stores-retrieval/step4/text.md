# Step 4 — Metadata filtering

Vector similarity finds semantically similar text. It has no idea whether a chunk is current, whether it applies to the right region, or whether **this particular user is allowed to see it**. Metadata filtering supplies that.

### How metadata works

Each document can carry structured attributes. For a Bedrock knowledge base with an S3 data source, you supply these in a companion metadata file alongside each document in the bucket, using the naming convention shown in the console for your Region.

The content is a small JSON object of attributes you define:

```json
{
  "metadataAttributes": {
    "doc_type": "claims",
    "audience": "internal",
    "revision": 2,
    "effective_year": 2026
  }
}
```

Attribute names and values are yours to choose. Design them deliberately — you are defining the filter dimensions your application will have forever, and adding a new one later means re-ingesting.

At query time, a filter is applied **during** the vector search, so non-matching chunks are never candidates:

```bash
aws bedrock-agent-runtime retrieve \
  --knowledge-base-id <YOUR_KB_ID> \
  --retrieval-query '{"text":"What are the claim deadlines?"}' \
  --retrieval-configuration '{
      "vectorSearchConfiguration": {
        "numberOfResults": 5,
        "filter": { "equals": { "key": "audience", "value": "internal" } }
      }
  }' \
  --region us-east-1
```

Check the console or the service documentation for the full set of filter operators available in your Region — typically equality, inequality, comparison operators for numbers, list membership, and boolean combinations.

### Try it

If you want to see it working end to end, add a metadata file for each of your three documents with a `doc_type` attribute (`shipping`, `claims`, `tiers`), re-sync, and then run **Q1** with a filter restricting to `doc_type = shipping`. Retrieval should fail to find the claims deadline, because the only chunk containing it has been excluded from the candidate set.

That failure is the point. **The filter is applied before similarity ranking, not after.** An excluded chunk is not a low-scoring result — it does not exist as far as this query is concerned.

### The three things filtering is for

**1. Access control — the important one.**

Consider a chat interface used by both customers and operations staff over one knowledge base. The claims policy is internal.

The wrong design: instruct the model in the system prompt not to reveal internal policies to customers. Lab 14 explains exactly why this fails — the instruction is steering, not enforcement, the content is already in the context window, and prompt injection or plain misunderstanding will eventually surface it.

The right design: **the customer's session applies a filter of `audience = public`, so internal chunks are never retrieved.** The model cannot leak what it was never given. The control is deterministic and it sits outside the probabilistic component.

This is the single most important architectural point in the lab. **Access control in RAG belongs at retrieval.** Your application derives the filter from the authenticated user's identity — never from anything the user typed, which would let them ask for the filter to be widened.

**2. Freshness and versioning.** Filter to the current revision so superseded policy text is never retrieved, while remaining in the store for audit. Without this, a query can retrieve both revision 2 and revision 4 of the same clause, and the model has no reliable way to know which governs.

**3. Precision on large corpora.** With three documents everything is close. With fifty thousand, a query about claims will surface superficially similar text from unrelated departments. Narrowing the candidate set by department, product line or geography raises precision far more cheaply than tuning K.

### Design guidance

- **Filter first, then tune K.** Filtering shrinks the haystack; K decides how much of it you take. Doing them the other way round wastes effort.
- **Metadata is set at ingestion.** A dimension you did not think of means re-ingesting. Think about audience, effective date, version, language and owning team up front.
- **Never let user input construct the filter.** Derive it from the authenticated session. A filter built from user-supplied text is an authorisation bypass waiting to happen.
- **Filtering does not replace bucket-level security.** If a document must not be retrievable by a class of user, also consider whether it should be in that knowledge base at all. Separate knowledge bases for separate trust domains is a legitimate and often safer design.

**Checkpoint:** You can write a metadata attributes object, explain why a filter is applied before ranking rather than after, and argue why access control belongs at retrieval rather than in the system prompt.
