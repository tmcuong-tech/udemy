# Lab 05 — The ML Pipeline and Data Preparation

Design a complete ML pipeline for a churn scenario, from business framing through data preparation and feature engineering to deployment and monitoring, grounded in the SageMaker console.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 1 — Fundamentals of AI and ML (20%)
**Task statement:** 1.3 Describe the ML development lifecycle
**WSQ mapping:** LU4 · Topic 7 Developing ML Solutions · K3 · A4 · LO4
**Slide reference:** v11 deck slides 84–135
**Estimated time:** 40 minutes

> **⚠️ Cost note:** the core of this lab is console navigation and design work, which
> creates nothing chargeable. The **optional** Data Wrangler walkthrough in Step 3.4 starts
> a SageMaker Canvas or Studio application that **bills per hour until you shut it down**.
> If you do that section, Step 7.4 is mandatory.

**Learning objectives:**
- Translate a business goal into an ML question, with distinct model metrics and business metrics
- Describe the stages of the ML lifecycle and name the AWS service that supports each
- Perform the checks that make up exploratory data analysis, and detect target leakage
- Apply pre-processing treatments for missing values, outliers, categorical variables, scaling and class imbalance without leaking data
- Engineer features for a tabular problem and explain how SageMaker Feature Store prevents training/serving skew
- Distinguish underfitting from overfitting and describe how automatic model tuning searches hyperparameters
- Select an evaluation metric appropriate to an imbalanced problem and a business constraint
- Choose a deployment option and design drift monitoring with SageMaker Model Monitor, Pipelines and the Model Registry

---

## Step 1 — Frame the business problem and map the pipeline

Lab 04 walked one narrow path through the ML lifecycle. This lab widens it to the full
pipeline the exam expects you to describe, and to the AWS service that supports each stage.

### 1.1 The scenario

You will design — not build — a pipeline for this brief:

> **Northwind Utilities** wants to reduce customer churn. It has 400,000 residential
> accounts, 3 years of monthly billing records, a support-ticket system, and a marketing
> team that can offer a retention discount to 5,000 customers a month. They want to know
> which 5,000.

Before anything technical, answer these:

1. **What is the ML question?** Not "reduce churn" — that is a business goal. The ML
   question is: *what is the probability that this account cancels in the next 90 days?*
2. **What kind of ML problem is it?** Supervised binary classification on tabular data.
3. **What does success look like?** Both a **model metric** (for example AUC, or recall at
   the top 5,000 ranked accounts) and a **business metric** (churn rate, revenue retained).
   These are not the same thing, and the exam tests that they are not.
4. **Is ML even the right tool?** If a simple rule — "anyone whose bill rose more than 40%"
   — captures most of the value, use the rule. ML is justified when the pattern is complex,
   the data volume is large, and the pattern changes over time.

> **Exam framing:** "business problem framing" is the first stage of the lifecycle and the
> one most often skipped. A model with excellent AUC that answers the wrong question is a
> failed project.

### 1.2 The full pipeline

| # | Stage | What happens | Primary AWS support |
|---|---|---|---|
| 1 | **Business problem framing** | Define the question, the metrics, and whether ML is warranted | — |
| 2 | **Data collection** | Gather and centralise raw data | Amazon S3, AWS Glue, Amazon Kinesis |
| 3 | **Exploratory data analysis (EDA)** | Understand distributions, missing values, correlations, leakage | SageMaker Data Wrangler, Amazon Athena, QuickSight |
| 4 | **Data pre-processing** | Clean, impute, deduplicate, encode, scale, split | SageMaker Data Wrangler, SageMaker Processing |
| 5 | **Feature engineering** | Create the variables the model actually learns from | SageMaker Data Wrangler, SageMaker Feature Store |
| 6 | **Model training** | Fit the algorithm to the training data | SageMaker training jobs, built-in algorithms, JumpStart |
| 7 | **Hyperparameter tuning** | Search for the best training settings | SageMaker automatic model tuning (AMT) |
| 8 | **Model evaluation** | Measure performance on held-out data; check bias | SageMaker evaluation, SageMaker Clarify |
| 9 | **Deployment** | Serve predictions | SageMaker endpoints, batch transform |
| 10 | **Monitoring** | Detect drift and degradation in production | SageMaker Model Monitor, Amazon CloudWatch |

