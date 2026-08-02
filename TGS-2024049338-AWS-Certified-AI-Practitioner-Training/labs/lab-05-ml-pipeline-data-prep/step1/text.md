# Step 1 — Frame the business problem and map the pipeline

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
