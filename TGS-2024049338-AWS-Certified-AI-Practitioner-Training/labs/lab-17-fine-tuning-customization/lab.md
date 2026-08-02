# Lab 17 — Fine-Tuning and Model Customisation

Prepare a fine-tuning dataset and walk through a Bedrock custom model job configuration without submitting it, then decide between prompt engineering, RAG, fine-tuning and continued pre-training on cost, effort and data.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 3 — Applications of Foundation Models (28%)
**Task statement:** 3.3 Describe the training and fine-tuning process for foundation models
**WSQ mapping:** LU5 · Topic 10 Optimizing Foundation Models · K10 · A5 · LO5
**Slide reference:** v11 deck slides 236–247
**Estimated time:** 40 minutes

> ## ⚠️ DO NOT SUBMIT THE JOB AND DO NOT PURCHASE PROVISIONED THROUGHPUT
>
> In Amazon Bedrock a **custom model cannot be invoked on demand** — serving it requires **provisioned throughput**, purchased in model units for a committed term. It is **far more expensive than anything else in this course**, it bills whether or not you send a request, and a term commitment generally cannot be cancelled early.
>
> **You will fill in every configuration screen and stop at the final button.** Do not choose Create, Submit, Start, Purchase or Confirm. Everything examinable in Task 3.3 lives in the configuration, the data preparation and the trade-off analysis — none of it requires running a job. In a shared classroom account, do not open the provisioned throughput purchase flow without your trainer present.

**Learning objectives:**

- Compare prompt engineering, RAG, fine-tuning and continued pre-training on weights, data, labelling, time, cost and citations.
- State the supervised versus unsupervised distinction between fine-tuning and continued pre-training.
- Prepare a valid JSONL training and validation dataset and apply the data quality rules that decide success.
- Explain every field of a Bedrock custom model job, including epochs, learning rate and overfitting.
- Explain why a custom model requires provisioned throughput and how that inverts Bedrock's usual cost model.
- Choose the cheapest sufficient customisation approach for a described scenario and justify it.
- Verify that no customisation job, custom model or provisioned throughput exists in your account.

---

## Step 1 — The customisation decision

## ⚠️ How this lab works — read first

**You will configure a fine-tuning job but you will NOT submit it, and you will NOT purchase provisioned throughput.**

This is deliberate, and it is not a shortcut. In Amazon Bedrock, a **custom model cannot be invoked on demand** — running inference against one requires **provisioned throughput**, which is purchased in model units for a committed term. It is **substantially more expensive than anything else in this course**, it commits you for the duration, and there is no meaningful free tier for it.

A single learner who provisions throughput in class can incur a bill far larger than every other lab in this course combined.

**So: walk through the configuration screens, fill them in, understand every field — and stop at the final button. Do not submit the training job. Do not purchase provisioned throughput.** This is stated again at each point where it matters.

Everything examinable about Task 3.3 is in the configuration, the data preparation and the trade-off analysis. None of it requires you to actually run a job.

---

## The four customisation options

Ordered by cost and effort. The exam tests whether you can pick the **cheapest option that actually solves the stated problem** — a question type that appears repeatedly.

### 1. Prompt engineering

Change the text you send. No training, no infrastructure, effect is immediate.

- **Changes weights:** no
- **Needs data:** no, or a handful of examples
- **Time to first result:** minutes
- **Cost:** tokens only; few-shot examples are paid for on every call
- **Fixes:** output format, tone, task framing, edge case handling

### 2. RAG

Retrieve relevant documents at query time and insert them into the prompt.

- **Changes weights:** no
- **Needs data:** a document corpus, no labelling
- **Time to first result:** hours
- **Cost:** vector store hourly, plus embedding and retrieval tokens per query
- **Fixes:** the model does not know your facts, your facts change often, you need citations

### 3. Fine-tuning

Continue training a pre-trained model on **labelled examples of your task** — prompt and completion pairs. This is **supervised** learning.

