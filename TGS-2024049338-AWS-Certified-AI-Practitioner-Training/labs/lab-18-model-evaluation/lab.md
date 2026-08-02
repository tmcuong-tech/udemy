# Lab 18 — Evaluating Foundation Model Performance

Run an Amazon Bedrock automatic model evaluation job against your own dataset, interpret the results critically, and place ROUGE, BLEU, BERTScore, benchmarks, human review and business metrics in a complete evaluation strategy.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 3 — Applications of Foundation Models (28%)
**Task statement:** 3.4 Describe methods to evaluate foundation model performance
**WSQ mapping:** LU5 · Topic 10 Optimizing Foundation Models · K10 · A5 · LO5
**Slide reference:** v11 deck slides 248–271
**Estimated time:** 40 minutes

> **Cost note.** A model evaluation job runs inference on every prompt in your dataset against every model selected, so cost scales with records multiplied by models. Keep the dataset to eight or ten records and select at most two models. A job is not a continuously-billing resource — it runs, finishes, and stops charging. Human-based evaluation additionally costs human worker time. Check the official Amazon Bedrock pricing page for current rates.

**Learning objectives:**

- Explain why generative output resists the accuracy metrics used for classification.
- State for ROUGE, BLEU, BERTScore, perplexity and F1 the task each belongs to, its orientation, and its limitation.
- Explain why no automatic metric detects hallucination.
- Build a JSONL evaluation dataset with consistent reference answers and run a Bedrock automatic evaluation job.
- Interpret a report per record rather than by aggregate, and identify a score that misrepresents output quality.
- Configure human evaluation and explain why comparative rating beats absolute rating.
- Name the major benchmark suites, including what makes HELM distinctive, and state where benchmarks should not be used.
- Identify the business metrics that actually justify a generative AI project.

---

## Step 1 — Why evaluate, and build a test set

### The question this lab answers

Every earlier lab in this domain ended with a change you *believed* was an improvement. A better prompt. More few-shot examples. A higher top-K. A fine-tuned model.

**How do you know?**

"It looked better when I tried it" is the default state of most generative AI projects, and it is not good enough to justify a fine-tuning budget, to pass a compliance review, or to decide between two models. Evaluation replaces impression with evidence.

Three decisions that require it:

1. **Model selection.** Which of several foundation models should we use? They differ in quality, latency and cost per token, and the cheapest adequate model is usually the right answer — but only if you can show it is adequate.
2. **Change validation.** Did this prompt change, RAG tuning or fine-tune actually improve anything, or did it improve the three examples I happened to look at while breaking others?
3. **Regression detection.** When we switch model versions, does quality hold? Providers release new versions and you do not control that timing.

### Why generative output is hard to evaluate

Classification has a right answer, so accuracy, precision, recall and F1 apply cleanly. Generation does not: there are many acceptable summaries of one document, and a good answer may share almost no wording with your reference answer.

This forces three families of method, and the exam expects you to know all three and their limits:

| Family | What it does | Strength | Weakness |
|---|---|---|---|
| **Automatic metrics** | Compare output to a reference text algorithmically | Cheap, fast, repeatable, scales | Measures overlap, not correctness or usefulness |
| **Human evaluation** | People rate outputs against criteria | Captures what actually matters | Slow, expensive, subjective, hard to reproduce |
| **Benchmarks** | Standard datasets and tasks with published results | Comparable across models, no setup | Generic — may not reflect your task; risk of contamination |

In practice you use automatic metrics for fast iteration and regression detection, benchmarks for initial model shortlisting, and human evaluation for the decisions that matter.

### Cost note

Model evaluation jobs in Bedrock incur charges: **inference cost** for every prompt in the dataset against every model evaluated, and, for human evaluation, the cost of the human workers. Keep your dataset small in this lab. Check the official Amazon Bedrock pricing page for current rates.

