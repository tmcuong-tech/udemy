# Step 4 — Interpret the results

Reading an evaluation report correctly is a skill, and misreading one is how teams ship worse systems while believing they improved them.

### Open the results

View the report in the console, and also open the raw output written to your S3 results bucket. The raw output carries **per-record** detail that the summary view aggregates away, and the per-record detail is where the understanding is.

### Read it in this order

**1. Look at the aggregate score last, not first.**

A single number across your whole dataset hides everything useful. Two models with the same average can fail on completely different records.

**2. Find your worst-scoring records and read the actual output.**

This is the essential step. For your two or three lowest-scoring records, put the generated text next to your reference and ask:

- **Is the output actually bad?** Or is it a perfectly good summary that used different words?
- **Is my reference bad?** Was it longer, shorter or stylistically different from the others?
- **Is the metric wrong for this record?**

You should find at least one record where **the low score is the metric's fault, not the model's.** That single observation is the most valuable outcome of this lab. It is why a score is evidence rather than a verdict.

**3. Find your best-scoring records and be suspicious.**

Check whether any high score came from the model **copying source text verbatim**. High overlap with a reference that itself closely tracks the source will score well while being a poor summary. High scores need scrutiny as much as low ones.

**4. Only now compare models.**

If you evaluated two models, compare per-record before comparing averages. Ask:

- Does one win consistently, or does it win on some records and lose on others?
- If they are close, what is the **cost per token** difference? A model scoring marginally lower for meaningfully less money is usually the correct production choice.
- What about **latency**? Not in the report, but it is a real requirement.

**The exam-relevant framing: model selection is a trade-off across quality, cost and latency, not a search for the highest score.** A question describing a high-volume, latency-sensitive workload with "good enough" quality requirements is pointing at the smaller, cheaper model.

### Record your findings

| Record | Score | Output actually good? | Score justified? | Why |
|---|---|---|---|---|
| Lowest | | | | |
| 2nd lowest | | | | |
| Highest | | | | |

### What automatic scores can and cannot support

**They can:**
- Detect a **regression** when something changes — the strongest everyday use.
- **Rank candidates** for a shortlist to be examined by hand.
- Provide a **repeatable** number that does not drift with the reviewer's mood.
- Run continuously in a pipeline at a cost no human process can match.

**They cannot:**
- Tell you an answer is **factually correct**.
- Detect a **hallucination** — a fabricated fact phrased similarly to the reference scores well.
- Judge **usefulness, tone or appropriateness** for your audience.
- Measure anything your reference answers did not encode.

### Use scores as a relative instrument

Do not ask "is 0.42 a good score?" — the number has no absolute meaning. Ask **"did the score change?"**

The reliable pattern: fix the dataset, fix the metric, fix the reference answers, then change **one** thing — prompt, model, top-K, chunk size — and re-run. The **delta** is trustworthy in a way the absolute value never is.

This closes the loop on the whole domain. Lab 12's prompt variants, Lab 16's top-K and chunking, and Lab 17's fine-tuning decision are all changes whose value should be established this way rather than by impression.

**Checkpoint:** You inspected per-record output, found at least one record where the score misrepresented the output quality, and can explain why a delta is more trustworthy than an absolute score.
