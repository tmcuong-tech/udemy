# Step 3 — Configure a Clarify explainability analysis

Clarify computes explainability in the same processing-job framework as bias analysis. As in
Lab 20, there are two paths.

> ### COST WARNING — Path 1 starts billable compute
> An explainability job **requires model predictions**, so Clarify deploys your model to a
> temporary (shadow) endpoint and calls it many times — once per SHAP sample per row. This
> is more inference traffic than a bias job. The processing instances and the endpoint both
> bill for their duration, and a failed job can strand the endpoint, which then **bills
> continuously until deleted**. Do not start Path 1 unless you will complete Step 6.

### 3.1 Path 1 — run it against your own model

1. Go to the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/).
2. Open SageMaker Studio, or the Clarify/processing entry point in your console version.
3. Create a Clarify processing job with an **explainability** configuration:

**Data configuration**
- Input dataset S3 URI, format and header row
- Output S3 prefix for the analysis and report
- The label column, and which feature columns to analyse

**Model configuration**
- The model to explain, plus instance type and count for the shadow endpoint
- How to read the model's output — which field carries the score or probability

**SHAP configuration**
- **Baseline** — one row or a set of rows representing your chosen reference. Decide this
  deliberately using Step 2.2, and write down *why* you chose it.
- **Number of samples** — more samples, more stable attributions, more cost
- Whether to emit **global** aggregated attributions, **local** per-row attributions, or both

**Job resources**
- Processing instance type and count

4. Run the job and wait for completion.
5. Collect the outputs from your S3 prefix — the analysis JSON containing attribution values
   and the generated report.

Then go **straight to Step 6** and verify nothing is left running.

### 3.2 Path 2 — no resources required

Skip the job. Steps 4 and 5 are written to be completed entirely from the illustrative
report in Step 4, and they carry the learning outcome on their own.

### 3.3 Two things worth noticing about the configuration

**Bias and explainability share a job type.** That is not an accident of packaging. The
workflow is: measure the disparity (Lab 20), then explain what produces it (this lab). A
fairness finding without an attribution analysis tells you a problem exists but gives you
nothing to act on. An attribution analysis without a fairness finding tells you what the
model uses but not whether that matters to anyone.

**Explainability can also be run online.** Clarify supports attaching explainability to a
real-time endpoint so individual predictions carry their attributions with them. That is the
architecture you need when a caseworker must explain a decision at the moment it is made,
rather than in a batch report a month later — and it is what makes a contestability process
operationally possible.

Note the cost consequence: online explainability means the attribution computation runs on
every explained request, adding latency and inference cost per call. Whether every prediction
needs an explanation, or only contested ones, is a design decision with a real bill attached.
