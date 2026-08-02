# Step 5 — Mitigations: grounding, review and scoping

None of the limitations in Steps 3 and 4 can be removed. They are properties of how the technology works. What a competent solution does is **manage** them.

## Mitigation 1 — Grounding with RAG

**This is the primary defence against hallucination**, and it follows directly from the pattern you spotted in Step 1: the model performed well when the source material was **in the prompt**.

RAG (Retrieval Augmented Generation) makes that the architecture rather than the accident. Retrieve the relevant documents from a trusted source, put them in the prompt, and instruct the model to answer **only** from them.

**Prove it to yourself now.** Take the topic where you produced a hallucination in Step 3 and re-run it grounded:

```
Answer the question using ONLY the reference text below. If the answer
is not contained in the reference text, reply exactly "Not found in the
provided documents." Do not use any other knowledge.

REFERENCE TEXT:
<paste two or three true sentences on the topic, from a source you trust>

QUESTION:
<your Step 3 question>
```

Record what changed. You should see the model either answer correctly from your text or decline. **You have narrowed the model's job from "recall a fact" to "read this passage"** — and reading a supplied passage is a task it is genuinely good at.

Then note what grounding does **not** fix:

- If the retrieved documents are wrong or out of date, the answer is confidently wrong — grounded on bad ground
- If retrieval misses the relevant document, the model may fall back on training knowledge unless firmly instructed not to
- Grounding does nothing for bias, cost or latency, and it *increases* token usage and latency

Labs 15 and 16 build a real RAG system with Knowledge Bases for Amazon Bedrock.

## Mitigation 2 — Human review, scaled to the stakes

Not everything needs the same scrutiny. Match the review model to the consequence of being wrong:

| Risk level | Example | Review model |
|---|---|---|
| Low | Internal brainstorming, first drafts | None — the human is already the reader |
| Medium | Customer email drafts, summaries | **Human in the loop** — a person approves before it is sent |
| High | Medical, legal, financial, safety advice | Human in the loop, by a **qualified** reviewer, with the source cited |
| Unacceptable | Fully autonomous decisions affecting a person's rights, money or health | Do not automate the decision — use AI only to assist the decision-maker |

The pattern that works: **AI drafts, a human approves.** It captures most of the productivity gain while keeping accountability with a person who can be held responsible.

## Mitigations 3-6

- **Cite sources.** Require the model to quote the passage it used. This does not make it correct, but it makes checking *cheap* — and a mitigation nobody can afford to apply is not a mitigation.
- **Constrain the scope.** A narrowly scoped assistant over a known document set fails far less than a general-purpose one. Refusing out-of-scope questions is a feature.
- **Apply guardrails.** Amazon Bedrock Guardrails can filter topics, block harmful content and detect gaps in grounding, independently of the prompt. Because they sit outside the prompt, they cannot be talked out of by a user. Lab 19 covers these.
- **Set expectations with users.** Tell people they are talking to an AI, that it can be wrong, and how to escalate to a human. Undisclosed AI is a trust and, increasingly, a regulatory problem.

## Complete your record

| Limitation | Primary mitigation | What the mitigation does NOT fix |
|---|---|---|
| Hallucination | | |
| Non-determinism | | |
| Knowledge cutoff | | |
| Bias | | |
| Cost and latency | | |

**Checkpoint:** You have re-run your Step 3 hallucination with grounding, recorded what changed, and completed the mitigations table.
