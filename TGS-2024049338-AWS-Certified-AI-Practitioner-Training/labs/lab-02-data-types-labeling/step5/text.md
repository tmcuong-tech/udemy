# Step 5 — Label the images and read the output manifest

Now do the annotator's job yourself. Doing it by hand for ten images is the fastest way to
understand why labelling is the expensive part of supervised learning.

### 5.1 Sign in to the labelling portal

1. Open the labelling portal URL from the invitation email (or copy it from the
   **Private** tab of **Labeling workforces**).
2. Sign in with the user name and temporary password from the email. You will be asked to
   set a new password on first sign-in.
3. Your assigned task appears in the **Jobs** list. Select it and choose **Start working**.

> **Note:** tasks can take a minute or two to appear after the job is created. If the list
> is empty, wait and refresh.

### 5.2 Label the images

1. For each image, read the instruction, choose the correct category, and choose
   **Submit**.
2. Deliberately notice any image where you hesitate. That hesitation is the ambiguity your
   instructions failed to resolve — real annotators hit it constantly, and it is where
   label noise comes from.
3. Continue until all images are submitted. The portal returns you to the job list.

### 5.3 Watch the job complete

1. Return to **Ground Truth → Labeling jobs** in the SageMaker console.
2. Refresh until the status becomes **Completed**. The list shows how many objects were
   labelled and the **Output dataset location**.
3. Select the job name to open its detail page, which shows a sample of the labelled
   images with their assigned categories.

### 5.4 Read the output manifest

1. Open the [Amazon S3 console](https://console.aws.amazon.com/s3/) and navigate to
   `output/` → your job name → `manifests/` → `output/`.
2. Select `output.manifest` and use **Object actions → Query with S3 Select** if
   available, or download the file and open it in a text editor.
3. Each line is one labelled record. Its shape is:

```json
{
  "source-ref": "s3://your-bucket/images/photo1.jpg",
  "aif-lab02-image-classification": 0,
  "aif-lab02-image-classification-metadata": {
    "class-name": "cat",
    "confidence": 1,
    "human-annotated": "yes",
    "creation-date": "2026-01-01T00:00:00.000000",
    "type": "groundtruth/image-classification"
  }
}
```

> **Teaching note:** the JSON above is illustrative. Field values in your file will differ,
> and the exact key names include your own job name.

This file — an **augmented manifest** — is the deliverable. Compare it with the input
manifest from Step 4.4:

- The input had **one key**: a pointer to the object.
- The output adds **the label**, **who or what produced it** (`human-annotated: yes`), and
  **a confidence value**.

That triple — input, label, provenance — is what a supervised training job consumes. A
SageMaker training job can read this file directly in augmented manifest format, without
you reshaping it.

### 5.5 Connect it back to the data types

You have now produced labelled, unstructured image data. Ask yourself which of the other
files in your bucket would need the same treatment before supervised training:

- `customers.csv` — already labelled (`churned`). Ready.
- `demand.csv` — the target is the future value of the same series, so labels come from
  shifting the series in time rather than from human annotation.
- `reviews.txt` — unlabelled. It would need a sentiment label per review, either from
  humans via Ground Truth or from a pre-trained service such as Amazon Comprehend, which
  you use in Lab 03.
