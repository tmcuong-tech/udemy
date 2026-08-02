# Step 5 — Human evaluation, benchmarks, and business metrics

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
