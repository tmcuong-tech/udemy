# Lab 04 — Train and Deploy a Model with SageMaker

Train a binary classifier with the SageMaker built-in XGBoost algorithm, deploy it to a real-time endpoint, evaluate it, and delete every billing resource.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 1 — Fundamentals of AI and ML (20%)
**Task statement:** 1.3 Describe the ML development lifecycle
**WSQ mapping:** LU4 · Topic 7 Developing ML Solutions · K3 · A4 · LO4
**Slide reference:** v11 deck slides 84–135
**Estimated time:** 45 minutes

> **⚠️ COST WARNING:** this lab creates a SageMaker notebook instance and a real-time
> inference endpoint. **Both bill continuously until deleted, whether you use them or not.**
> Step 7 removes everything — do not skip it. If you must stop part-way through, go
> straight to Step 7.

**Learning objectives:**
- Explain the SageMaker cost model and identify which resources bill continuously versus per job
- Create a notebook instance and describe the role of the SageMaker execution role
- Prepare tabular data into train, validation and test splits in the format a built-in algorithm requires
- Run a training job with the built-in XGBoost algorithm and interpret its console record
- Deploy a model as a real-time endpoint and explain the model, endpoint configuration and endpoint objects
- Evaluate a classifier using accuracy, precision, recall, F1 and AUC, and explain how the decision threshold trades precision against recall
- Delete every chargeable resource and verify the account is clean

---

## Step 1 — Read the cost warning and plan the run

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

---

## Step 2 — Create a SageMaker notebook instance

The notebook instance is your development environment. It is a managed EC2 instance with
Jupyter, the SageMaker Python SDK and an IAM role already attached.

> **⚠️ This instance bills per hour from the moment its status becomes `InService`.**
> Note the time you start it.

### 2.1 Create the instance

1. Open the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/) in
   `us-east-1`.
2. In the left navigation, find **Notebook instances** (under the notebook or applications
   grouping, depending on your console version) and choose **Create notebook instance**.
3. **Notebook instance name:** `aif-lab04-notebook`.
4. **Notebook instance type:** `ml.t3.medium`.
5. **Platform identifier / volume size:** leave the defaults.
6. Under **Permissions and encryption → IAM role**, choose **Create a new role**.
   - For **S3 buckets you specify**, choose **Any S3 bucket** for this lab, or restrict it
     to your own bucket if you prefer. The role is created with the
     `AmazonSageMakerFullAccess` managed policy plus S3 access.
   - Choose **Create role**.
7. Leave networking, Git repositories and lifecycle configuration at their defaults.
8. Choose **Create notebook instance**.

Status goes **Pending** → **InService**, usually in about five minutes.

### 2.2 Understand the execution role

While you wait, note what just happened, because the exam tests it:

- The notebook instance runs **as an IAM role**, not as your user. Anything the notebook
  does — creating training jobs, reading S3, deploying endpoints — is authorised by that
  role.
- `AmazonSageMakerFullAccess` is broad. It is fine for a lab; in production you would scope
  the role down to the specific buckets and actions required. Lab 23 revisits this.
- The **execution role** is passed to every training job and endpoint you create. That is
  how a training job running in AWS-managed infrastructure gets permission to read *your*
  training data from *your* bucket.

### 2.3 Open Jupyter

1. When the status is **InService**, choose **Open JupyterLab** (or **Open Jupyter**).
2. Create a new notebook and choose the **`conda_python3`** kernel. This kernel has the
   SageMaker Python SDK, boto3, pandas and scikit-learn already installed.
3. In the first cell, confirm the environment:

```python
import sagemaker, boto3
sess = sagemaker.Session()
role = sagemaker.get_execution_role()
bucket = sess.default_bucket()
region = sess.boto_region_name

print("SDK version:", sagemaker.__version__)
print("Region:", region)
print("Default bucket:", bucket)
print("Execution role:", role)
```