An evaluation job is not a continuously-billing resource like a vector store — it runs, it finishes, it stops charging. But an evaluation with a large dataset across several models can still produce a surprising bill, because cost scales with dataset size multiplied by model count.

### Build a test set

Use summarisation, because it has clear reference answers and is the natural home for ROUGE.

Create `eval-prompts.jsonl`. Bedrock evaluation datasets are **JSONL**, one record per line. The exact schema depends on the task type you select — **the console shows the required format for your chosen task type and metric, and that is authoritative.** A record typically carries the prompt, an optional category, and the reference answer:

```json
{"prompt": "Summarise in one sentence: Northwind Logistics offers standard delivery within Singapore in 2 working days, and 5 working days to Malaysia and Indonesia. Express delivery is Singapore only, next working day for orders before 1400.", "category": "shipping", "referenceResponse": "Northwind delivers in 2 days domestically and 5 days regionally, with next-day express available only in Singapore."}
{"prompt": "Summarise in one sentence: A damage claim must be filed within 7 calendar days of delivery. A claim for a parcel that never arrived must be filed within 21 calendar days of despatch. Claims above 500 dollars need manager review and photographs.", "category": "claims", "referenceResponse": "Damage claims must be filed within 7 days and non-delivery claims within 21 days, with claims over 500 dollars requiring manager review and photographic evidence."}
{"prompt": "Summarise in one sentence: Gold tier includes express delivery, a dedicated account manager, a 10 percent service credit for any late delivery, and priority claims handling. Gold requires more than 5000 shipments annually.", "category": "tiers", "referenceResponse": "Gold tier requires over 5000 annual shipments and provides express delivery, a dedicated account manager, a 10 percent late-delivery credit and priority claims handling."}
```

Add a few more of your own so you have around eight to ten records — enough to be meaningful, small enough to be cheap.

**Reference answers determine everything.** A metric compares output to your reference. If your references are inconsistent in length or style, your scores measure that inconsistency rather than model quality. Write them all in the same voice and to the same length.

Upload it:

```bash
aws s3 cp eval-prompts.jsonl s3://<your-bucket>/eval/
```

Also create an S3 location for results — the job writes its output there:

```bash
aws s3 mb s3://<your-bucket>-eval-results --region us-east-1
```

**Checkpoint:** A JSONL evaluation dataset of eight to ten records with consistent reference answers in S3, plus an output location, and you can name the three families of evaluation method.

---

## Step 2 — The automatic metrics

You must be able to name each metric, say what task it belongs to, and state its limitation. That triple is what gets tested.

### ROUGE — summarisation

**Recall-Oriented Understudy for Gisting Evaluation.** Measures how much of the **reference** appears in the generated output. It is **recall-oriented**: the question is "how much of what should have been said was said?"

Variants you should recognise:

- **ROUGE-N** — overlap of n-grams. ROUGE-1 is single words, ROUGE-2 is word pairs. ROUGE-2 is stricter because it requires correct ordering.
- **ROUGE-L** — longest common subsequence. Rewards matching sequence without requiring contiguity, so it tolerates inserted words.

**Use for:** summarisation. Recall orientation fits — a summary that omits the key point has failed, and ROUGE penalises that.

**Limitation:** it measures **word overlap, not meaning**. A summary that is perfectly accurate but uses synonyms throughout scores badly. A summary that copies large chunks of the source verbatim scores well while being a poor summary.

### BLEU — translation

**Bilingual Evaluation Understudy.** Measures how much of the **generated output** appears in the reference — **precision-oriented**, the mirror of ROUGE. Includes a brevity penalty so a model cannot score well by emitting one confidently-correct word.

**Use for:** machine translation. Precision orientation fits — in translation, adding content that was not in the source is an error, and BLEU penalises that.

**Limitation:** same as ROUGE. It is n-gram overlap, so a valid alternative translation using different vocabulary is penalised.

> **The ROUGE and BLEU pairing is heavily examined.** ROUGE for summarisation, recall-oriented, "did we capture the reference". BLEU for translation, precision-oriented, "is what we produced in the reference". If you remember only one thing about metrics, remember this.

