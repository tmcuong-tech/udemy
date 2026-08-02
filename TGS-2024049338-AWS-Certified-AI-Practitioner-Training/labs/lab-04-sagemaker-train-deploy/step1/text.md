# Step 1 — Read the cost warning and plan the run

> ## ⚠️ COST WARNING — READ BEFORE YOU START
>
> **This is the first lab in the course that creates resources which bill continuously.**
>
> | Resource | Bills | Stops billing when |
> |---|---|---|
> | SageMaker **notebook instance** | Per hour, whenever the status is `InService` | You **stop** or **delete** it |
> | SageMaker **Studio application** (JupyterLab, Code Editor, Canvas) | Per hour, whenever it is running | You **delete the app** — closing the browser tab does nothing |
> | SageMaker **real-time endpoint** | Per hour, continuously, **even with zero requests** | You **delete the endpoint** |
> | SageMaker **training job** | Only for the seconds the job runs | Automatically, when the job finishes |
> | Amazon **S3** objects | Per GB-month stored | You delete the objects |
>
> An endpoint left running is the single most common source of unexpected AWS bills for
> people learning SageMaker. **Do not skip Step 7.** If you have to abandon the lab
> part-way through, jump straight to Step 7 and delete everything.
>
> Confirm current instance pricing on the AWS SageMaker pricing page for your Region before
> you start, and check whether your account still has AWS Free Tier coverage.

### 1.1 What you will build

You will run the full lifecycle you defined in Lab 01, end to end:

```
data in S3  →  training job  →  model artefact  →  endpoint  →  prediction
```

The task is **binary classification** on a small tabular dataset, using the SageMaker
**built-in XGBoost algorithm**. XGBoost is the standard first choice for tabular data and
appears constantly in AIF-C01 scenarios.

### 1.2 Prerequisites

- An AWS account with permission to create SageMaker, IAM and S3 resources.
- Region **US East (N. Virginia) `us-east-1`** selected in the console.
- About 45 minutes of uninterrupted time — the notebook instance bills the whole time it
  is running, so do not start and walk away.

### 1.3 Set a billing guard (recommended)

1. Open the **Billing and Cost Management** console.
2. Under **Budgets**, create a small monthly cost budget — for example 5 USD — with an
   email alert at 80%.

This will not stop anything running, but it is the cheapest insurance available and takes
two minutes. Cost awareness is itself an exam topic.

### 1.4 Note the instance types you will use

| Purpose | Instance type used in this lab |
|---|---|
| Notebook instance | `ml.t3.medium` — the smallest generally suitable notebook size |
| Training job | `ml.m5.large` |
| Inference endpoint | `ml.m5.large` |

If a chosen type is unavailable or your account quota does not permit it, the console will
say so; choose the next smallest type it offers rather than a larger one.