Run the cell (Shift+Enter). You should see a region, an S3 bucket name beginning
`sagemaker-`, and a role ARN.

The **default bucket** is created automatically by the SDK in your account and Region. Note
its name — you will empty it in Step 7.

---

## Step 3 — Prepare the dataset and upload it to S3

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

---

## Step 4 — Train a model with the built-in XGBoost algorithm

Now run the training job. This is where the algorithm meets the data and produces a model
artefact.

> **Cost note:** a training job bills only for the seconds it runs, then the instance is
> torn down automatically. This job should take a few minutes. Training is *not* the
> expensive part of this lab — the endpoint in Step 6 is.

### 4.1 Get the algorithm container

```python
from sagemaker.image_uris import retrieve

container = retrieve(framework="xgboost", region=region, version="1.7-1")
print(container)
```

`retrieve` returns the URI of the AWS-managed container image holding the built-in
algorithm. You did not build it, do not maintain it, and do not pay for it separately —
this is what "built-in algorithm" means in practice.

> **Note:** if this call reports that the version is unavailable, list the versions your
> SDK supports and choose a current one. Do not hard-code a version you have not verified.

### 4.2 Configure the estimator

```python
from sagemaker.estimator import Estimator

xgb = Estimator(
    image_uri=container,
    role=role,
    instance_count=1,
    instance_type="ml.m5.large",
    output_path=f"s3://{bucket}/{prefix}/output",
    sagemaker_session=sess,
    base_job_name="aif-lab04-xgboost",
)
```

Read each argument as a piece of exam vocabulary:

- `image_uri` — the **algorithm**.
- `role` — the **execution role** from Step 2.2, which lets the job read your S3 data.
- `instance_type` / `instance_count` — the **training compute**, separate from the
  inference compute you choose later. They do not have to match.
- `output_path` — where the **model artefact** (`model.tar.gz`) will be written.

### 4.3 Set hyperparameters

```python
xgb.set_hyperparameters(
    objective="binary:logistic",
    num_round=100,
    max_depth=5,
    eta=0.2,
    subsample=0.8,
    eval_metric="auc",
)
```

These are **hyperparameters** — you set them *before* training. Contrast them with the
tree structures XGBoost learns, which are **parameters**.

| Hyperparameter | Effect | Increase it and… |
|---|---|---|
| `num_round` | Number of boosting rounds | More capacity, more risk of overfitting |
| `max_depth` | Maximum tree depth | More complex interactions, more overfitting |
| `eta` | Learning rate | Faster convergence, less stable |
| `subsample` | Fraction of rows sampled per round | Lower values add regularisation |

`objective="binary:logistic"` declares this a binary classification problem returning a
probability. Changing it to a regression objective would change the whole task.

### 4.4 Run the training job

```python
from sagemaker.inputs import TrainingInput

xgb.fit({
    "train": TrainingInput(train_uri, content_type="text/csv"),
    "validation": TrainingInput(val_uri, content_type="text/csv"),
})
```

Watch the streamed log. Two things to observe:

1. The per-round `train-auc` and `validation-auc` values. If training AUC keeps improving
   while validation AUC stalls or falls, that is **overfitting** — the model is memorising
   the training set rather than learning a generalisable pattern.
2. The final lines report **billable seconds**, which is the concrete meaning of "training
   bills only while it runs".

### 4.5 Inspect the job in the console

1. Open the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/) → in the
   left navigation, **Training jobs**.
2. Select the job that begins `aif-lab04-xgboost-`.
3. Note on the detail page:
   - **Algorithm / image** — the container from 4.1
   - **Hyperparameters** — exactly what you set in 4.3
   - **Input data configuration** — the two S3 channels, `train` and `validation`
   - **S3 model artifact** — the path to `model.tar.gz`
   - **Monitor** — links to CloudWatch metrics and logs
4. Confirm the status is **Completed** and note the **Billable time**.