### BERTScore — semantic similarity

Uses **embeddings** rather than exact word matching. It embeds the tokens of both texts and compares them in vector space, so semantically equivalent wording scores highly even with no shared words.

**Use for:** any generation task where paraphrase is acceptable — which is most of them.

**Advantage over ROUGE and BLEU:** it captures meaning. "The parcel arrives in two days" and "delivery takes 48 hours" score near zero on n-gram overlap and high on BERTScore.

**Limitation:** it depends on the embedding model, so scores are comparable within a configuration and not across different ones. It is also slower and costlier than counting n-grams, and it can score a fluent, semantically similar but factually **wrong** statement highly. Similarity is not correctness.

### Perplexity — fluency

Measures how "surprised" a model is by a piece of text. **Lower is better.** It is a property of the model's confidence, not a comparison against a reference.

**Use for:** assessing language modelling quality, comparing base models, monitoring training. It is not a task quality metric — a model can produce fluent, low-perplexity text that is completely wrong.

### F1, precision, recall — classification

When the task **does** have one right answer — classification, extraction, question answering with short exact answers — use the classification metrics. They are stronger than any overlap metric because they measure correctness rather than similarity.

**Practical implication:** if you can reframe a generative task as classification or extraction, do it. Evaluation becomes dramatically easier and more meaningful. This is a genuinely useful design insight, not just an exam point.

### Summary table

| Metric | Task | Orientation | Measures | Main limitation |
|---|---|---|---|---|
| **ROUGE** | Summarisation | Recall | N-gram / LCS overlap with reference | Word overlap, not meaning |
| **BLEU** | Translation | Precision | N-gram overlap, with brevity penalty | Penalises valid paraphrase |
| **BERTScore** | General generation | Semantic | Embedding similarity | Similarity is not correctness |
| **Perplexity** | Language modelling | — | Model's surprise at the text | Fluency, not accuracy |
| **F1 / precision / recall** | Classification, extraction | Both | Correctness against a label | Needs one right answer |

### The limitation that applies to all of them

**None of these metrics detects a hallucination.** A summary that invents a plausible fact, phrased in wording similar to the reference, can score well on ROUGE and BERTScore alike. Automatic metrics measure **similarity to a reference**, and similarity is not truth.

This is the reason human evaluation and grounding checks exist, and it is why a mature evaluation strategy never relies on automatic metrics alone. It is also a frequently-tested point.

**Checkpoint:** You can state for each metric its task, its orientation and its limitation, and you can explain why no automatic metric detects hallucination.

---

## Step 3 — Run an automatic evaluation job

Amazon Bedrock provides **model evaluation** as a managed capability, so you do not build a harness yourself.

> **Cost.** The job runs inference on every prompt in your dataset against every model selected. With eight to ten records this is small. Do not point it at a large dataset in this lab, and do not select several large models at once — cost scales with records multiplied by models.

### Create the job

1. Open the Bedrock console at <https://console.aws.amazon.com/bedrock/> and check your Region. **Model evaluation is not offered in every Region.**
2. In the left navigation, find the **evaluations** area and create a model evaluation.
3. **Evaluation type.** Choose **automatic**. The alternative is human-based evaluation, covered in Step 5.
4. **Name and description.** Name it so you recognise it later.
5. **Model selection.** Choose a model you have access to. If the console lets you select more than one for comparison, and your budget allows, select two — comparing two models on one dataset is far more informative than scoring one in isolation. Note that inference cost roughly doubles.
6. **Task type.** Choose the task matching your data. Options typically include general text generation, summarisation, question and answer, and classification. **Choose summarisation** — the task type determines which metrics are offered.
7. **Metrics.** Select what to compute. Depending on task type and Region you will typically be offered metrics grouped around **accuracy**, **robustness** and **toxicity**. For summarisation, accuracy is where you will find the ROUGE-family scoring. Read what the console describes for each — it names the underlying metric.
8. **Dataset.** Choose to use your **own prompt dataset** rather than a built-in one, and point at the S3 location of `eval-prompts.jsonl`.

   Built-in datasets are also offered. They are useful for a quick generic read on a model, but **your own dataset is what tells you about your own task** — a built-in dataset says nothing about whether a model summarises *Northwind's policies* well.