- **Changes weights:** yes
- **Needs data:** typically hundreds to thousands of labelled examples, curated
- **Time to first result:** days to weeks including data preparation
- **Cost:** training compute, plus **provisioned throughput to serve it**
- **Fixes:** consistent house style at scale, a specialised task shape, domain vocabulary, shorter prompts for high-volume workloads

### 4. Continued pre-training

Continue the original **unsupervised** pre-training objective on a large corpus of your **unlabelled** domain text.

- **Changes weights:** yes
- **Needs data:** large volumes of unlabelled domain text — a corpus, not a labelled set
- **Time to first result:** weeks
- **Cost:** the highest of the four, plus provisioned throughput
- **Fixes:** the model does not understand your **domain language** at all — highly specialised medical, legal or scientific vocabulary

### The distinction that gets tested

**Fine-tuning is supervised and uses labelled prompt–completion pairs. Continued pre-training is unsupervised and uses unlabelled raw text.** If a question mentions labelled examples of a task, it is fine-tuning. If it mentions a large body of domain documents with no labels, it is continued pre-training.

### The comparison table

| | Prompt engineering | RAG | Fine-tuning | Continued pre-training |
|---|---|---|---|---|
| Weights changed | No | No | Yes | Yes |
| Data needed | None to a few examples | Document corpus | Hundreds to thousands of labelled pairs | Large unlabelled corpus |
| Labelling required | No | No | **Yes** | **No** |
| Learning type | — | — | Supervised | Unsupervised |
| Time | Minutes | Hours | Days to weeks | Weeks |
| Adds new facts | No | **Yes** | Poorly | Somewhat |
| Update a fact | — | Re-sync, seconds | Retrain | Retrain |
| Citations | No | **Yes** | No | No |
| Serving cost | On demand | On demand | **Provisioned throughput** | **Provisioned throughput** |

### The heuristic

**RAG changes what the model knows. Fine-tuning changes how the model behaves.**

If the complaint is *"it does not know our data"* → **RAG**.
If the complaint is *"it does not sound like us"* or *"it will not stick to our format"* → **prompt engineering first, fine-tuning only if that genuinely fails**.
If the complaint is *"it does not understand our field's language at all"* → **continued pre-training**, and this is rare.

**And they combine.** A production system commonly fine-tunes for behaviour and uses RAG for facts. These are not competing choices.

**Checkpoint:** You can state the supervised versus unsupervised distinction between fine-tuning and continued pre-training, and you understand that you will not submit a job or provision throughput in this lab.

---

## Step 2 — Prepare a fine-tuning dataset

Most of the effort and most of the risk in fine-tuning lives here, not in the training job. A team that budgets for compute and not for data preparation has mis-planned the project.

### The format

Bedrock fine-tuning datasets are **JSONL** — JSON Lines. One complete JSON object per line, no commas between lines, no wrapping array. A single stray blank line or trailing comma fails validation.

For text-to-text fine-tuning each record pairs an input with the desired output. The exact key names depend on the model you are customising — **the console shows the required schema for your selected model, and that is the authoritative source.** A common shape is:

```json
{"prompt": "Classify: My card was charged twice.", "completion": "BILLING"}
{"prompt": "Classify: The app crashes on the reports tab.", "completion": "TECHNICAL"}
{"prompt": "Classify: Please change my profile email.", "completion": "ACCOUNT"}
```

Do not type key names from memory in an exam or in production — read the schema the console shows for the model you picked.

### Build a small dataset

Create `northwind-train.jsonl`. Use the Lab 13 triage task, with the completion being the structured record you want the model to learn to produce.

```json
{"prompt": "Assess this delivery complaint: My frozen seafood arrived at room temperature. Order value 180 dollars.", "completion": "{\"category\":\"DAMAGE\",\"severity\":\"HIGH\",\"refund_warranted\":\"YES\",\"summary\":\"Perishable shipment arrived at ambient temperature; temperature excursion.\"}"}
{"prompt": "Assess this delivery complaint: The box was dented but the contents seem fine.", "completion": "{\"category\":\"DAMAGE\",\"severity\":\"LOW\",\"refund_warranted\":\"NO\",\"summary\":\"Cosmetic packaging damage; contents undamaged.\"}"}
{"prompt": "Assess this delivery complaint: I ordered a laptop stand and received a keyboard. Value 620 dollars.", "completion": "{\"category\":\"WRONG_ITEM\",\"severity\":\"MEDIUM\",\"refund_warranted\":\"NEEDS_REVIEW\",\"summary\":\"Incorrect item despatched; value above review threshold.\"}"}
```