This page is the answer to "how do I reproduce this model six months from now?" — the job
record captures the data location, the algorithm, the hyperparameters and the output.

---

## Step 5 — Deploy the model to a real-time endpoint

Training produced a model artefact in S3. That artefact predicts nothing until it is
hosted. Deployment creates three linked SageMaker objects and one running fleet.

> ## ⚠️ COST WARNING
>
> **The endpoint you create in this step bills continuously, per hour, from the moment its
> status becomes `InService` — whether you send it requests or not.**
>
> Do not leave this lab without completing Step 7. If you are interrupted now, run
> `predictor.delete_endpoint(delete_endpoint_config=True)` before you close the notebook.

### 5.1 What deployment creates

| Object | What it is |
|---|---|
| **Model** | A pointer to the `model.tar.gz` artefact plus the inference container image and the execution role |
| **Endpoint configuration** | The deployment recipe — which model(s), which instance type, how many instances, traffic split |
| **Endpoint** | The running HTTPS service backed by those instances |

The separation matters: because the *configuration* is a distinct object, you can create a
new one and update the endpoint in place — which is how blue/green and canary deployments
work, and how A/B testing across model variants is done. All three objects must be deleted
separately in Step 7.

### 5.2 Deploy

```python
from sagemaker.serializers import CSVSerializer

predictor = xgb.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large",
    endpoint_name="aif-lab04-endpoint",
    serializer=CSVSerializer(),
)

print("Endpoint:", predictor.endpoint_name)
```

This takes a few minutes. The serializer tells the SDK to send your Python data to the
endpoint as CSV, which is what the XGBoost container expects.

### 5.3 Watch it appear in the console

While it deploys, open the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/)
and check all three lists in the left navigation under the inference section:

1. **Models** — a new model object.
2. **Endpoint configurations** — a new configuration.
3. **Endpoints** — `aif-lab04-endpoint`, status **Creating**, then **InService**.

Compare this with Lab 01 Step 4.3, where all three lists were empty. You have now filled
in the whole picture.

### 5.4 Note the alternatives you did not choose

You deployed a **real-time endpoint** because this lab needs an interactive prediction. For
the same trained model you could instead have used:

- **Batch transform** — score `test_df` as a file, no standing resource, cheapest for bulk.
- **Serverless inference** — no instance to choose, scales to zero, accepts cold starts.
- **Asynchronous inference** — queued, for large payloads or long inference times.

The model artefact is identical in every case. **The deployment option is a separate
decision from the model**, driven by latency, traffic pattern and payload size. That
separation is exactly what the exam tests.

---

## Step 6 — Run inference and evaluate the model

The endpoint is live. Send it the held-back test data and find out how good the model
actually is.

### 6.1 Predict a single record

```python
X_test = test_df.drop(columns=["target"])
y_test = test_df["target"].values

single = X_test.iloc[0].tolist()
result = predictor.predict(single).decode("utf-8")
print("Raw response:", result)
print("Actual label:", y_test[0])
```

The endpoint returns a **probability** between 0 and 1, not a class. That is what
`objective="binary:logistic"` asked for.

### 6.2 Apply a threshold

```python
prob = float(result)
threshold = 0.5
predicted_class = 1 if prob >= threshold else 0
print(f"probability={prob:.4f}  predicted={predicted_class}  actual={y_test[0]}")
```

**The threshold is a business decision, not a model property.** Lowering it catches more
positives at the cost of more false alarms. In a medical screening context you would
lower it deliberately, because a missed positive costs far more than a false alarm.

### 6.3 Score the whole test set

```python
import numpy as np

payload = "\n".join(",".join(str(v) for v in row) for row in X_test.values)
raw = predictor.predict(payload).decode("utf-8")
probs = np.array([float(p) for p in raw.strip().split("\n")])
preds = (probs >= 0.5).astype(int)

print("predictions:", preds.shape)
```