9. **Output location.** Point at your results bucket.
10. **IAM role.** Let the console create one unless your organisation requires otherwise. It needs to read your dataset, invoke the models, and write results.
11. **Create the job.**

The job takes some minutes. Monitor from the console, or:

```bash
aws bedrock list-evaluation-jobs --region us-east-1
```

```bash
aws bedrock get-evaluation-job --job-identifier <JOB_NAME_OR_ARN> --region us-east-1
```

If you need to abandon it:

```bash
aws bedrock stop-evaluation-job --job-identifier <JOB_NAME_OR_ARN> --region us-east-1
```

### While it runs — predict the results

Do this before you look. Predicting first is what turns a results page into learning.

Write down your answers:

1. **Which of your test records do you expect to score worst, and why?** Look for one where your reference answer uses different vocabulary from the source text — that is where n-gram overlap will punish a good summary.
2. **If a model produces a summary that is accurate but half the length of your reference, what happens to a recall-oriented score?** Why?
3. **If a model copies a whole sentence verbatim from the source, what happens?** Is that a good summary?

These three questions are the whole lesson of Step 4.

### What the job actually did

For each record: sent the prompt to each selected model, collected the response, compared it to your `referenceResponse` using the selected metrics, and wrote per-record scores plus aggregates to your S3 output location.

The important consequence: **the results are only as good as your reference answers.** The job did not judge quality — it measured similarity to text you wrote. If your references are weak, the scores are meaningless regardless of how precise they look.

**Checkpoint:** An automatic evaluation job completed, and you wrote down predictions before looking at the results.

---

## Step 4 — Interpret the results

Reading an evaluation report correctly is a skill, and misreading one is how teams ship worse systems while believing they improved them.

### Open the results

View the report in the console, and also open the raw output written to your S3 results bucket. The raw output carries **per-record** detail that the summary view aggregates away, and the per-record detail is where the understanding is.

### Read it in this order

**1. Look at the aggregate score last, not first.**

A single number across your whole dataset hides everything useful. Two models with the same average can fail on completely different records.

**2. Find your worst-scoring records and read the actual output.**

This is the essential step. For your two or three lowest-scoring records, put the generated text next to your reference and ask:

- **Is the output actually bad?** Or is it a perfectly good summary that used different words?
- **Is my reference bad?** Was it longer, shorter or stylistically different from the others?
- **Is the metric wrong for this record?**

You should find at least one record where **the low score is the metric's fault, not the model's.** That single observation is the most valuable outcome of this lab. It is why a score is evidence rather than a verdict.

**3. Find your best-scoring records and be suspicious.**

Check whether any high score came from the model **copying source text verbatim**. High overlap with a reference that itself closely tracks the source will score well while being a poor summary. High scores need scrutiny as much as low ones.

**4. Only now compare models.**

If you evaluated two models, compare per-record before comparing averages. Ask:

- Does one win consistently, or does it win on some records and lose on others?
- If they are close, what is the **cost per token** difference? A model scoring marginally lower for meaningfully less money is usually the correct production choice.
- What about **latency**? Not in the report, but it is a real requirement.

**The exam-relevant framing: model selection is a trade-off across quality, cost and latency, not a search for the highest score.** A question describing a high-volume, latency-sensitive workload with "good enough" quality requirements is pointing at the smaller, cheaper model.

### Record your findings

| Record | Score | Output actually good? | Score justified? | Why |
|---|---|---|---|---|
| Lowest | | | | |
| 2nd lowest | | | | |
| Highest | | | | |

