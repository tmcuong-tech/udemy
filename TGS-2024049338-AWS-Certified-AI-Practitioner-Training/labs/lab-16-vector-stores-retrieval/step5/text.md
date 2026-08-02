# Step 5 — Diagnose a bad answer

You now have every tool. This step assembles them into a procedure you can apply to any RAG system that is giving wrong answers.

### The diagnostic procedure

When a RAG answer is wrong, resist the urge to edit the prompt. Work through this in order.

**Question 1 — Was the answer in the corpus at all?**

Search the source documents directly. If the fact is not there, this is not a retrieval or generation problem; it is a **data coverage** problem, and the fix is to add the document. Surprisingly often, this is the answer.

**Question 2 — Was the correct chunk retrieved?**

Run retrieval alone and read the chunks. This is the fork in the road:

- **Chunk not retrieved** → retrieval problem. Go to question 3.
- **Chunk retrieved** → generation problem. Go to question 5.

Do not skip this. It determines which half of the system you work on, and getting it wrong means hours spent tuning a prompt that was never the issue.

**Question 3 — Why was the chunk not retrieved?**

- **Was it excluded by a filter?** Re-run without the filter. If it appears, your metadata or filter logic is wrong.
- **Was it ranked below K?** Re-run with a much higher K. If it appears at rank 8, raise K or add re-ranking.
- **Did it not appear at any K?** The chunk's vector is genuinely far from the query's. Causes: the chunk is too large and its vector is a blurred average; the query uses vocabulary the document never uses; or the fact is an exact identifier that vector search handles poorly, which is the case for hybrid search.

**Question 4 — Was the chunk retrieved but incomplete?**

The fact was severed at a chunk boundary. This is a chunking problem: increase chunk size, add overlap, or move to hierarchical chunking. Symptom to recognise: a **confident half-answer** — the model states the part it received as if it were the whole rule.

**Question 5 — The right chunk was retrieved and the answer is still wrong.**

Now, and only now, it is a generation problem:

- **The model contradicted the chunk.** Strengthen the prompt: instruct it to answer only from the provided context. Consider contextual grounding checks in Guardrails.
- **The model blended context with training knowledge.** Same fix, plus check citations — an uncited claim in the answer is the tell.
- **Conflicting chunks were retrieved** — two revisions of the same clause. This is a *metadata* fix, not a prompt fix. Filter to the current version.
- **The model answered despite insufficient context.** Explicitly instruct it to say when the provided context does not answer the question, and treat "I cannot answer from the provided documents" as a **successful** outcome, not a failure. A system that never admits ignorance is a system whose ignorance you cannot see.

### Work an example

Recall **Q3**: *Can I get express delivery to Malaysia?*

The correct answer is no — `shipping-policy.txt` states express is available in Singapore only. The document never says "Malaysia" and "express" in the same sentence, because it is expressing the answer as a **limitation** rather than a denial.

Run Q3 and work the procedure:

1. Is the answer in the corpus? Yes, implicitly, in the express delivery paragraph.
2. Was the chunk retrieved? Check. Vector similarity to a query mentioning Malaysia may pull the *international delivery* paragraph instead, which mentions Malaysia and never mentions express.
3. If the express paragraph was not retrieved — is it below K, or genuinely distant? Try a higher K.
4. If both paragraphs came back, what did the model do? Did it correctly combine "express is Singapore only" with the question about Malaysia, or did it see "Malaysia: 5 working days" and answer with a delivery time?

**The lesson:** negative and constraint-based facts are harder for RAG than positive facts, because the query's vocabulary matches the wrong paragraph. The mitigation is partly retrieval — higher K, hybrid search — and partly **how the source documents are written**. A policy document that states limitations explicitly ("Express delivery is not available outside Singapore") retrieves far better than one that states them by omission.

> **Document authoring is part of RAG engineering.** A corpus written for human readers, who infer from context, often retrieves badly. Explicit, self-contained statements retrieve well. This is a genuine and underrated lever.

### The tuning order

When retrieval quality is poor, work in this order — cheapest and highest-leverage first:

1. **Check data coverage.** Is the fact even there?
2. **Fix the source documents.** Make implicit facts explicit. Free, and it helps every query.
3. **Add metadata and filter.** Shrinks the haystack. No re-chunking needed.
4. **Tune top-K.** Per query, no re-ingestion, immediate feedback.
5. **Add hybrid search or re-ranking.** More capability, more cost per query.
6. **Change the chunking strategy.** Requires full re-ingestion — do it last, and test on a sample first.
7. **Only then** touch the generation prompt.

Most teams do this list backwards, starting with the prompt because it is the most visible part. That is why so much time gets spent on prompts that were never the problem.

**Checkpoint:** You can state the procedure, know that retrieval-only inspection is the fork that decides everything, and can explain why negative facts retrieve poorly and what to do about it.