### 6.4 Build the confusion matrix

```python
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

tn, fp, fn, tp = confusion_matrix(y_test, preds).ravel()

print(f"True negatives : {tn}")
print(f"False positives: {fp}")
print(f"False negatives: {fn}")
print(f"True positives : {tp}")
print()
print(f"Accuracy : {accuracy_score(y_test, preds):.4f}")
print(f"Precision: {precision_score(y_test, preds):.4f}")
print(f"Recall   : {recall_score(y_test, preds):.4f}")
print(f"F1       : {f1_score(y_test, preds):.4f}")
print(f"AUC      : {roc_auc_score(y_test, probs):.4f}")
```

Learn these definitions — Domain 1 and Domain 3 both test them:

| Metric | Formula | Answers |
|---|---|---|
| **Accuracy** | (TP + TN) / all | What fraction did it get right? Misleading when classes are imbalanced. |
| **Precision** | TP / (TP + FP) | Of the ones it flagged, how many were real? Optimise when false positives are costly. |
| **Recall (sensitivity)** | TP / (TP + FN) | Of the real ones, how many did it catch? Optimise when misses are costly. |
| **F1** | Harmonic mean of precision and recall | A single balanced score. |
| **AUC-ROC** | Area under the ROC curve | Ranking quality across *all* thresholds, independent of the one you chose. |

Precision and recall trade off against each other; moving the threshold in 6.2 moves you
along that trade-off. AUC does not depend on the threshold at all, which is why it is the
better headline number when the operating point is still undecided.

### 6.5 Try moving the threshold

```python
for t in [0.2, 0.35, 0.5, 0.65, 0.8]:
    p = (probs >= t).astype(int)
    print(f"threshold={t:<5} precision={precision_score(y_test, p):.3f}  recall={recall_score(y_test, p):.3f}")
```

Watch precision rise and recall fall as the threshold increases. **The model did not
change** — only the decision rule you wrapped around it. This is one of the most useful
practical insights in the whole course.

### 6.6 Invoke from outside the SDK (optional)

The endpoint is an ordinary HTTPS service any authorised application can call:

```python
import boto3, json

runtime = boto3.client("sagemaker-runtime", region_name=region)
row = ",".join(str(v) for v in X_test.iloc[1].values)

response = runtime.invoke_endpoint(
    EndpointName="aif-lab04-endpoint",
    ContentType="text/csv",
    Body=row,
)
print(response["Body"].read().decode("utf-8"))
```

This is what a web application, a Lambda function or an API Gateway integration would do.
The model is now a piece of infrastructure, not a notebook artefact.

**Now go straight to Step 7 and delete the endpoint.**

---

## Step 7 — Clean up

> ## ⚠️ DO NOT SKIP THIS STEP
>
> The endpoint and the notebook instance created in this lab **bill continuously until you
> delete them**. An endpoint left running overnight costs money for every idle hour. Work
> through every item below and verify at the end.

Delete in this order: endpoint → endpoint configuration → model → notebook instance →
S3 objects.

### 7.1 Delete the endpoint, endpoint configuration and model

From the notebook, the fastest route:

```python
predictor.delete_endpoint(delete_endpoint_config=True)
predictor.delete_model()
print("endpoint, endpoint config and model deleted")
```

If your notebook session has been lost, use the AWS CLI:

```bash
aws sagemaker delete-endpoint --endpoint-name aif-lab04-endpoint --region us-east-1
aws sagemaker delete-endpoint-config --endpoint-config-name aif-lab04-endpoint --region us-east-1
aws sagemaker list-models --region us-east-1
aws sagemaker delete-model --model-name <model-name-from-the-list> --region us-east-1
```

