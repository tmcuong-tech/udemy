# Step 7 — Clean up

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
