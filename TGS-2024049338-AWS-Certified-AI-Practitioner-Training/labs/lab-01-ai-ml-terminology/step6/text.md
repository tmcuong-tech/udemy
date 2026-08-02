# Step 6 — Clean up

This lab was deliberately read-only, so there is little to remove. Run the checks anyway —
building the habit now prevents surprise charges in Lab 04, where you will create
resources that bill continuously.

### 6.1 Confirm you created nothing chargeable

1. In the **Amazon SageMaker AI** console, check each of these lists is still empty (or
   contains only resources that existed before this lab):
   - **Notebook instances** — a running notebook instance bills per hour.
   - **Domains** and any Studio **applications** (JupyterLab, Code Editor, Canvas) — a
     running Studio app bills per hour even when idle in a browser tab.
   - **Endpoints** — an endpoint bills continuously until deleted.
2. If you opened **SageMaker Studio** or **Canvas** during Step 3 and an application
   started, shut it down: open the domain, select your user profile, and delete or stop
   any running application. In Canvas, use **Log out** — closing the browser tab does not
   stop the session.

> **Cost warning:** SageMaker notebook instances, Studio applications, SageMaker Canvas
> sessions and inference endpoints all bill for wall-clock time, not for use. Closing the
> browser does not stop them.

### 6.2 Verify with the CLI (optional)

If you have the AWS CLI configured, these read-only commands confirm nothing is running:

```bash
aws sagemaker list-endpoints --region us-east-1
aws sagemaker list-notebook-instances --region us-east-1
aws sagemaker list-apps --region us-east-1
```

Each should return an empty list. If any returns a resource you do not recognise,
investigate before moving on.

### 6.3 Check billing

Open the **Billing and Cost Management** console and review **Bills** for the current
month. Get used to looking here after every lab in this course.

### 6.4 Keep your notes

Retain the classification tables from Steps 2, 3 and 5. They are the raw material for your
exam revision and are referenced again in Lab 05.
