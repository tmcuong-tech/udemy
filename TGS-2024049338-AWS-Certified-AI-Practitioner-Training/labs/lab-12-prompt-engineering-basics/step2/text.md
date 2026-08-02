# Step 2 — The anatomy of a prompt

A prompt is not one blob of text. It has **four parts**, and the exam expects you to name them and say what each one does.

| Part | What it is | What breaks without it |
|---|---|---|
| **Instructions** | The task you want performed | The model guesses at the task — it may summarise when you wanted classification |
| **Context** | Background the model needs: domain, audience, rules, definitions | The model applies generic world knowledge instead of your business rules |
| **Input data** | The specific thing to act on this time | Nothing to act on, or the model invents an example |
| **Output indicator** | The required shape of the answer: format, length, structure | Prose you cannot parse; inconsistent formatting between runs |

Not every prompt needs all four, but a production prompt almost always does — especially the **output indicator**, which is the part beginners most often leave out.

### See it with a minimal prompt

Run this in the playground, exactly as written:

```
Classify this: My card was charged twice for the same month.
```

This prompt has **instructions** (weakly — "classify") and **input data**. It has no context and no output indicator.

Record what you get. Typically you will see one or more of these problems:

- The model invents its own category names, which are not your four.
- It returns a paragraph explaining its reasoning instead of a label.
- It asks you a clarifying question.
- Run it again — the wording differs even at low temperature.

None of these are model failures. The model did the best it could with an underspecified request.

### Now add the missing parts

Run this version:

```
You are a support ticket triage assistant for a subscription software company.

Classify the customer message below into exactly one category.
Valid categories: BILLING, TECHNICAL, ACCOUNT, FEEDBACK.

Message: My card was charged twice for the same month.

Respond with the category name only. No explanation, no punctuation.
```

Map each line back to the anatomy:

- **Context** — "You are a support ticket triage assistant for a subscription software company."
- **Instructions** — "Classify the customer message below into exactly one category."
- **Context (constraint)** — "Valid categories: BILLING, TECHNICAL, ACCOUNT, FEEDBACK."
- **Input data** — the `Message:` line.
- **Output indicator** — "Respond with the category name only. No explanation, no punctuation."

Compare the two outputs. The second should be a single clean token you could write straight into a database column.

> **Exam point.** The constraint that made the biggest difference was not a clever technique — it was simply *telling the model what shape the answer should take*. Most real-world prompt failures are missing output indicators, not missing examples.

**Checkpoint:** You can name the four parts of a prompt and point to each one in the structured prompt above.
