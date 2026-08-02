# Step 1 — Why evaluate, and build a test set

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