Note that the JSON in `completion` is escaped, because it is a string value inside the outer JSON object. Getting this wrong is one of the most common validation failures.

Also create a small `northwind-validation.jsonl` in the same format with **different** examples. Validation data must never overlap with training data — if it does, your reported validation loss is measuring memorisation, and it will look excellent while telling you nothing.

Upload both:

```bash
aws s3 cp northwind-train.jsonl      s3://<your-bucket>/finetune/
aws s3 cp northwind-validation.jsonl s3://<your-bucket>/finetune/
```

Three records will not train anything useful. This is a format exercise — the volume discussion follows.

### How much data do you actually need?

There is no universal number, and any specific figure you have memorised is probably wrong for your model. What you can rely on:

- Fine-tuning needs **substantially more** than few-shot prompting — hundreds to thousands of examples rather than three to five.
- Bedrock enforces **minimum and maximum record counts that vary by model**. The console states the limits for your selected model; read them there.
- **Quality dominates quantity.** A few hundred consistent, correct examples beat several thousand noisy ones. Inconsistent labelling is worse than less data, because you are actively teaching the model to be inconsistent.

### Data quality rules that decide success or failure

1. **Be consistent.** If two near-identical complaints carry different labels, you are teaching contradiction. Have a second person re-label a sample and measure agreement before training.
2. **Represent your real distribution.** Training only on clear-cut cases produces a model that fails on exactly the ambiguous ones you needed help with.
3. **Cover every output class.** An absent class will effectively never be produced.
4. **Match the format exactly.** Every completion must have identical structure. Fine-tuning is highly sensitive to formatting inconsistency — this is what it learns most readily.
5. **Split train and validation properly.** No overlap, and validation should reflect the same distribution.
6. **Remove PII and sensitive data.** This is a governance requirement, and it is more serious than for RAG: RAG context is transient, but **fine-tuning data is absorbed into the weights**. You cannot delete a record from a trained model — you retrain. Amazon Macie can help identify sensitive data in S3 before training; see Lab 24.
7. **Check for bias.** Historical labelling reflects historical decisions, including biased ones. Fine-tuning bakes them in and makes them harder to detect. SageMaker Clarify addresses this; see Lab 20.
8. **Know your data provenance and licensing.** Confirm you have the right to train on it.

> **This is the honest cost of fine-tuning.** Curating, labelling, checking and de-biasing a dataset takes a team weeks. It is usually the largest line item, and it is almost always underestimated in project plans.

**Checkpoint:** Valid JSONL training and validation files created and uploaded, with no overlap between them, and you can list at least five data quality rules.

---

## Step 3 — Configure a custom model job — DO NOT SUBMIT

> ## ⚠️ STOP BEFORE THE FINAL BUTTON
>
> Walk through every screen and fill in every field. **Do not choose Create, Submit or Start.** A training job incurs charges, and the custom model it produces can only be served through provisioned throughput, which is the expensive commitment described in Step 4.
>
> The whole of Task 3.3 is in understanding these fields. Submitting the job teaches you nothing further and costs real money.

### Open the configuration

1. Open the Bedrock console at <https://console.aws.amazon.com/bedrock/> and check your Region. **Model customisation is not offered in every Region, and the models available for customisation are a subset of those available for inference.** The console tells you what is offered where you are.
2. In the left navigation, find the **custom models** area and begin creating a customisation job.

### Field by field

**Job type — fine-tuning or continued pre-training.**

This is the first and most consequential choice, and it is the Step 1 distinction made concrete. Select **fine-tuning** — you have labelled prompt–completion pairs. Continued pre-training would expect unlabelled text and a much larger corpus.

**Base model.**

Choose the model to customise. Only some models support customisation, and the set differs by Region. Note two things:

- Your custom model is **derived from a specific version** of the base model. When the provider releases a newer base version, your customisation does **not** carry over — you retrain. This is real, recurring maintenance cost.
- Different base models expect different training data schemas. Changing base model may mean reformatting your dataset.

**Custom model name and job name.**

Name them so you can identify them later. A job that fails at 3am is much easier to investigate when it is not called `job-3`.

**Encryption.**

You can supply a KMS key to encrypt the custom model artefacts. **Your training data becomes part of the model's weights**, so if that data is sensitive, this is not optional. See Lab 23.

**Input data — training and validation.**

Point at the S3 locations of the two JSONL files from Step 2. The console shows the required schema for your selected base model — read it and confirm your files match. Format errors are caught at validation, after the job has started, so check before submitting.

**Hyperparameters.**

The set offered depends on the model. You will typically be able to configure some of:

| Hyperparameter | What it controls | Failure mode at the wrong value |
|---|---|---|
| **Epochs** | How many complete passes over the training data | Too few: undertrained, no behaviour change. Too many: **overfitting** — memorises training data, performs worse on new input |
| **Batch size** | Examples processed before each weight update | Affects stability and memory; interacts with learning rate |
| **Learning rate** | Size of each weight update | Too high: unstable, may destroy existing capability. Too low: slow, may never converge |
| **Learning rate warmup steps** | Gradual ramp of learning rate at the start | Improves early stability |

**Leave these at their defaults for a first run.** Defaults are chosen by the model provider to be reasonable, and changing several at once means you cannot attribute any result to any change.

**Overfitting is the concept to hold on to.** The model learns the training examples so specifically that it generalises worse. The symptom is training loss continuing to fall while validation loss flattens or rises — which is precisely why the validation set exists and why it must not overlap the training set.

**Output data.**

An S3 location for training metrics and artefacts. **Do check this after any real job** — the training and validation loss curves are the primary evidence of whether training worked or overfitted.

**Service role.**

The job needs to read your S3 input, write output, and access the base model. Let the console create a role unless your organisation requires otherwise.

### Now stop

**Review the summary page. Read every value. Then leave the page without submitting.**

Confirm nothing was created:

```bash
aws bedrock list-model-customization-jobs --region us-east-1
aws bedrock list-custom-models --region us-east-1
```

Both should return empty. If either does not, you submitted a job — go to Step 6 immediately and stop it.

### What would happen if you did submit

For completeness, since the exam may describe it:

1. The job validates the dataset format. Malformed JSONL fails here.
2. Training runs for hours, longer with more data or more epochs.
3. Loss metrics are written to your S3 output location.
4. On success, a **custom model** appears in your account.
5. **That custom model cannot be invoked on demand.** To use it at all you must first purchase provisioned throughput. Which is Step 4.

**Checkpoint:** You walked every configuration screen, can explain epochs, learning rate and overfitting, and both list commands return empty because you submitted nothing.

---

## Step 4 — Provisioned throughput, and why you stop here

> ## ⚠️ DO NOT PURCHASE PROVISIONED THROUGHPUT IN THIS LAB
>
> You may open the configuration screen to see the fields. **Do not choose Purchase, Confirm or Create.** This is the single most expensive action available anywhere in this course, and unlike most AWS resources it may involve a **term commitment you cannot simply delete your way out of**.
>
> If you are in a shared classroom account, do not open the purchase flow at all without your trainer present.

### The constraint that shapes everything

On-demand inference against a base model is **serverless and per-token**. No commitment, no idle cost. That is what every earlier lab in this course used.

**A custom model does not work that way.** Once you fine-tune, you own a model artefact that no shared serving fleet hosts. To invoke it, capacity must be dedicated to you — and you pay for that capacity **whether or not you send it a single request**.

This is purchased as **provisioned throughput**, in **model units**. A model unit represents a quantum of dedicated capacity with an associated throughput ceiling.

### The three things to understand

**1. You pay for time, not for use.** Provisioned throughput bills for the duration it exists. A model unit sitting idle overnight costs the same as one running at capacity. This inverts the economics you have internalised from every other Bedrock lab.

