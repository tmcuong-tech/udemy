# Step 4 — Train a model with the built-in XGBoost algorithm

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
