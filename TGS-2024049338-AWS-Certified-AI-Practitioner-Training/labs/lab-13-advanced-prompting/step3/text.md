# Step 3 — Chain-of-thought prompting

**Chain-of-thought (CoT)** prompting asks the model to produce its intermediate reasoning before its final answer. It reliably improves accuracy on tasks that require multiple steps — arithmetic, logical deduction, and, as here, **applying several rules in sequence**.

The mechanism is worth understanding: a foundation model generates one token at a time, conditioned on everything generated so far. If it must emit a final answer immediately, it has no opportunity to work. If it emits reasoning first, that reasoning becomes context that the final answer is conditioned on.

### Zero-shot chain of thought

The simplest form is a single instruction. Add this to the end of your Step 2 prompt and re-run complaint A:

```
Before giving your answer, think through the house rules one at a time and
state whether each applies. Then give the final triage record.
```

Compare against your Step 2 result for complaint A. Look specifically for whether the model now catches **both** rules — perishable goods *and* repeat contact — rather than stopping at the first.

### Structured chain of thought

Naming the steps works better than asking the model to "think step by step", because you control the sequence:

```
Work through these steps in order and show your work under each heading.

Step 1 — Category: which of DELAY, DAMAGE, WRONG_ITEM, BILLING, OTHER fits?
Step 2 — Base severity: LOW, MEDIUM or HIGH, ignoring house rules.
Step 3 — House rule check: state each of the three house rules and whether
         it applies to this complaint.
Step 4 — Final severity after applying every rule that fired.
Step 5 — Refund decision, applying the 500 dollar threshold.
Step 6 — One-sentence internal summary.
```

Run this against **all four** complaints. For complaint C, watch Step 5 specifically: the model should hit the 500-dollar threshold and return `NEEDS_REVIEW`.

### The costs of chain of thought

CoT is not free, and the exam expects you to know the trade-offs:

- **More output tokens** — you pay for the reasoning, and output tokens are typically the more expensive kind.
- **Higher latency** — the reasoning is generated before the answer appears.
- **The reasoning is not a guarantee.** A model can produce plausible reasoning and still reach a wrong conclusion; the stated reasoning is not a verified audit trail of an internal process.
- **You usually do not want the reasoning in your final output.** Downstream systems want the record, not the workings.

### Separating reasoning from answer

The standard fix is to tag the two regions so your application can discard one:

```
Put your step-by-step working inside <reasoning> tags.
Then put the final triage record, and nothing else, inside <record> tags.
```

Run this and confirm you can see two clearly delimited regions. Your application would parse `<record>` and drop `<reasoning>` — while still keeping the accuracy benefit of having generated it, and optionally logging it for human review when a decision is disputed.

**Checkpoint:** You have run structured CoT across all four complaints, seen it catch a rule it previously missed, and produced output where reasoning and answer are separately extractable.
