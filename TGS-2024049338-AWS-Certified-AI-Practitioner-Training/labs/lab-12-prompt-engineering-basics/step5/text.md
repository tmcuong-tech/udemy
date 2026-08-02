# Step 5 — Compare, and find where more examples stop helping

You now have four rows of evidence. This step turns them into a decision.

### Score your table

For each row, count two things:

- **Accuracy** — how many of messages 1–4 got the category you would have assigned. (Message 5 is excluded; it has no single right answer.)
- **Format cleanliness** — how many of the five responses were exactly one bare category name with nothing else.

Write both numbers at the end of each row.

### The pattern you should see

In most runs of this exercise, the shape of the result is:

- **Zero-shot minimal** — poor on format, unreliable on task.
- **Zero-shot structured** — accuracy jumps sharply; format usually good.
- **One-shot** — format becomes reliable; accuracy roughly flat.
- **Few-shot** — format reliable; ambiguous case now handled predictably; accuracy on easy cases still flat.

The big win came from **structuring the prompt**, not from adding examples. Examples then delivered a second, smaller win on **consistency and edge cases**.

> This figure is illustrative teaching data, not a measurement from a benchmark run. Your own numbers may differ by model. The *shape* — a large gain from structure, then diminishing returns from examples — is the durable lesson.

### Find the point of diminishing returns

Add three more few-shot examples of easy, obvious cases to your Step 4 prompt, so you have eight examples. Re-run messages 1–5.

Ask yourself:

- Did accuracy improve? Almost certainly not — it was already at ceiling.
- Did the prompt get longer, slower and more expensive? Yes, on every call.
- Did anything get *worse*? Sometimes: a long tail of similar examples can bias the model toward a category that happens to appear most often.

This is the practical rule: **add examples until format and edge cases are stable, then stop.** More examples are not free and are not monotonically better.

### The escalation ladder

Prompt engineering sits at the bottom of a cost ladder. Work upward only when the rung below genuinely fails:

| Rung | Technique | Cost / effort | Changes model weights? |
|---|---|---|---|
| 1 | Zero-shot, well structured | Lowest | No |
| 2 | Few-shot / in-context learning | Low — but pays token cost per call | No |
| 3 | RAG (Labs 15–16) | Medium — needs a data pipeline and vector store | No |
| 4 | Fine-tuning (Lab 17) | High — needs labelled data, training, hosting | Yes |
| 5 | Continued pre-training (Lab 17) | Highest — needs a large unlabelled corpus | Yes |

A very common exam scenario describes a team that wants to fine-tune, and asks for the **lowest-cost approach that meets the need**. If the problem is format, tone, or a handful of edge cases, the answer is prompt engineering — not fine-tuning. If the problem is *missing facts*, the answer is usually RAG.

**Checkpoint:** You can state which change gave the largest quality gain, and explain why eight examples were not better than five.
