# Step 6 — Compare against the no-context baseline

This step turns the lab into evidence. Put the RAG answer beside the plain-model answer from Step 1.

### The comparison

Open the plain **Chat** playground — no knowledge base — and re-ask all four questions from Step 5. Then place the two sets side by side.

| Question | Plain model answer | RAG answer | Which is correct? |
|---|---|---|---|
| Max liability | | | |
| Express to Malaysia | | | |
| Gold tier perishable late | | | |
| Lithium batteries by air | | | |

### What to notice

**The plain model was confident and wrong.** This is the observation that matters most. It did not say "I have no information about Northwind Logistics." It produced a fluent, specific, plausible answer — a liability figure, a delivery timeframe — with the same tone it uses when correct.

This is the practical definition of **hallucination**: not gibberish, but confident fabrication that is indistinguishable from a correct answer by fluency alone. A user cannot tell the difference. **That** is why grounding and citations are engineering requirements and not niceties.

**The RAG answer could be checked.** Every claim traced to a document you can open. Even where RAG was imperfect — question 3, or a partially-cited multi-document answer — you could *see* the imperfection. The plain model's errors were invisible.

**Freshness.** Change one fact in `claims-policy.txt`, upload the new version, and re-sync. The knowledge base reflects it within a sync. There is no equivalent for training data — a fine-tuned model with an outdated fact needs retraining.

### Design considerations this lab surfaces

These map directly to Task 3.1, "design considerations for applications that use foundation models":

- **Context window.** Retrieved chunks consume it. Higher top-K, larger chunks, or a long conversation history all compete for the same finite budget.
- **Cost per query.** You pay to embed the query, and you pay input tokens for every retrieved chunk on every call. Doubling top-K roughly doubles the retrieval portion of your input tokens.
- **Latency.** RAG adds an embedding call plus a vector search before generation begins.
- **Access control.** Retrieval is where per-user permissions belong. If a user must not see the claims policy, filter it out at retrieval — never rely on a prompt instruction to make the model decline. Metadata filtering, covered in Lab 16, is the mechanism.
- **Freshness versus consistency.** The vector store is only as current as the last sync. Decide your sync cadence and know your staleness window.
- **Retrieved content is untrusted.** Lab 14's indirect injection risk lands here concretely. Anyone who can write to that S3 bucket can influence what the model reads in **another user's** session. Lock down write access to the data source with the same rigour you apply to code.

### When RAG is the wrong answer

RAG is not universal. It is a poor fit when:

- the question needs **aggregation across the whole corpus** ("how many of our policies mention perishables?") — retrieval returns a handful of chunks, not a count, and a database query is the right tool;
- the corpus is **small enough to fit in the context window** — just include it and skip the vector store cost entirely;
- what you need is a **change of style, tone or output format** — that is prompt engineering or fine-tuning, not retrieval;
- the answer requires **reasoning over structured data** — SQL against a database beats similarity search over prose.

**Checkpoint:** All four questions compared side by side, and you can articulate why a confidently wrong answer is more dangerous than a refusal.
