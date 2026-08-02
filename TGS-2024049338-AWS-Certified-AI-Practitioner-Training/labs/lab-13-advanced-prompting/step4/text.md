# Step 4 — Negative prompting and constraints

**Negative prompting** tells the model what *not* to do. It is a legitimate and necessary technique, but it is weaker than positive instruction and you need to know why.

### Try it on complaint D

Complaint D is the one that tempts the model into apologising and promising a delivery date. Add explicit prohibitions:

```
Do not apologise to the customer.
Do not promise or estimate a delivery date.
Do not state a refund amount.
Do not address the customer directly in the second person.
```

Run complaint D again with these added. Record whether all four prohibitions held.

### Why negatives are weaker than positives

The instruction "do not mention a delivery date" places the concept *delivery date* in the context window. You have raised its salience while asking for its absence. In practice models comply with negative instructions less reliably than with positive ones — especially when several negatives stack up, or when the prohibited thing is exactly what the surrounding text is about.

The robust pattern is to **replace each negative with a positive that occupies the same space**:

| Weaker negative | Stronger positive replacement |
|---|---|
| Do not apologise to the customer | Write only internal notes addressed to operations staff |
| Do not promise a delivery date | For timing, write exactly: `timing: not assessed at triage` |
| Do not state a refund amount | Emit only the refund flag: YES, NO or NEEDS_REVIEW |
| Do not write in the second person | Refer to the customer in the third person as "the customer" |

Every positive here makes the prohibited output structurally impossible rather than merely discouraged. If the only field for timing is a fixed literal string, the model cannot invent a date and stay in format.

Rewrite your prohibitions as positives and re-run complaint D. Compare against the negative version. The positive version should be noticeably more reliable, and it also produces output your downstream system can validate.

### Constraints that actually bind

Ranked roughly from weakest to strongest:

1. **Politeness** — "please try to be brief". Almost no effect.
2. **Negative instruction** — "do not exceed 30 words". Some effect, inconsistently applied.
3. **Positive instruction** — "write exactly one sentence of at most 30 words". Better.
4. **Format constraint** — "output valid JSON with exactly these four keys". Strong, because deviation is visibly malformed.
5. **Enumerated value set** — "severity must be exactly one of LOW, MEDIUM, HIGH". Strongest, because the model has nowhere else to go.
6. **Validation outside the model** — your application rejects and retries anything that fails the schema. Not a prompt technique at all, and the only one that is actually a guarantee.

> **Exam point.** Prompt instructions are **steering, not enforcement**. Anything that must never happen needs a control outside the prompt — schema validation, an output filter, or Amazon Bedrock Guardrails. Lab 14 builds exactly this layered defence, and Lab 19 covers Guardrails in depth.

Note also that the max-tokens inference parameter is **not** a length constraint in this sense: it truncates output mid-sentence rather than instructing the model to be brief. To get a genuinely shorter answer you must say so in the prompt.

**Checkpoint:** You have converted four negative instructions into positives, observed the reliability difference on complaint D, and can explain why prompt constraints are steering rather than enforcement.