Two points to fix in memory:

- **The pipeline is a loop, not a line.** Monitoring feeds back into data collection and
  retraining. A model is not "finished" at deployment.
- **Stages 2–5 typically consume the majority of a project's effort.** The exam reflects
  this: data preparation questions outnumber training questions.

### 1.3 Record your version

Write out the ten stages for the Northwind scenario, one line each, saying what you would
actually do at that stage for *this* problem. You will fill in the detail as you work
through Steps 2–6.

---

## Step 2 — Collect data and explore it

Stages 2 and 3 of the pipeline: get the data into one place, then look at it before you
touch it.

### 2.1 Data collection for the scenario

Northwind's data lives in three places. Map each to a data type and a collection approach:

| Source | Data type | How it reaches S3 |
|---|---|---|
| Billing records (relational database) | Structured, tabular and time-series | Scheduled extract, or AWS Glue / AWS DMS into S3 |
| Support tickets (free text) | Unstructured text | Export to S3; enrich with Amazon Comprehend |
| Meter readings (streaming) | Time-series | Amazon Kinesis Data Firehose into S3 |

Two design facts worth stating:

- **Amazon S3 is the centre of gravity.** Whatever the source, ML data lands in S3 because
  every SageMaker component reads from it.
- **A data lake plus a catalogue beats scattered extracts.** AWS Glue crawlers populate the
  Glue Data Catalog so Amazon Athena can query the raw files with SQL — often the cheapest
  possible EDA.

### 2.2 Look at the exploration tooling in the console

1. Open the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/) in
   `us-east-1`.
2. In the left navigation, look for **Data Wrangler** (it may appear under a data
   preparation grouping, or inside **SageMaker Canvas**, depending on your console version).
3. Read the description on the landing page. Do **not** launch it yet — Step 3 covers
   that, with a cost warning.

Data Wrangler is a visual data preparation tool. It imports from S3, Athena, Amazon
Redshift and other sources, profiles the data, offers built-in transforms, and exports
either a processed dataset or a repeatable processing job.

### 2.3 What EDA actually looks for

Whether you use Data Wrangler, Athena or pandas, EDA answers the same six questions.
Write down, for the Northwind data, what you would check for each:

| Question | What you are looking for | Why it matters |
|---|---|---|
| **What is the distribution of each feature?** | Skew, unexpected ranges, unit errors | Skewed features may need transformation |
| **How much is missing, and is it missing randomly?** | Null counts per column and per segment | Non-random missingness is itself a signal — and a bias risk |
| **Are there outliers?** | Extreme values | Could be errors to fix, or the rare events you care most about |
| **What is the class balance?** | Ratio of churned to retained | Churn is usually 2–5%; heavy imbalance changes metrics and sampling |
| **Which features correlate with the target — and with each other?** | Correlation matrix | Strong feature-to-feature correlation is redundancy; strong target correlation may be leakage |
| **Is there target leakage?** | Features unavailable at prediction time | The single most damaging silent error in ML |

### 2.4 The leakage trap

**Target leakage** is when a feature encodes information that would not exist at the moment
you actually need the prediction. For Northwind, a column called `cancellation_reason_code`
is perfect at predicting churn — and useless, because it is only populated *after* the
customer cancels.

Symptoms: implausibly high validation performance, and a model that collapses in
production. Test for it by asking of every feature: **"would I have this value, with this
value, at the moment I score a live customer?"**

Go through your Northwind feature list now and mark any column that fails that test.

---

## Step 3 — Pre-process the data

