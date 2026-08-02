# Step 3 — Run an automatic evaluation job

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
