# Step 7 — Clean up

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
