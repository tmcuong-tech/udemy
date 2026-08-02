# Step 4 — One-shot and few-shot prompting

Adding worked examples to a prompt is called **in-context learning**. The model is not retrained and its weights do not change — the examples simply sit in the context window and steer the response.

- **One-shot** — exactly one example.
- **Few-shot** — a small number of examples, typically two to five.

This distinction is examinable, and the counting is on **examples of the task**, not on the number of instructions.

### One-shot

Run this, substituting each of the five messages in turn:

```
You are a support ticket triage assistant for a subscription software company.

Classify the customer message into exactly one category.
Valid categories: BILLING, TECHNICAL, ACCOUNT, FEEDBACK.

Message: The invoice PDF shows the wrong company name.
Category: BILLING

Message: <paste message 1..5 here>
Category:
```

Two things changed, and both matter:

- The single example **demonstrates the output format** far more precisely than a sentence describing it. The model sees `BILLING` in capitals with nothing after it.
- The trailing `Category:` is an **output indicator by prefix** — the model completes the pattern rather than starting a new sentence.

Fill in the **One-shot** row of your table.

### Few-shot

Now give one example **per category**, and include an example that resolves the ambiguity:

```
You are a support ticket triage assistant for a subscription software company.

Classify the customer message into exactly one category.
Valid categories: BILLING, TECHNICAL, ACCOUNT, FEEDBACK.
If a message spans more than one category, choose the one that blocks the
customer most urgently.

Message: The invoice PDF shows the wrong company name.
Category: BILLING

Message: Export to CSV returns an empty file on Safari.
Category: TECHNICAL

Message: Please add my colleague as a second admin user.
Category: ACCOUNT

Message: The onboarding flow was much clearer than last year.
Category: FEEDBACK

Message: My payment failed and now the app will not open.
Category: ACCOUNT

Message: <paste message 1..5 here>
Category:
```

Fill in the **Few-shot** row.

### What the examples actually bought you

Compare your four rows now and note specifically:

1. **Format consistency.** Few-shot output is usually the most uniform. Examples pin down format better than prose instructions do.
2. **Message 5.** Its handling should now be *stable and predictable*, because the fifth example demonstrates the tie-break rule on a near-identical case. Note that the improvement came from the combination of a stated rule *and* an example of it — either alone is weaker.
3. **Messages 1–4.** Very likely unchanged from zero-shot. Examples did not make an easy case easier.

### Choosing and ordering examples

Example quality matters more than example count:

- **Cover your label space.** An unrepresented category is one the model will under-predict.
- **Keep the label distribution sane.** Four `BILLING` examples and one `TECHNICAL` biases the model towards `BILLING`.
- **Use examples for the hard cases**, not the obvious ones. The fifth example above earns its tokens; an example reading *"My card was charged twice → BILLING"* would not.
- **Be consistent in formatting.** If one example ends with a full stop and another does not, you have taught the model that it may vary.
- **Examples cost tokens on every single call.** A five-example prompt is charged for those examples each time it runs, and it consumes context window that longer inputs might need.

**Checkpoint:** All four rows of your table are complete for all five messages.
