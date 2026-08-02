# Step 4 — Path 1: run a Clarify bias job against your own model

> ### COST WARNING — this step starts billable compute
> A Clarify processing job runs on instances you choose and bills for the duration.
> Post-training analysis additionally causes Clarify to **deploy your model to a temporary
> (shadow) endpoint**. If the job fails midway, that endpoint can be left behind and will
> **bill continuously until you delete it**. Do not start this step unless you intend to
> follow Step 6 immediately afterwards.

**Only do this step if you already have a trained SageMaker model and a tabular dataset in
S3.** Otherwise skip to Step 5, which is the expected route and fully sufficient.

### 4.1 Prepare the inputs

You need:

- A **dataset** in S3 as CSV or Parquet, with a header row, containing your facet column
  and your label column.
- An **output S3 prefix** where the bias report and analysis JSON will be written.
- A **model** already registered in SageMaker, if you want post-training metrics.

### 4.2 Configure the job

1. Go to the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/).
2. In the left navigation, open SageMaker Studio, or the Clarify/processing entry point
   available in your console version.
3. Create a **Clarify processing job** and supply:

**Data configuration**
- Input dataset S3 URI and content type
- Output S3 prefix
- `label` — the target column name
- Header row and dataset format

**Bias configuration**
- `label_values_or_threshold` — which value(s) count as the positive outcome
- `facet` — the sensitive column, plus the facet value(s) under analysis
- **Analysis type** — pre-training only, post-training only, or both

**Model configuration** (required for post-training bias)
- The model name, the instance type and count for the shadow endpoint, and the
  accept/content types the model expects
- For post-training metrics Clarify also needs to know how to read the model's output —
  which field holds the probability or the predicted label, and any threshold to apply

**Job resources**
- Instance type and instance count for the processing job itself

4. Run the job and wait for completion.

### 4.3 Retrieve and read the outputs

From your S3 output prefix you will get:

- **`analysis.json`** — the computed metric values, machine-readable
- A **generated report** summarising the analysis in readable form
- Supporting artefacts depending on which analyses you enabled

Read the pre-training section first, then the post-training section, and compare them —
that comparison is where amplification (Step 3.3) shows up.

### 4.4 Immediately verify nothing is left running

Before you do anything else:

- [ ] The processing job shows **Completed**, **Stopped** or **Failed** — not **InProgress**.
- [ ] **Endpoints** — check the endpoints list even if you did not deliberately create one.
      Clarify's shadow endpoint is normally cleaned up automatically, but a failed job can
      strand it.

Then complete Step 6 in full.

### 4.5 If you cannot run Path 1

That is the expected case, and it is not a gap in your learning. The exam tests whether you
can **read and reason about** a bias report, choose the right metric family for a described
symptom, and report a finding responsibly. Step 5 exercises all three.
