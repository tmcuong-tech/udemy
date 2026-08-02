# Step 3 — Prepare the dataset and upload it to S3

SageMaker training jobs read from Amazon S3. This step produces the exact format the
built-in XGBoost algorithm expects and puts it there.

### 3.1 Load and inspect the data

In a new cell:

```python
import pandas as pd
from sklearn.datasets import load_breast_cancer

data = load_breast_cancer(as_frame=True)
df = data.frame

print(df.shape)
print(df["target"].value_counts())
df.head()
```

This is a small, well-known binary classification dataset bundled with scikit-learn: 30
numeric features per record and a 0/1 target. It stands in for any tabular business
problem — churn, default, defect.

Note the **class balance** printed above. A roughly balanced dataset means accuracy is a
reasonable headline metric; a heavily imbalanced one would not be. Lab 05 returns to this.

### 3.2 Put the target in the first column

The built-in XGBoost algorithm has a strict CSV contract:

- **The target must be the first column.**
- **No header row.**
- **No index column.**
- Numeric values only.

```python
cols = ["target"] + [c for c in df.columns if c != "target"]
df = df[cols]
df.head()
```

Getting this wrong is the most common cause of a failed XGBoost training job — the
algorithm will happily train on your target as if it were a feature and produce nonsense.

### 3.3 Split into train, validation and test

```python
from sklearn.model_selection import train_test_split

train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df["target"])
train_df, val_df = train_test_split(train_df, test_size=0.2, random_state=42, stratify=train_df["target"])

print("train:", train_df.shape, "validation:", val_df.shape, "test:", test_df.shape)
```

Three splits, three distinct jobs:

| Split | Used for | Seen by the algorithm? |
|---|---|---|
| **Training** | Fitting the model parameters | Yes, directly |
| **Validation** | Watching for overfitting during training and tuning hyperparameters | Yes, but only to score, not to fit |
| **Test** | A final honest estimate of performance | **No** — held back until the very end |

`stratify` keeps the class proportions the same in every split. Without it, a small split
can end up with a badly skewed class mix.

### 3.4 Write the CSVs and upload

```python
train_df.to_csv("train.csv", index=False, header=False)
val_df.to_csv("validation.csv", index=False, header=False)

prefix = "aif-lab04-xgboost"

train_uri = sess.upload_data("train.csv", bucket=bucket, key_prefix=f"{prefix}/train")
val_uri   = sess.upload_data("validation.csv", bucket=bucket, key_prefix=f"{prefix}/validation")

print(train_uri)
print(val_uri)
```

`index=False, header=False` is what satisfies the contract from 3.2 — check both flags.

### 3.5 Confirm in the S3 console

Open the [Amazon S3 console](https://console.aws.amazon.com/s3/), find the
`sagemaker-...` default bucket, and browse to `aif-lab04-xgboost/`. You should see the
`train/` and `validation/` prefixes with one CSV each.

You have now completed the *data* half of the pipeline. Keep `test_df` in memory in the
notebook — you will use it against the endpoint in Step 6.
