# Step 6 — Deploy, monitor and close the loop

Stages 9 and 10, plus the automation that ties the pipeline together.

### 6.1 Deployment choice for Northwind

The business offers 5,000 discounts a month, decided in advance. Nobody is waiting for an
answer, and all the inputs already exist.

**Therefore: batch transform, run monthly.** Not a real-time endpoint.

Choosing a real-time endpoint here would mean paying for always-on instances to answer
twelve requests a year. Recognising this is worth more marks than any amount of algorithm
knowledge — it is the most common cost-optimisation question in Domain 1.

The design changes only if the requirement changes: if the retention offer must appear
while a customer is on the phone to the call centre, then it is a real-time endpoint, and
Feature Store's **online store** becomes necessary.

### 6.2 Why monitoring is a stage, not an afterthought

Models decay. Three named causes:

| Type | What changes | Northwind example |
|---|---|---|
| **Data drift** (covariate shift) | The distribution of the *inputs* changes | A tariff change shifts every bill upward |
| **Concept drift** | The *relationship* between inputs and target changes | A competitor enters the market and churn behaviour changes entirely |
| **Data quality issues** | The pipeline breaks | An upstream schema change silently sends nulls |

None of these is visible from the model itself. The endpoint keeps returning confident
predictions that are increasingly wrong.

### 6.3 SageMaker Model Monitor

1. In the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/) left
   navigation, find **Model Monitor** or the monitoring section under inference.
2. Read the available monitor types. SageMaker Model Monitor can watch for:

| Monitor | Detects |
|---|---|
| **Data quality** | Input statistics or schema deviating from a captured baseline |
| **Model quality** | Predictions diverging from actual outcomes, once ground truth arrives |
| **Bias drift** | Bias metrics moving beyond a threshold over time |
| **Feature attribution drift** | The relative importance of features shifting |

The mechanism to remember: **capture a baseline from the training data, enable data capture
on the endpoint, schedule monitoring jobs to compare live traffic against the baseline, and
alert through Amazon CloudWatch when a constraint is violated.**

Note that **model quality** monitoring requires ground truth. For Northwind, whether an
account actually churned is only known 90 days later — so model quality can only be
measured with a lag, while data quality can be measured immediately. That lag is a real
design constraint.

### 6.4 Closing the loop

When monitoring fires, the response is to retrain — which means going back to stage 2 with
fresh data. Doing that reliably by hand is not realistic, so AWS provides:

1. **SageMaker Pipelines** — a CI/CD workflow service for ML. Look for **Pipelines** in the
   left navigation. A pipeline chains processing, training, evaluation, conditional
   approval and registration steps into one repeatable, version-controlled definition.
2. **SageMaker Model Registry** — open **Model registry** (under models or governance). It
   holds **model groups** containing **versioned model packages**, each with an approval
   status. A pipeline registers a new version as `PendingManualApproval`; a human approves
   it; approval triggers deployment.

Together these give you **MLOps**: the same discipline software engineering applies to code,
applied to models — versioning, automated testing, approval gates and reproducible
deployment.

### 6.5 Review your pipeline

Return to the ten-line pipeline you wrote in Step 1.3 and fill in, for every stage:

- what you would do for Northwind
- which AWS service supports it
- what would go wrong if you skipped it

Check specifically that you have:

- Split by **account and by time**, not randomly (Step 3.2)
- Removed the leaky `cancellation_reason_code` (Step 2.4)
- Chosen **precision-at-5000 or AUC**, not accuracy (Step 5.4)
- Chosen **batch transform**, not a real-time endpoint (Step 6.1)
- Planned **data quality monitoring now** and **model quality monitoring at a 90-day lag**
  (Step 6.3)

Those five decisions are the substance of this lab.
