# Step 4 — Create a SageMaker Ground Truth labelling job

Ground Truth turns the unlabelled images in your `images/` prefix into a labelled dataset,
using a **private work team** made up of you.

> **Cost note:** Ground Truth charges per labelled object, and a private workforce is
> backed by an Amazon Cognito user pool. Charges for a handful of images are very small,
> but confirm current rates on the AWS pricing page for SageMaker before running larger
> jobs. Nothing in this step creates an always-on compute resource.

### 4.1 Create a private work team

1. Open the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/) in
   `us-east-1`.
2. In the left navigation, under **Ground Truth**, choose **Labeling workforces**.
3. Select the **Private** tab, then choose **Create private team**.
4. Choose to create a team with **AWS Cognito** and invite new workers by email.
5. **Team name:** `aif-lab02-team`.
6. **Email addresses:** your own address. Add an organisation name and a contact email if
   the form asks for them.
7. Choose **Create private team**.

You will receive an email with a **labelling portal URL**, your user name, and a temporary
password. Keep it — you need it in Step 5. The portal URL is also shown on the
**Private** tab under the team's details.

### 4.2 Create the labelling job

1. Still under **Ground Truth**, choose **Labeling jobs**, then **Create labeling job**.
2. **Job name:** `aif-lab02-image-classification`.
3. **Input data setup:** choose the automated data setup option, which builds the input
   manifest for you.
   - **S3 location for input datasets:** `s3://<your-bucket>/images/`
   - **S3 location for output datasets:** `s3://<your-bucket>/output/`
   - **Data type:** Image
   - Choose **Complete data setup**. Ground Truth scans the prefix and writes an input
     manifest — one JSON line per object. Wait for it to report success.
4. **IAM role:** choose **Create a new role**, and when prompted for S3 buckets, grant
   access to **specific S3 buckets** and enter your bucket name. Least privilege matters
   even in a lab.
5. **Task category:** **Image**. **Task type:** **Image Classification (Single Label)**.
6. Choose **Next**.

### 4.3 Configure workers and the task

1. **Worker types:** choose **Private**, then select `aif-lab02-team`.
2. Leave the task timeout and task expiration at their defaults.
3. In the labelling tool editor:
   - **Task description:** paste the one-sentence instruction you wrote in Step 3.3.
   - **Labels:** enter your two categories, one per box (for example `cat` and `dog`).
   - **Good and bad examples / full instructions:** paste your edge-case rule here. This
     text is what workers see when they choose **View full instructions**.
4. Use the preview pane to check the task renders sensibly.
5. Choose **Create**.

The job appears in the **Labeling jobs** list with status **In progress**. Ground Truth
has now distributed one task per image to your work team.

### 4.4 Inspect the input manifest (optional)

In S3, open the `output/` prefix and find the generated input manifest. Each line looks
like this:

```json
{"source-ref": "s3://your-bucket/images/photo1.jpg"}
```

That is what "unlabelled" means concretely — a pointer to an object, and nothing else.
Compare it with the output manifest you will read in Step 5.
