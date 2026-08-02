# Step 5 — Apply the decision to real scenarios

Everything so far was preparation for this. Work through each scenario, choose an approach, and justify it. These are written in the style of exam questions and the reasoning is what matters.

For each, ask in order:

1. What is the **actual complaint** — missing knowledge, or wrong behaviour?
2. Would the **cheapest** option plausibly fix it?
3. What is the **volume**, and does it justify provisioned throughput?
4. Are there **freshness, citation or access control** requirements that force RAG?

---

**Scenario A.** A bank's support chatbot answers general questions well but does not know the bank's current fee schedule, which changes quarterly. Compliance requires that every answer cite the document it came from.

*Consider:* the complaint is missing knowledge. The data changes quarterly. Citations are mandatory. Which two of these three points on their own rule out fine-tuning?

---

**Scenario B.** A law firm's assistant produces correct content but in a style that reads as generic. Partners want it to follow the firm's house drafting conventions. There are about 40 documents a day, and roughly 200 well-edited past documents available as examples.

*Consider:* the complaint is behaviour, not knowledge — which points at fine-tuning. But: is 40 documents a day enough volume to justify provisioned throughput? Have they tried a detailed style guide in the system prompt with few-shot examples? What would you insist they do **first**, and what evidence would justify escalating?

---

**Scenario C.** A medical research tool must interpret highly specialised clinical terminology. The base model does not appear to understand the vocabulary at all — not just phrasing it oddly, but misreading terms. The organisation holds a large archive of unlabelled clinical literature.

*Consider:* a large **unlabelled** corpus and a **vocabulary comprehension** failure. Which of the four options does that combination point to, and why is it neither fine-tuning nor RAG? What would you check before committing, given this is the most expensive option available?

---

**Scenario D.** A retailer processes 50,000 product descriptions a day. The prompt is long — a detailed style guide plus eight few-shot examples — and token cost is now a significant line item. Output quality is already acceptable.

*Consider:* quality is fine, so this is purely economic. Fine-tuning could bake the style into the weights, allowing a much shorter prompt. Weigh the saved input tokens across 50,000 daily requests against provisioned throughput and retraining. This is the scenario where fine-tuning is most likely to be right — why?

---

**Scenario E.** A startup's assistant must answer from its own documentation *and* respond in a distinctive brand voice. It has 500 documentation pages and 300 examples of on-brand replies.

*Consider:* two different complaints — missing knowledge and wrong behaviour. Does one approach cover both? What does the phrase "RAG for knowledge, fine-tuning for behaviour" tell you here, and in what order would you build them?

---

### Answers to check yourself against

**A — RAG.** Quarterly change and mandatory citations each independently rule out fine-tuning: fine-tuning cannot cite, and updating a fact means retraining.

**B — Prompt engineering first.** Behaviour is the fine-tuning signal, but 40 documents a day is nowhere near the volume to justify provisioned throughput, and 200 examples is thin. A detailed style guide plus few-shot examples should be attempted and *measured* before escalating. Escalate only if measured quality remains inadequate at realistic volume.

**C — Continued pre-training.** A large unlabelled corpus and a comprehension-level vocabulary failure is the defining case. Before committing, verify that the failure really is comprehension and not retrieval — and confirm no domain-adapted model already exists that would be cheaper than training one.

**D — Fine-tuning.** Very high sustained volume, a purely economic driver, stable requirements, and a long prompt to eliminate. This is the profile where provisioned throughput's flat cost beats linear on-demand cost, and where a shorter prompt compounds across 50,000 daily calls.

**E — RAG first, then consider fine-tuning.** RAG handles the documentation; brand voice should be attempted with prompt engineering first. If voice remains inadequate at volume, add fine-tuning **alongside** RAG. They are complementary, not alternatives.

### The summary you should be able to reproduce

| Symptom | First response |
|---|---|
| Does not know our facts | RAG |
| Facts change frequently | RAG |
| Must cite sources | RAG |
| Different users see different data | RAG with metadata filtering |
| Wrong format or tone | Prompt engineering |
| Inconsistent behaviour at low volume | Prompt engineering |
| Consistent house behaviour at very high volume | Fine-tuning |
| Prompt too long, cost dominated by input tokens at scale | Fine-tuning |
| Does not understand the domain's language at all | Continued pre-training |
| Both facts and behaviour | RAG plus prompt engineering, fine-tuning only if measured need |

**Checkpoint:** All five scenarios answered with reasoning, and you can reproduce the symptom-to-response table.