**2. Commitment terms.** Provisioned throughput can be purchased with no commitment or with a longer commitment term at a lower rate. **A term commitment cannot generally be cancelled early.** Choosing a one-month or six-month term to save money is a decision you live with for that period. Read the terms shown on screen carefully.

**3. It is the dominant cost of fine-tuning.** Teams routinely budget for the training job — a one-off — and are surprised by serving. **Serving is the recurring cost, and it is usually much larger over any realistic time horizon.**

### Do the arithmetic yourself

Rather than quote figures that would be out of date, look them up:

1. Open the official Amazon Bedrock pricing page and find the provisioned throughput rates for a model in your Region.
2. Compute the cost of **one model unit for one month with no commitment**.
3. Find the on-demand price per thousand input and output tokens for the same model family.
4. Work out **how many on-demand requests you could make for the same money**, using your own estimate of tokens per request.

Almost everyone is surprised by the answer. Write your number down; it is the most useful thing you will take from this step.

### The break-even question

Provisioned throughput becomes rational at **sustained high volume**. The reasoning:

- On-demand cost scales **linearly** with requests. Ten times the traffic, ten times the bill.
- Provisioned cost is **flat**. Ten times the traffic on the same units costs the same, until you hit the throughput ceiling.

So there is a crossover. **Below it, on-demand wins. Above it, provisioned wins.** And an intermittent workload — busy for two hours, idle for twenty-two — sits badly on provisioned throughput, because you pay for the idle twenty-two.

Note that provisioned throughput is also available for **base** models, where it buys predictable latency and guaranteed capacity rather than being a precondition for using the model at all. For a custom model it is not a choice — it is the only path to inference.

### What this means for the customisation decision

Now revisit Step 1 with this knowledge. The full cost of fine-tuning is:

```
data curation and labelling   (weeks of human effort — usually the largest hidden cost)
+ training job                (one-off compute)
+ provisioned throughput      (RECURRING, and it dominates)
+ retraining                  (when the base model version moves on)
+ evaluation                  (Lab 18 — you must prove it improved anything)
```

Against prompt engineering, whose cost is an afternoon of an engineer's time and some extra tokens per call.

> **The exam-relevant conclusion.** When a question describes a team wanting to customise a model and asks for the most cost-effective approach, the presence of provisioned throughput in the fine-tuning path is usually what decides it. Fine-tuning is justified by **sustained high volume** plus a behavioural requirement that prompting genuinely cannot meet — not by a preference for having a custom model.

### Verify you purchased nothing

```bash
aws bedrock list-provisioned-model-throughputs --region us-east-1
```

**This must return empty.** If it does not, go to Step 6 immediately.

**Checkpoint:** You can explain why a custom model cannot be served on demand, you have calculated the on-demand equivalent of one model unit for one month, and `list-provisioned-model-throughputs` returns empty.

---

## Step 5 — Apply the decision to real scenarios

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

---

## Step 6 — Clean up

If you followed the lab, **you created almost nothing** — which was the point. Verify that, then remove the small amount that does exist.

### 1. Verify nothing expensive was created

Run all three. **All three must return empty.**

```bash
aws bedrock list-model-customization-jobs --region us-east-1
aws bedrock list-custom-models --region us-east-1
aws bedrock list-provisioned-model-throughputs --region us-east-1
```

Check **every Region you opened the console in**, since these are Region-scoped and it is easy to have switched Regions while looking for customisation support.

### 2. If a training job is running — stop it now

If `list-model-customization-jobs` shows a job in progress, it is accruing training charges. Stop it:

```bash
aws bedrock stop-model-customization-job \
  --job-identifier <JOB_NAME_OR_ARN> \
  --region us-east-1
```

Or use the console: open the custom models area, select the job, and stop it. Then re-run the list command to confirm.

### 3. If a custom model exists — delete it

A custom model is a stored artefact. Delete it in the console, or:

```bash
aws bedrock delete-custom-model --model-identifier <MODEL_NAME> --region us-east-1
```

### 4. If provisioned throughput exists — this is urgent

**This is the expensive one and it bills continuously.**

