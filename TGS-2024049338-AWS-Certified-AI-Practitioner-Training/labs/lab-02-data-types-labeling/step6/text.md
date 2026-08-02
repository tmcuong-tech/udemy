# Step 6 — Clean up

Remove everything you created so the account is clean before Lab 03.

> **Cost warning:** S3 storage bills for as long as objects exist, and a Ground Truth
> private workforce keeps an Amazon Cognito user pool in your account. Neither is expensive
> at this scale, but leaving orphaned buckets and user pools around is how lab accounts
> accumulate cost and clutter.

### 6.1 Stop any running labelling job

1. Open the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/) →
   **Ground Truth** → **Labeling jobs**.
2. If your job is still **In progress**, select it and choose **Stop**. A stopped or
   completed labelling job consumes nothing further — it is a job, not a standing resource.

### 6.2 Delete the private work team

1. Go to **Ground Truth** → **Labeling workforces** → **Private**.
2. Select `aif-lab02-team` and delete it.
3. Ground Truth created an **Amazon Cognito user pool** to back the workforce. If you do
   not intend to run further labelling labs, open the **Amazon Cognito** console, find the
   user pool created for the workforce, and delete it too. If you are unsure which pool it
   is, leave it — an empty user pool has no ongoing charge — and note it for later review.

### 6.3 Empty and delete the S3 bucket

1. Open the [Amazon S3 console](https://console.aws.amazon.com/s3/).
2. Select your `aif-lab02-...` bucket and choose **Empty**. Type `permanently delete` to
   confirm. This removes your uploads *and* everything Ground Truth wrote to `output/`.
3. With the bucket still selected, choose **Delete** and confirm with the bucket name.

Or, with the AWS CLI:

```bash
aws s3 rm s3://<your-bucket> --recursive
aws s3 rb s3://<your-bucket>
```

### 6.4 Verify

```bash
aws s3 ls
aws sagemaker list-labeling-jobs --region us-east-1
```

Your lab bucket should be gone, and the labelling job should show a terminal status
(`Completed` or `Stopped`) rather than `InProgress`.

### 6.5 Keep

Before deleting the bucket, download a copy of `output.manifest` if you want to keep an
example of an augmented manifest for revision. Also keep your classification table from
Step 1 — Lab 05 builds on it.