### What automatic scores can and cannot support

**They can:**
- Detect a **regression** when something changes — the strongest everyday use.
- **Rank candidates** for a shortlist to be examined by hand.
- Provide a **repeatable** number that does not drift with the reviewer's mood.
- Run continuously in a pipeline at a cost no human process can match.

**They cannot:**
- Tell you an answer is **factually correct**.
- Detect a **hallucination** — a fabricated fact phrased similarly to the reference scores well.
- Judge **usefulness, tone or appropriateness** for your audience.
- Measure anything your reference answers did not encode.

### Use scores as a relative instrument

Do not ask "is 0.42 a good score?" — the number has no absolute meaning. Ask **"did the score change?"**

The reliable pattern: fix the dataset, fix the metric, fix the reference answers, then change **one** thing — prompt, model, top-K, chunk size — and re-run. The **delta** is trustworthy in a way the absolute value never is.

This closes the loop on the whole domain. Lab 12's prompt variants, Lab 16's top-K and chunking, and Lab 17's fine-tuning decision are all changes whose value should be established this way rather than by impression.

**Checkpoint:** You inspected per-record output, found at least one record where the score misrepresented the output quality, and can explain why a delta is more trustworthy than an absolute score.

---

## Step 5 — Human evaluation, benchmarks, and business metrics

Step 4 showed the ceiling on automatic metrics. This step covers what sits above it.

### Human evaluation in Bedrock

Bedrock supports **human-based model evaluation**, where people rate model outputs against criteria you define.

Walk through the configuration — **you may create this if your budget allows, but a small automatic job plus this walkthrough is sufficient for the lab.** Human evaluation costs more than automatic, because you are paying for human time.

1. In the evaluations area, begin creating an evaluation and choose the **human** type.
2. **Work team.** You choose who does the rating. You can bring your **own team of workers** — colleagues, subject matter experts — or use an AWS-managed work team. Domain experts almost always give more useful ratings than generic raters, and for specialised material they are essential.
3. **Rating method.** You define how outputs are judged. Typical methods include **comparison between two models**, **rating on a scale**, **thumbs up or down**, and **ranking**.

   **Comparison is usually the most reliable.** People are much better at judging "which of these two is better" than at assigning an absolute score, and comparative judgements are more consistent between raters.

4. **Evaluation criteria and instructions.** Define what raters assess — helpfulness, correctness, coherence, tone, adherence to a policy. **Write the instructions carefully.** Vague criteria produce inconsistent ratings, and inconsistent ratings are worse than no ratings because they carry false authority.
5. **Dataset.** Your own prompt dataset, as before.
6. Workers rate through a provided interface; results aggregate into a report.

### Getting human evaluation right

- **Define the criteria precisely, with examples.** "Rate helpfulness 1 to 5" means five different things to five raters. Anchor each point on the scale with a concrete example.
- **Use multiple raters per item and measure agreement.** If two raters disagree constantly, your criteria are ambiguous — fix the criteria, not the raters.
- **Blind the raters to which model produced which output**, or you measure expectation rather than quality.
- **Watch for fatigue.** Rating quality falls over long sessions. Keep batches short.
- **Sample, do not enumerate.** Humans cannot rate ten thousand outputs. Use automatic metrics broadly and human evaluation on a representative sample.

### LLM as a judge

A middle path between the two: use a strong foundation model to score outputs against criteria you specify in a prompt.

- **Cheaper and faster than humans**, and it can assess qualities no n-gram metric reaches — relevance, tone, whether an answer is grounded in provided context.
- **But it is a model evaluating a model.** It inherits biases, can favour longer or more confident-sounding answers, and its judgements should themselves be validated against human ratings on a sample before you trust them.

This is the same mechanism behind **contextual grounding checks** in Amazon Bedrock Guardrails, encountered in Lab 14 — a model assessing whether a response is supported by its source material.

### Benchmark suites

