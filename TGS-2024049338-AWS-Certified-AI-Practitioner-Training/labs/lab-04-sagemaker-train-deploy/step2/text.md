# Step 2 — Create a SageMaker notebook instance

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
