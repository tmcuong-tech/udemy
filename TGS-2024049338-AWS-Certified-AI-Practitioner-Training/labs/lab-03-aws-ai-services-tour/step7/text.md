# Step 7 — Clean up

Managed AI services bill **per unit processed**, so an idle account costs nothing for
Comprehend, Translate, Polly, Transcribe or Rekognition. The only standing resources you
created are in Amazon S3, plus any custom assets.

> **Cost warning:** none of the five services in this lab leaves a continuously billing
> resource behind — unlike SageMaker endpoints in Lab 04. Storage in S3 *does* bill for as
> long as objects exist, including the transcript JSON and the MP3.

### 7.1 Delete transcription job artefacts

1. Open the [Amazon Transcribe console](https://console.aws.amazon.com/transcribe/) →
   **Transcription jobs**.
2. Select `aif-lab03-transcribe` and delete it. The job record itself carries no ongoing
   charge, but deleting keeps the list clean and removes the transcript held in the
   service-managed bucket.
3. If you have any **custom vocabularies**, **vocabulary filters** or **custom language
   models** from Step 4.2, delete those too.

### 7.2 Empty and delete the S3 bucket

1. Open the [Amazon S3 console](https://console.aws.amazon.com/s3/).
2. Select your `aif-lab03-...` bucket, choose **Empty**, and confirm. This removes the MP3
   and any transcript JSON.
3. Choose **Delete** and confirm with the bucket name.

Or with the AWS CLI:

```bash
aws s3 rm s3://<your-bucket> --recursive
aws s3 rb s3://<your-bucket>
```

### 7.3 Check for other assets

Confirm you did not leave anything behind in the services you toured:

- **Amazon Comprehend** — check the custom classification and custom entity recognition
  pages. If you started an endpoint for a custom model, **delete it immediately**: a
  Comprehend endpoint provisions throughput and bills continuously until deleted. This lab
  did not ask you to create one.
- **Amazon Translate** — check for any custom terminology or parallel data resources.
- **Amazon Polly** — check for lexicons, and delete any you created.
- **Amazon Rekognition** — check that no **Custom Labels** project or model is running. A
  running Custom Labels model bills per inference hour.

### 7.4 Verify

```bash
aws s3 ls
aws transcribe list-transcription-jobs --region us-east-1
aws comprehend list-endpoints --region us-east-1
```

The bucket should be gone and the endpoint list empty.

### 7.5 Check billing

Open the **Billing and Cost Management** console and review the current month's charges by
service. Because these services bill per unit, this is a good opportunity to see how small
per-call charges actually are.

### 7.6 Keep

Save your completed table from Step 6.1 and your answers to Step 6.2. Domain 1 task
statement 1.2 is largely tested through exactly that kind of service-to-use-case matching.
