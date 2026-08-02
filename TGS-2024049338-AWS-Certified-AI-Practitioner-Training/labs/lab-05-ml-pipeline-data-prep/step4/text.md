# Step 4 — Engineer features and store them

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