Stage 4: turn raw records into something an algorithm can consume without being misled.

### 3.1 The pre-processing checklist

| Problem | Typical treatment | Trap |
|---|---|---|
| **Missing values** | Impute with mean, median or a constant; or drop the row or column | Imputing with the mean of the *whole* dataset leaks test information into training |
| **Duplicates** | Deduplicate on a business key | Near-duplicates often survive an exact-match dedupe |
| **Outliers** | Cap (winsorise), transform, or remove | Removing outliers destroys the signal in fraud and fault detection |
| **Inconsistent categories** | Standardise (`SG`, `Singapore`, `sg` → one value) | Unseen categories at inference time will break naive encoders |
| **Categorical variables** | One-hot encoding for low cardinality; ordinal encoding where order is real | One-hot on a high-cardinality column explodes dimensionality |
| **Numeric scale differences** | Normalisation (0–1) or standardisation (mean 0, sd 1) | Fit the scaler on **training data only**, then apply it to validation and test |
| **Class imbalance** | Resampling, class weights, or a threshold chosen on a ranking metric | Oversampling before splitting puts copies of the same record on both sides of the split |
| **Text fields** | Tokenise, or extract features with Amazon Comprehend | — |

The single rule underneath half of these: **fit every transformation on the training split
only, then apply it to validation and test.** Anything else is data leakage.

### 3.2 Splitting, revisited

You split in Lab 04 with a random shuffle. For Northwind that would be **wrong**.

- The data is **time-series-flavoured** — you are predicting the future from the past. A
  random split lets the model train on March and be tested on February, which it will never
  do in production. Split by time: train on months 1–30, validate on 31–33, test on 34–36.
- The data has **grouped records** — many rows per account. If rows from the same account
  land in both train and test, the model can memorise the account rather than learn the
  pattern. Split by **account**, not by row.

Choosing the split strategy is a modelling decision, not a formality.

### 3.3 See where pre-processing runs on AWS

In the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/) left
navigation, find **Processing jobs**.

A **SageMaker Processing job** runs a container over your data on managed compute and then
shuts down — the same billing model as a training job. It is how you run pre-processing at
scale and, critically, how you run **the same transformation code at training time and at
inference time**. Divergence between the two is a classic production failure known as
**training/serving skew**.

The list is probably empty. Note what a job record would contain: an input S3 path, a
container, an instance type, and an output S3 path.

### 3.4 Optional hands-on — SageMaker Data Wrangler

> **⚠️ COST WARNING:** Data Wrangler runs inside a **SageMaker Canvas or Studio
> application**, which **bills per hour while it is running** and does not stop when you
> close the browser tab. If you do this section you **must** complete Step 7.4 to shut the
> application down. Skip this section if you are unsure — Steps 3.1–3.3 carry the
> examinable content.

If you choose to proceed:

1. In the SageMaker console, launch **SageMaker Canvas** (or Studio) and create a
   **Data Wrangler** data flow.
2. Import a CSV from S3 — the `customers.csv` from Lab 02 works, or any small tabular file.
3. Open the **Data quality and insights report**, which profiles the dataset: column types,
   missing values, distributions, and warnings about likely issues.
4. Add two or three transforms from the built-in list — for example handle missing values,
   encode a categorical column, and scale a numeric column. Each appears as a node in the
   flow.
5. Note the **Export** options: you can export the flow as a SageMaker Processing job,
   which is precisely the reproducibility point from 3.3 — the visual flow becomes runnable,
   version-controllable code.
6. **Immediately** go to Step 7.4 and shut the application down when you are finished.

---

## Step 4 — Engineer features and store them

Stage 5. Pre-processing makes data *usable*; feature engineering makes it *predictive*.

### 4.1 What feature engineering is

A **feature** is an input variable the model learns from. Feature engineering is creating
better ones from the raw columns — usually by encoding domain knowledge the algorithm has
no way to discover on its own.