```bash
aws bedrock list-provisioned-model-throughputs --region us-east-1
```

If anything is listed, delete it immediately:

```bash
aws bedrock delete-provisioned-model-throughput \
  --provisioned-model-id <PROVISIONED_MODEL_ID> \
  --region us-east-1
```

**If it was purchased with a commitment term, deletion may not stop the committed charges.** If this has happened in your own account, check the Billing console to understand your exposure and contact AWS Support. Do not assume that deleting the resource ends the obligation.

Re-run the list command and confirm it is empty.

### 5. Remove the training data

The JSONL files are tiny, but tidy up:

```bash
aws s3 rm s3://<your-bucket>/finetune/ --recursive
```

If the bucket has no other purpose, remove it entirely:

```bash
aws s3 rb s3://<your-bucket>
```

**If your training data contained anything sensitive**, deleting it from S3 is the right step here. Note the broader point from Step 2 though: had you actually trained on it, the data would be reflected in the model's weights and deleting the source file would not remove it. That asymmetry — RAG context is transient, training data is permanent — is a governance distinction worth carrying forward.

### 6. Remove the IAM role

If the console created a service role while you walked the configuration, delete it from <https://console.aws.amazon.com/iam/>. It does not bill, but it has S3 and Bedrock permissions with no remaining purpose.

### 7. Confirm the knowledge base from Labs 15 and 16 is gone

The most common source of an unexpected bill at this point in the course is a leftover vector store:

```bash
aws bedrock-agent list-knowledge-bases --region us-east-1
aws opensearchserverless list-collections --region us-east-1
```

Both should be empty, in every Region you used. If not, return to Lab 16 Step 6.

### Final checklist

- [ ] No model customisation jobs, in any Region
- [ ] No custom models, in any Region
- [ ] **No provisioned model throughputs, in any Region**
- [ ] Training and validation JSONL removed from S3
- [ ] IAM service role deleted
- [ ] No knowledge bases and no OpenSearch Serverless collections remaining

**Checkpoint:** All three Bedrock list commands return empty in every Region you used, and the Labs 15–16 knowledge base and vector store are confirmed gone.

---

## Verification

- [ ] You did **not** submit a training job and did **not** purchase provisioned throughput.
- [ ] You can complete the four-way comparison table from memory on weights, data, labelling, time, citations and serving cost.
- [ ] You can state that fine-tuning is supervised on labelled pairs and continued pre-training is unsupervised on unlabelled text.
- [ ] You created valid JSONL training and validation files with no overlap between them.
- [ ] You can list at least five data quality rules and explain why validation data must not overlap training data.
- [ ] You can explain why fine-tuning data is a greater governance concern than RAG data.
- [ ] You walked every field of the custom model job configuration and can explain epochs, learning rate and batch size.
- [ ] You can define overfitting and name the symptom that reveals it in the loss curves.
- [ ] You can explain why a custom model cannot be served on demand.
- [ ] You calculated how many on-demand requests equal one model unit for one month.
- [ ] You answered all five scenarios and can reproduce the symptom-to-response table.
- [ ] `list-model-customization-jobs`, `list-custom-models` and `list-provisioned-model-throughputs` all return empty, in every Region you used.
- [ ] No knowledge base or OpenSearch Serverless collection remains from Labs 15 and 16.

## Discussion questions

1. **The hidden cost (Task 3.3).** A project plan budgets for the training job and nothing else. Name every other cost the plan has omitted, order them by likely size, and identify which one most often kills fine-tuning projects after they have already started. Why is that particular cost so consistently underestimated?

2. **Data governance and permanence.** A customer exercises a right to erasure. Their data is in your RAG knowledge base and also in the dataset used to fine-tune your production model. Describe what happens in each case and why they differ fundamentally. What does that difference imply about how you should screen data *before* training?

3. **Making the case honestly.** Your team wants to fine-tune because output tone is inconsistent. Design the experiment that would establish whether prompt engineering can meet the requirement instead. What would you measure, on what test set, and what specific result would justify the escalation to fine-tuning? Connect this to the evaluation methods in Lab 18.

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.
