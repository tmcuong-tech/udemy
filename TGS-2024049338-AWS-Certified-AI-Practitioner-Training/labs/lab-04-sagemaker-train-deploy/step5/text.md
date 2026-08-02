# Step 5 — Deploy the model to a real-time endpoint

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