For Northwind, the raw table has `monthly_bill` per account per month. None of these
columns exists yet, and every one is more predictive than the raw value:

| Engineered feature | How it is built | Why it helps |
|---|---|---|
| `bill_change_pct_3m` | Current bill ÷ mean of previous 3 months | A sudden bill jump is a churn trigger |
| `tenure_months` | Today − signup date | New customers churn at different rates |
| `tickets_last_90d` | Count of support tickets in a window | Dissatisfaction signal |
| `avg_ticket_sentiment` | Amazon Comprehend sentiment over ticket text, averaged | Turns unstructured text into a numeric feature |
| `days_since_last_payment` | Recency | Payment behaviour precedes cancellation |
| `is_winter_month` | Calendar flag | Separates seasonal bill rises from real ones |
| `usage_vs_similar_homes` | Ratio to a peer group | Normalises for household size |

Note the pattern: **aggregations over time windows, ratios, recency counts, and
domain-derived flags**. That set covers most tabular feature engineering.

### 4.2 Feature engineering as dimensionality change

Two directions, both examinable:

- **Feature creation** adds columns — the table above.
- **Feature selection and dimensionality reduction** remove them. Drop features that are
  redundant (highly correlated with another), useless (near-zero variance), or leaky.
  **Principal component analysis (PCA)** compresses many correlated numeric features into
  fewer components.

More features is not better. Too many relative to the number of rows increases overfitting
and training cost, and makes the model harder to explain — which matters for Domain 4.

### 4.3 The reproducibility problem, and SageMaker Feature Store

Here is the failure mode Feature Store exists to solve:

- The data science team computes `bill_change_pct_3m` in a training notebook.
- The application team recomputes it in production code, subtly differently — a different
  window, or a different null-handling rule.
- The model receives inputs at inference time that do not match what it was trained on, and
  quietly degrades. This is **training/serving skew**.

**Amazon SageMaker Feature Store** is a purpose-built repository for engineered features:

| Concept | Meaning |
|---|---|
| **Feature group** | A named schema — a table of features sharing a record identifier and an event time |
| **Record identifier** | The key, e.g. `account_id` |
| **Event time** | The timestamp each feature value became true |
| **Online store** | Low-latency lookup for real-time inference |
| **Offline store** | Historical values in S3 for training and batch scoring |

The online and offline stores are populated from the same ingestion, so **training and
inference read the same definition of each feature**. The event time makes **point-in-time
correct** training sets possible: when building a training row for 1 March, you retrieve
feature values as they were on 1 March, not today's values. Without that, you leak the
future into the past.

### 4.4 Find it in the console

1. In the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/) left
   navigation, open **Feature Store** (under a data or governance grouping depending on
   your console version).
2. Read the **Feature groups** page. It is empty in a new account.
3. Note what creating a feature group would require: a name, a record identifier column, an
   event time column, a schema, and a choice of online store, offline store or both.

> **Cost note:** a feature group with an **online store** enabled provisions capacity and
> incurs ongoing charges; an offline-only store is S3 storage. This lab does not create
> one. If you experiment beyond the lab, delete the feature group afterwards.

### 4.5 Sketch your feature group

On paper, define the feature group you would create for Northwind:

- **Name:** `northwind-account-features`
- **Record identifier:** `account_id`
- **Event time:** `feature_date`
- **Features:** the seven from 4.1, each with a type
- **Stores:** offline for training; online as well, if the retention offer needs to be
  decided live rather than in a monthly batch

That last decision links straight back to Lab 01: **real-time inference needs an online
store; a monthly batch job does not.**

---

## Step 5 — Train, tune and evaluate

Stages 6, 7 and 8. You ran stage 6 by hand in Lab 04; this step adds the two that surround
it.

### 5.1 Training, in one paragraph

Choose an algorithm suited to the data type — XGBoost or Linear Learner for tabular, a
neural network for images or text, or a foundation model where the task is generative.
Supply the training and validation channels, set hyperparameters, and run the job. Training
bills only while it runs.

