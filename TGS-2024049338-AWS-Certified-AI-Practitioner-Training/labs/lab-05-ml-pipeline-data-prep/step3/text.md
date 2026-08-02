# Step 3 — Pre-process the data

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
