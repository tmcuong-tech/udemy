# Lab 12 — Prompt Engineering Basics — Zero-Shot and Few-Shot

Run one identical classification task at zero-shot, one-shot and few-shot in the Amazon Bedrock playground, and record exactly how and why the output quality changes.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 3 — Applications of Foundation Models (28%)
**Task statement:** 3.2 Choose effective prompt engineering techniques
**WSQ mapping:** LU4 · Topic 9 Essentials of Prompt Engineering · K9 · A4 · LO4
**Slide reference:** v11 deck slides 210–235
**Estimated time:** 35 minutes

**Learning objectives:**

- Identify the four components of a prompt — instructions, context, input data and output indicator — in any prompt you are shown.
- Write a zero-shot prompt and explain when zero-shot is sufficient.
- Write one-shot and few-shot prompts, and explain that in-context learning does not change model weights.
- Measure the quality difference between prompting styles on one fixed task, model and inference setting.
- Recognise the point of diminishing returns where additional examples add cost without adding accuracy.
- Place prompt engineering correctly on the customisation cost ladder against RAG and fine-tuning.

---

## Step 1 — Set up the playground and fix one task

Prompt engineering can only be learned by comparison. To compare fairly you must change **one thing at a time** — so this lab fixes the model, the inference settings and the task, and varies only the prompt.

### Open the playground

1. Sign in to the AWS Management Console and open the Amazon Bedrock console at <https://console.aws.amazon.com/bedrock/>.
2. In the **Region selector** at the top right, choose a Region where Amazon Bedrock is offered — for example **US East (N. Virginia) us-east-1**. Everything in this lab is Region-specific.
3. In the left navigation, choose **Model access** and confirm that at least one text model shows access granted. If not, request access first (this is covered in Lab 06). The Model access page is the source of truth for which models are available in your Region.
4. In the left navigation, choose the **playground** area and open the **Chat** (or **Text**) playground.
5. Choose **Select model** and pick one text model you have access to. **Write the model name down. Do not change it for the rest of this lab.**

### Fix the inference settings

Open the inference configuration panel (labelled *Configurations*, *Inference parameters* or shown behind a settings icon).

- Set **temperature** to a **low** value, near 0.
- Leave top-P as provided.
- Set maximum response length to a comfortable value — long enough that answers are not truncated.

> **Why low temperature?** A high temperature makes the model's output vary between runs. If output varies for random reasons, you cannot tell whether a change in quality came from your prompt or from sampling noise. Low temperature is the correct setting for prompt experiments.

### The task for this lab

Every prompt in this lab does the same job: **classify a short customer support message into a category**.

The categories are exactly: `BILLING`, `TECHNICAL`, `ACCOUNT`, `FEEDBACK`.

Here are the five test messages. Copy them somewhere you can reuse them:

```
1. My card was charged twice for the same month.
2. The mobile app crashes every time I open the reports tab.
3. I need to change the email address on my profile.
4. Honestly the new dashboard is a big improvement, well done.
5. I was billed after cancelling and now I cannot log in at all.
```

Message 5 is deliberately ambiguous — it touches billing *and* account access. Watch what each prompting style does with it.

### Record your results

Keep this table beside you. You will fill in one row per prompting style.

| Prompting style | Msg 1 | Msg 2 | Msg 3 | Msg 4 | Msg 5 | Format clean? |
|---|---|---|---|---|---|---|
| Zero-shot, minimal | | | | | | |
| Zero-shot, structured | | | | | | |
| One-shot | | | | | | |
| Few-shot | | | | | | |

**Checkpoint:** You have one model selected, temperature near 0, and the five test messages to hand.

---

## Step 2 — The anatomy of a prompt

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

---

## Step 3 — Zero-shot prompting

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

---

## Step 4 — One-shot and few-shot prompting

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

---

## Step 5 — Compare, and find where more examples stop helping

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

---

## Step 6 — Clean up

**Good news: this lab is serverless.** Amazon Bedrock on-demand inference leaves behind no instance, endpoint, cluster or collection. There is nothing to delete and nothing accruing an hourly charge from this lab.

Still, complete these steps:

1. **Close the playground tab.** An open playground is one stray keypress away from another billed request.
2. **Understand what you were charged for.** On-demand Bedrock billing is based on **tokens processed — input and output**. Your few-shot prompt was billed for its examples on *every* invocation. Consult the official Amazon Bedrock pricing page for current rates; do not rely on figures quoted from memory or from older course material.
3. **Leave model access as it is.** Model access is a persistent, per-account, per-Region setting. Having access enabled does **not** generate charges — only invocations do. In a shared or corporate account, follow your organisation's policy on which models may remain enabled.
4. **Set up cost visibility.** If this is your own account, enable AWS Budgets or a billing alert so unexpected usage is surfaced early. Do this once; it protects every remaining lab in this course.
5. **Keep your prompts.** Save the four prompts and your results table. Lab 13 builds directly on the structured prompt from this lab, and Lab 14 hardens it against misuse.

### Nothing to delete — but check anyway

If you explored beyond this lab's steps, look for these, because unlike on-demand inference they **do** bill continuously until deleted:

- **Provisioned throughput** for a model (Bedrock console → provisioned throughput)
- **Custom models** you created or imported
- **Knowledge bases** and their underlying vector store — an Amazon OpenSearch Serverless collection bills continuously whether or not you query it
- **SageMaker notebook instances, Studio apps or inference endpoints**

If you did not create any of these, you have nothing to remove.

**Checkpoint:** Playground closed, no provisioned throughput or custom models exist in your account, and a billing alert is in place.

---

## Verification

- [ ] You worked with **one** model and a **low temperature** throughout, and can say why holding these constant was necessary.
- [ ] You can point to instructions, context, input data and output indicator in the Step 2 structured prompt.
- [ ] Your results table has four completed rows — zero-shot minimal, zero-shot structured, one-shot, few-shot — across all five messages.
- [ ] You observed the minimal prompt produce a category name that was not one of your four valid categories, or extra text around it.
- [ ] You can state which change produced the largest quality gain, and it was structuring the prompt rather than adding examples.
- [ ] You ran the ambiguous message 5 under all four styles and can describe how few-shot made its handling predictable.
- [ ] You added three extra easy examples and confirmed accuracy did not improve.
- [ ] You can explain that few-shot prompting does not change the model's weights.

## Discussion questions

1. **In-context learning versus training.** A colleague says "we few-shot prompted the model, so now it knows our categories." Correct them precisely. What actually persists between two API calls, and what does not? What does this imply about where the cost of few-shot prompting lands?

2. **Choosing the cheapest sufficient technique (Task 3.2).** A support team reports three separate problems: (a) the model returns categories in inconsistent casing, (b) the model cannot classify tickets that reference a product feature launched last month, and (c) the model does not know the team's internal escalation rules. For each, say whether prompt engineering, RAG or fine-tuning is the right response, and justify your choice on cost and effort.

3. **Designing the example set.** You have budget for exactly three few-shot examples. Your label space has four categories and one known ambiguity. Which three examples do you choose, and what are you deliberately giving up? What could go wrong if all three examples happened to be from the same category?

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.
