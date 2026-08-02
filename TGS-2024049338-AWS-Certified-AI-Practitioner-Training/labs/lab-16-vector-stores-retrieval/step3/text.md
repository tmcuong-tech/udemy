# Step 3 — Top-K

**Top-K** is how many chunks retrieval returns for insertion into the prompt. Unlike chunking, it is set **per query** — so you can experiment freely without re-ingesting anything.

### Run the experiment

Take **Q4**, the multi-document question, which needs facts from all three files:

```
What happens if a Gold tier customer's perishable shipment arrives late?
```

Run it at several values of K. Specify K through the retrieval configuration:

```bash
aws bedrock-agent-runtime retrieve \
  --knowledge-base-id <YOUR_KB_ID> \
  --retrieval-query '{"text":"What happens if a Gold tier customer perishable shipment arrives late?"}' \
  --retrieval-configuration '{"vectorSearchConfiguration":{"numberOfResults":1}}' \
  --region us-east-1
```

Repeat with `numberOfResults` set to 3, then 5, then a higher value. The console test panel also exposes the number of retrieved results in its configuration options.

Record for each:

| K | Distinct source documents retrieved | All three facts present? | Total retrieved text | Answer correct? |
|---|---|---|---|---|
| 1 | | | | |
| 3 | | | | |
| 5 | | | | |
| higher | | | | |

Then run the full retrieve-and-generate at each K and check the answer.

### What you should see

**At K=1** the answer is almost certainly incomplete. Only one chunk was available, so at most one of the three needed facts was present. Critically, **the model does not announce the gap** — it answers confidently from what it has. This is the clearest demonstration in the whole domain that a RAG failure looks exactly like a model failure.

**Raising K improves recall.** More chunks means a higher chance the needed facts are all present. Q4 typically becomes answerable somewhere in the middle of the range.

**Raising K further stops helping, then hurts:**
- **Cost.** Every retrieved chunk is input tokens on every query. Doubling K roughly doubles the retrieval share of your input cost.
- **Latency.** More text to process before generation.
- **Context window pressure.** Chunks compete with the system prompt and conversation history for a finite budget.
- **Dilution.** With many marginally-relevant chunks present, the model may latch onto a low-relevance chunk that happens to be phrased confidently. Adding noise can make a previously correct answer wrong.

### Precision and recall

The standard framing, and it is examinable:

- **Recall** — of all the chunks that *should* have been retrieved, how many were? Raising K raises recall.
- **Precision** — of the chunks that *were* retrieved, how many were actually relevant? Raising K lowers precision.

Tuning K is choosing a point on that trade-off. There is no universally correct value.

**The asymmetry that decides it:** a fact that was never retrieved is **unrecoverable** — the model has no path to the right answer. A fact that was retrieved alongside irrelevant material is merely **more expensive**, and the model will usually still find it. So the sensible default is to **bias toward recall**, then reduce K if cost, latency or dilution become real problems.

### Beyond top-K

Two techniques you should be able to name:

- **Re-ranking.** Retrieve a generous K by vector similarity, then use a second, more accurate model to re-score those candidates and keep only the best few. This gets high recall from the first stage and high precision from the second — at the cost of an extra model call.
- **Hybrid search.** Combine vector similarity with keyword search. Pure vector search can miss exact identifiers — a part number, an error code, a policy revision number — because such strings carry little semantic meaning. Hybrid search covers that gap. Check the console for the search type options available on your knowledge base.

**Checkpoint:** You have run Q4 at several values of K, seen K=1 give a confidently incomplete answer, and can explain why the asymmetry between recall and precision favours biasing toward recall.