For Northwind: **XGBoost, binary classification, tabular** — the same shape as Lab 04.

### 5.2 Underfitting, overfitting, and the bias-variance trade-off

| Condition | Training performance | Validation performance | Cause | Fix |
|---|---|---|---|---|
| **Underfitting** | Poor | Poor | Model too simple, features too weak, trained too briefly | More capacity, better features, more rounds |
| **Good fit** | Good | Good, close to training | — | — |
| **Overfitting** | Excellent | Noticeably worse | Model memorised the training set | More data, fewer features, regularisation, early stopping, simpler model |

- **Bias** (in the statistical sense) is error from an over-simple model — it underfits.
- **Variance** is error from over-sensitivity to the training sample — it overfits.
- Reducing one tends to raise the other. Finding the balance is what tuning does.

> Note the collision of vocabulary: **statistical bias** here means systematic model error.
> **Societal bias** — unfair outcomes across demographic groups — is a different concept,
> covered in Domain 4 and Lab 20. The exam uses both senses.

### 5.3 Hyperparameter tuning

Manually guessing `max_depth` and `eta` as you did in Lab 04 does not scale. **SageMaker
automatic model tuning (AMT)** runs many training jobs across a hyperparameter search space
and returns the best.

1. In the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/) left
   navigation, open **Hyperparameter tuning jobs** (near Training jobs).
2. The list is empty. Note what a tuning job specifies:
   - The **objective metric** to optimise, e.g. `validation:auc`, and whether to maximise
     or minimise it
   - **Ranges** for each hyperparameter to search
   - The **maximum number of training jobs** and how many run in **parallel**
   - The **search strategy** — Bayesian (learns from previous trials), random, grid, or
     Hyperband (stops unpromising jobs early)

> **⚠️ Cost warning:** a tuning job launches *many* training jobs. Cost scales with the
> maximum-jobs setting. Always cap it. This lab does not run one.

### 5.4 Evaluation

Evaluate on the **test split**, untouched until now.

For Northwind's binary classifier, use the metrics from Lab 04 — accuracy, precision,
recall, F1, AUC-ROC — with two additions:

- With churn at perhaps 3%, a model that predicts "no churn" for everyone scores **97%
  accuracy** and is worthless. Accuracy is the wrong headline metric here.
- The actual business constraint is "5,000 offers a month". So the right metric is
  **precision within the top 5,000 ranked accounts** — of the 5,000 you contact, how many
  would really have churned? That is a ranking question, which is why AUC and
  precision-at-k beat accuracy for this problem.

For **regression** problems the metric set is different, and the exam expects both:

| Metric | Meaning |
|---|---|
| **MAE** | Mean absolute error — average size of error, in the units of the target |
| **MSE / RMSE** | Squared error; punishes large errors much more heavily |
| **R²** | Proportion of variance explained |

### 5.5 Evaluate for more than accuracy

A complete evaluation also asks:

- **Is performance equal across segments?** Overall AUC can hide a model that works well
  for urban accounts and badly for rural ones. **SageMaker Clarify** measures this — Lab 20.
- **Can we explain individual predictions?** Feature attribution, also Clarify — Lab 21.
- **What is the cost of each error type?** A false positive is a wasted discount; a false
  negative is a lost customer. They are rarely equal, and that inequality should set the
  threshold.

---

## Step 6 — Deploy, monitor and close the loop

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

---

## Step 7 — Clean up

Most of this lab was console navigation and design, which creates nothing. The one section
that can leave a chargeable resource running is the optional Data Wrangler walkthrough in
Step 3.4.

> **⚠️ COST WARNING:** a **SageMaker Canvas session** or **Studio application** bills per
> hour for as long as it runs. **Closing the browser tab does not stop it.** If you did
> Step 3.4, section 7.4 below is not optional.

### 7.1 Confirm no endpoints are running

