# Step 2 — Collect data and explore it

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