Standard public datasets with published results, used to compare models on general capability. You should recognise the category and the following names:

- **GLUE** and **SuperGLUE** — general language understanding tasks.
- **MMLU** (Massive Multitask Language Understanding) — knowledge and reasoning across many academic subjects.
- **BIG-bench** — a large, diverse collection of hard tasks.
- **HELM** (Holistic Evaluation of Language Models) — a framework that evaluates across multiple dimensions including accuracy, robustness, fairness, bias, toxicity and efficiency, rather than reducing a model to one number.

**Use benchmarks for:** initial shortlisting, and comparing models on general capability where you have no task-specific data yet.

**Do not use benchmarks for:** deciding whether a model is good at *your* task. Two limitations matter:

- **They are generic.** Strong MMLU performance says nothing about summarising Northwind's claims policy.
- **Contamination.** Benchmark data may have appeared in training data, inflating scores without reflecting real capability.

**HELM is worth singling out** because its multi-dimensional design matches how you should actually think: a model is not one number, and fairness, bias, toxicity, robustness and efficiency are dimensions in their own right — connecting directly to Domain 4.

### Business metrics — the ones that decide

Everything so far measures the model. Ultimately the organisation cares whether the system worked. Be ready to name these:

- **User satisfaction** — surveys, thumbs up or down in the product, complaint volume
- **Task completion rate** — did users achieve what they came to do
- **Escalation or deflection rate** — for a support assistant, the proportion of conversations resolved without a human
- **Average revenue per user, conversion, retention** — where the system touches revenue
- **Cross-domain efficiency** — cost per interaction, handling time, throughput per employee
- **Time to resolution** and error rates in downstream processes

**These are the metrics that justify the project.** A ROUGE improvement that does not move any of them has not delivered value. A frequent exam framing asks how to measure the *business* success of a generative AI application — the answer is these, not ROUGE.

### The complete evaluation strategy

| Stage | Method | Frequency |
|---|---|---|
| Shortlist candidate models | Benchmarks, published results | Once per selection |
| Iterate on prompts, RAG, models | Automatic metrics on your own dataset | Every change |
| Validate a significant change | Human evaluation on a sample | Per major release |
| Continuous quality monitoring | LLM as a judge, plus sampled human review | Ongoing |
| Prove business value | Business metrics | Ongoing |

**Checkpoint:** You can describe how to configure human evaluation and why comparison beats absolute rating, name four benchmark suites including what makes HELM distinctive, and list five business metrics.

---

## Step 6 — Clean up

This is the last lab of Domain 3, so clean up this lab **and** verify that nothing from Labs 15, 16 and 17 survived.

### 1. Stop any running evaluation job

An evaluation job bills for the inference it performs. If one is still running and you no longer need it:

```bash
aws bedrock list-evaluation-jobs --region us-east-1
```

```bash
aws bedrock stop-evaluation-job --job-identifier <JOB_NAME_OR_ARN> --region us-east-1
```

A **completed** job is a stored record, not a running resource — it is not accruing charges. You may keep completed jobs for reference; delete them from the console if you prefer a tidy account.

### 2. Remove the S3 data

Evaluation results can be sizeable if the dataset was large. Yours is small, but tidy up:

```bash
aws s3 rm s3://<your-bucket>/eval/ --recursive
aws s3 rm s3://<your-bucket>-eval-results --recursive
aws s3 rb s3://<your-bucket>-eval-results
```

**Keep a local copy of `eval-prompts.jsonl` and your reference answers.** A curated evaluation dataset is genuinely valuable — it is the asset that makes every future change measurable, and rebuilding one is tedious.

### 3. Delete the IAM role

If the console created a service role for the evaluation job, remove it from <https://console.aws.amazon.com/iam/>. It does not bill, but it holds S3 and Bedrock invoke permissions with no remaining purpose.

### 4. Domain 3 final sweep — do this properly