Carry the Lab 04 habit forward. In the
[Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/), check that
**Endpoints** is empty. If anything from Lab 04 survives, delete it now — it has been
billing since then.

### 7.2 Check for feature groups

If you experimented beyond Step 4.4 and created a **feature group**:

1. Open **Feature Store** → **Feature groups**.
2. Select the group and delete it. A feature group with an **online store** enabled
   provisions capacity and bills continuously.
3. Deleting the feature group does not remove the **offline store** data in S3 — delete
   those objects separately from the S3 console.

### 7.3 Check for tuning and processing jobs

1. Open **Hyperparameter tuning jobs**. If one is running, **stop it** — a tuning job
   launches many training jobs and cost scales with the number.
2. Open **Processing jobs**. These end on their own, but confirm none is stuck running.

### 7.4 Shut down Data Wrangler, Canvas and Studio applications

**Do this if you completed Step 3.4.**

1. In the SageMaker console, open **Domains** and select your domain.
2. Open your user profile and review the running **applications**.
3. Delete every running app — JupyterLab, Code Editor, Canvas, and any Data Wrangler
   session.
4. If you used **SageMaker Canvas**, open Canvas and choose **Log out** from the left
   navigation. Logging out is what ends the Canvas session; closing the tab does not.

Verify with the CLI:

```bash
aws sagemaker list-apps --region us-east-1
```

Any app with status `InService` is still billing. Delete it.

### 7.5 Clean up S3

Delete any files you imported for the Data Wrangler flow, along with the flow's exported
output. If you still have the Lab 02 bucket, remove it now.

```bash
aws s3 ls
```

### 7.6 Full account sweep

You have now finished Domain 1. Run a complete check before moving to Domain 2:

```bash
aws sagemaker list-endpoints --region us-east-1
aws sagemaker list-notebook-instances --region us-east-1
aws sagemaker list-apps --region us-east-1
aws sagemaker list-feature-groups --region us-east-1
aws sagemaker list-hyper-parameter-tuning-jobs --region us-east-1
aws comprehend list-endpoints --region us-east-1
aws s3 ls
```

Everything should be empty or terminal. Then open **Billing and Cost Management** →
**Bills** and review the month's charges by service. Anything unexpected is worth
investigating now, while you still remember what you created.

### 7.7 Keep

Save your completed ten-stage pipeline from Step 6.5. It is a single-page summary of
Domain 1 task statement 1.3 and the best revision artefact you will produce in this course.

---

## Verification

- [ ] You wrote the Northwind ML question as a prediction, not as a business goal, with both a model metric and a business metric
- [ ] You produced a ten-line pipeline in Step 1.3 and completed it in Step 6.5
- [ ] You identified `cancellation_reason_code` as target leakage and can explain the test that catches it
- [ ] You can explain why a random row-level split is wrong for this dataset, and what to split by instead
- [ ] You listed at least five engineered features and can name the pattern each one follows
- [ ] You located Feature Store, Processing jobs, Hyperparameter tuning jobs, Model Monitor, Pipelines and Model registry in the SageMaker console
- [ ] You can state why accuracy is the wrong headline metric at a 3% churn rate
- [ ] You justified batch transform over a real-time endpoint for this scenario
- [ ] No SageMaker endpoint, notebook instance, Studio or Canvas application, or feature group is running in your account

## Discussion questions

1. Northwind's model performs well for three months and then degrades sharply. Walk through how you would diagnose whether this is data drift, concept drift or a broken pipeline, and say which SageMaker monitor would have caught each first.
2. The data science team wants to add `avg_ticket_sentiment` from Amazon Comprehend as a feature. What must be true about how that value is computed at training time and at inference time, and which service exists specifically to guarantee it?
3. The marketing director asks for "the most accurate model possible". Rewrite that request as a set of requirements a data scientist could actually build against, and explain what you would have to ask about the cost of a false positive versus a false negative.

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.
