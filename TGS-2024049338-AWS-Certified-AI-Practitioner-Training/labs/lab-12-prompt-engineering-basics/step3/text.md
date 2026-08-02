# Step 3 — Zero-shot prompting

**Zero-shot** means you give the model the task and **no worked examples**. You rely entirely on what the model learned during training and on how clearly you describe the job.

Zero-shot is the right starting point for any new task. It is the cheapest prompt (fewest input tokens), the fastest to write, and the easiest to maintain. Reach for examples only when zero-shot demonstrably falls short.

### Run the zero-shot prompt on all five messages

Use the structured prompt from Step 2, swapping the `Message:` line each time. Start a **new conversation** between runs so that earlier answers do not act as accidental examples.

```
You are a support ticket triage assistant for a subscription software company.

Classify the customer message below into exactly one category.
Valid categories: BILLING, TECHNICAL, ACCOUNT, FEEDBACK.

Message: <paste message 1..5 here>

Respond with the category name only. No explanation, no punctuation.
```

Fill in the **Zero-shot, structured** row of your table.

Also run message 1 against the *minimal* prompt from Step 2 and fill in the **Zero-shot, minimal** row, so you have both.

### What to look for

Work through these questions and write the answers down — they are the actual learning in this step.

1. **Did every answer come back as exactly one of your four category names?** Or did you get `Billing`, `billing issue`, or `BILLING (duplicate charge)`?
2. **Messages 1–4 are unambiguous.** A capable model should get all four right zero-shot. If yours did, that tells you something important: for an easy, well-known task, examples may add nothing at all.
3. **Message 5 is ambiguous** — billing *and* account. Which did the model pick? Did it pick the same one when you ran it twice? Your prompt never said what to do with a message that spans two categories, so any answer is defensible. **The ambiguity is a gap in your prompt, not a defect in the model.**
4. **Casing and stray text** are the most common zero-shot failure. They are trivially fixable by a stricter output indicator, or by examples — which is where the next step goes.

### When zero-shot is enough

Zero-shot generally works well when:

- the task is common and well represented in training data (sentiment, translation, summarisation, simple classification),
- the categories or output values are self-explanatory from their names,
- you do not need a house-specific style or an unusual output format.

Zero-shot tends to struggle when:

- your labels are internal jargon the model has never seen (`TIER_2_ESCALATION`),
- the output format is idiosyncratic,
- edge cases must be resolved by a business rule the model cannot infer.

**Checkpoint:** The zero-shot rows of your table are complete and you have written down how the model handled the ambiguous message 5.