Run every command below, **in every Region you worked in during Labs 15 to 18**. Region-scoped resources in a Region you switched away from are invisible in the console and still billing.

```bash
aws bedrock-agent list-knowledge-bases --region us-east-1
aws opensearchserverless list-collections --region us-east-1
aws bedrock list-custom-models --region us-east-1
aws bedrock list-model-customization-jobs --region us-east-1
aws bedrock list-provisioned-model-throughputs --region us-east-1
aws bedrock list-evaluation-jobs --region us-east-1
```

The two that bill continuously and therefore matter most:

- **`list-collections`** — an OpenSearch Serverless collection from Lab 15 or 16 bills by the hour, whether or not you query it, and **survives deletion of the knowledge base**.
- **`list-provisioned-model-throughputs`** — provisioned throughput from Lab 17 bills for its duration and may carry a term commitment.

If either returns anything of yours, delete it now. Return to Lab 16 Step 6 or Lab 17 Step 6 for the exact commands.

### 5. Check the bill tomorrow

Open the Billing and Cost Management console **the following day** and review yesterday's spend by service. Domain 3 was the expensive part of this course; this is your confirmation that it is properly finished.

Look specifically for **Amazon OpenSearch Service** and **Amazon Bedrock** line items. An unexpected OpenSearch charge means a collection survived somewhere — check every Region.

### Final checklist

- [ ] No running evaluation jobs
- [ ] Evaluation dataset and results removed from S3, local copy of the dataset kept
- [ ] IAM service role deleted
- [ ] **No knowledge bases, in any Region**
- [ ] **No OpenSearch Serverless collections, in any Region**
- [ ] **No provisioned model throughputs, in any Region**
- [ ] No custom models or customisation jobs
- [ ] Billing check scheduled for tomorrow

**Checkpoint:** All six list commands return nothing of yours in every Region you used, your evaluation dataset is saved locally, and Domain 3 has left no billing resource behind.

---

## Verification

- [ ] You can name the three families of evaluation method and the main weakness of each.
- [ ] You built a JSONL dataset of eight to ten records with consistent reference answers.
- [ ] You can state for each of ROUGE, BLEU, BERTScore, perplexity and F1 its task, orientation and limitation.
- [ ] You can explain that ROUGE is recall-oriented for summarisation and BLEU is precision-oriented for translation.
- [ ] You can explain why no automatic metric detects a hallucination.
- [ ] An automatic evaluation job completed against your own dataset.
- [ ] You wrote predictions before opening the results.
- [ ] You inspected per-record output and found at least one record where the score misrepresented the quality of the output.
- [ ] You checked whether any high score came from verbatim copying of source text.
- [ ] You can explain why a score delta is trustworthy where an absolute score is not.
- [ ] You can describe how to configure human evaluation and why comparison beats absolute rating.
- [ ] You can name GLUE, SuperGLUE, MMLU, BIG-bench and HELM, and say what makes HELM distinctive.
- [ ] You can list at least five business metrics for a generative AI application.
- [ ] **All six Domain 3 sweep commands return nothing of yours, in every Region you used.**

## Discussion questions

1. **When the metric is wrong (Task 3.4).** You found a record where a good summary scored badly because it paraphrased the reference. Give three distinct responses to that: one that changes the metric, one that changes the dataset, and one that changes how the score is used. Which would you actually implement, and what does each cost you?

2. **Designing an evaluation strategy.** You are launching a customer-facing support assistant built on RAG. Specify the full strategy: what you evaluate before launch, what runs automatically on every change, what humans review and how often, and which business metrics prove it worked. Justify why each method sits where it does rather than somewhere cheaper or more expensive.

3. **Choosing a model on more than quality (Tasks 3.1 and 3.4).** Two models are evaluated on your dataset. The larger scores modestly higher but costs several times more per token and is noticeably slower. The workload is high volume and latency sensitive. Make the case for the smaller model in terms your finance and product stakeholders would each accept — and state the specific evidence that would change your recommendation.

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.