Or in the [SageMaker console](https://console.aws.amazon.com/sagemaker/), delete each of
these in turn from the left navigation under the inference section:

1. **Endpoints** → select `aif-lab04-endpoint` → **Delete**
2. **Endpoint configurations** → select the matching configuration → **Delete**
3. **Models** → select the model → **Delete**

**Deleting the endpoint alone stops the billing.** Deleting the configuration and model as
well keeps the account tidy and prevents an accidental redeploy.

### 7.2 Stop and delete the notebook instance

1. In the SageMaker console, open **Notebook instances**.
2. Select `aif-lab04-notebook` and choose **Stop**. Wait for the status to become
   **Stopped** — billing for the instance ends here.
3. With the status **Stopped**, choose **Actions → Delete** and confirm.

> A **stopped** notebook instance no longer bills for compute, but its EBS volume still
> incurs a small storage charge. Delete it, not just stop it, unless you plan to return
> tomorrow.

### 7.3 Check for Studio applications

If you explored SageMaker Studio at any point in Labs 01–04:

1. In the SageMaker console, open **Domains**.
2. Open your domain, then your user profile.
3. Delete any running **applications** (JupyterLab, Code Editor, Canvas). A running Studio
   app bills per hour exactly like a notebook instance, and closing the browser tab does
   not stop it.
4. In **SageMaker Canvas**, use **Log out** to end the session — closing the tab leaves it
   running.

### 7.4 Empty the S3 data

The SageMaker default bucket now holds your training CSVs and the model artefact.

```bash
aws s3 rm s3://<sagemaker-default-bucket>/aif-lab04-xgboost --recursive
```

Or in the S3 console, open the `sagemaker-...` bucket, select the `aif-lab04-xgboost/`
prefix and choose **Delete**. You can keep the bucket itself — the SDK reuses it — but
delete the objects.

### 7.5 Verify everything is gone

```bash
aws sagemaker list-endpoints --region us-east-1
aws sagemaker list-endpoint-configs --region us-east-1
aws sagemaker list-models --region us-east-1
aws sagemaker list-notebook-instances --region us-east-1
aws sagemaker list-apps --region us-east-1
```

**Every one of these must return an empty list** (or contain only resources that predate
this lab). If `list-endpoints` returns anything, delete it now.

### 7.6 Confirm in Billing

Open the **Billing and Cost Management** console and check **Bills** for the current month.
SageMaker charges appear within a few hours, so also check again tomorrow. Note that the
**training job** charge is a one-off for a few minutes, while any endpoint charge would
keep growing — the clearest possible illustration of why this step exists.

---

## Verification

- [ ] A billing budget with an alert exists in your account
- [ ] The notebook instance reached **InService** and `sagemaker.__version__`, the Region, the default bucket and the role ARN all printed
- [ ] `train.csv` and `validation.csv` exist in S3 under `aif-lab04-xgboost/`, with the target in the first column and no header row
- [ ] The training job shows status **Completed**, and you noted its billable time and model artefact path
- [ ] All three of Models, Endpoint configurations and Endpoints contained an entry after deployment
- [ ] You produced a confusion matrix and can state what each of TP, FP, TN and FN means for this dataset
- [ ] You observed precision rise and recall fall as the threshold increased, without retraining
- [ ] **The endpoint is deleted** — `aws sagemaker list-endpoints` returns an empty list
- [ ] The endpoint configuration, model, and notebook instance are deleted, and no Studio app is running
- [ ] The `aif-lab04-xgboost/` objects have been removed from the S3 default bucket

## Discussion questions

1. Your training AUC reaches 0.99 while validation AUC sits at 0.82. Name the problem, then give three distinct changes you could make — one to the data, one to the hyperparameters, one to the algorithm choice.
2. This model screens for a medical condition. Where would you set the threshold, and what would you have to build around the endpoint to make that choice safe in practice?
3. The same trained artefact could be served by a real-time endpoint, batch transform, serverless inference or asynchronous inference. For each of the four, describe a workload where it is clearly the right answer and state what would make it the wrong one.

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.
