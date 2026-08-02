# Lab 02 — Data Types and Labelling for ML

Classify structured, semi-structured and unstructured data, store samples in Amazon S3, and produce a labelled image dataset with SageMaker Ground Truth.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 1 — Fundamentals of AI and ML (20%)
**Task statement:** 1.1 Explain basic AI concepts and terminologies
**WSQ mapping:** LU2 · Topic 4 Fundamentals of ML and AI · K4 · A2 · LO2
**Slide reference:** v11 deck slides 25–51
**Estimated time:** 35 minutes

**Learning objectives:**
- Classify a dataset as structured, semi-structured or unstructured, and as tabular, time-series, image or text
- Store and organise ML datasets in Amazon S3 using key prefixes
- Explain why only labelled data can train a supervised model, and what makes labelling costly and error-prone
- Choose between a private, vendor and public Ground Truth workforce for a given data-sensitivity requirement
- Create and complete a Ground Truth image classification job, and interpret the augmented output manifest

---

## Step 1 — Classify structured, semi-structured and unstructured data

Before you store or label anything, you need the vocabulary. AIF-C01 asks you to identify
a data type from a description and to pick a service that suits it.

### 1.1 The three structural categories

| Category | Definition | Examples | Where it usually lives |
|---|---|---|---|
| **Structured** | Fixed schema; rows and columns defined in advance | Sales table, sensor readings, transaction ledger | Relational database, data warehouse, CSV/Parquet in S3 |
| **Semi-structured** | Self-describing tags or keys, but no rigid schema | JSON, XML, log lines, key-value documents | Amazon DynamoDB, JSON files in S3 |
| **Unstructured** | No predefined model; meaning is in the content itself | Images, audio, video, free-text documents, email | Amazon S3 |

The practical consequence: **structured data is usually ready for classical ML
(XGBoost, Linear Learner) with modest preparation; unstructured data usually needs deep
learning or a managed AI service**, because the useful features are not sitting in
columns.

### 1.2 The four data types you must recognise

| Type | Shape | Distinguishing feature | Typical model or service |
|---|---|---|---|
| **Tabular** | Rows = records, columns = features | Order of rows does not matter | XGBoost, Linear Learner |
| **Time-series** | Values indexed by timestamp | Order *does* matter; past predicts future | Forecasting models |
| **Image** | Pixel grids | Spatial structure | Convolutional networks, Amazon Rekognition |
| **Text** | Sequences of tokens | Sequential and contextual | Language models, Amazon Comprehend |

> **Exam tip:** the giveaway for time-series is that reordering the rows would destroy the
> signal. A table of customers is tabular; a table of one customer's monthly balance is
> time-series.

### 1.3 Classify these

| # | Dataset | Structural category | Data type |
|---|---|---|---|
| 1 | A CSV of 50,000 loan applications with 14 columns | | |
| 2 | Five years of hourly electricity demand | | |
| 3 | 3,000 JPEG photos of warehouse shelves | | |
| 4 | 20,000 customer support emails | | |
| 5 | Application logs in JSON, one object per line | | |

**Answer key:** 1 = structured / tabular · 2 = structured / time-series ·
3 = unstructured / image · 4 = unstructured / text · 5 = semi-structured / text (log data).

Keep this table — you will store one example of each in Step 2.

---

## Step 2 — Create an S3 bucket and organise a dataset

Amazon S3 is the default landing zone for ML data on AWS. SageMaker training jobs,
Ground Truth labelling jobs and batch transform jobs all read from and write to S3.

### 2.1 Create the bucket

1. Open the [Amazon S3 console](https://console.aws.amazon.com/s3/).
2. Choose **Create bucket**.
3. **Bucket name:** `aif-lab02-<your-initials>-<random-digits>` — bucket names are globally
   unique, so add something distinctive.
4. **AWS Region:** US East (N. Virginia) `us-east-1`. The bucket must be in the same Region
   as the Ground Truth job you create later.
5. Leave **Block all public access** enabled. Training data should never be public.
6. Leave default encryption at its default setting (server-side encryption is applied
   automatically) and choose **Create bucket**.

### 2.2 Create a prefix structure

Open the bucket and use **Create folder** to make these prefixes. A clear layout matters
more than it looks — Ground Truth writes output back into the same bucket, and you do not
want it mixed with your inputs.

```
tabular/
timeseries/
text/
images/
output/
```

> **Note:** S3 has no real folders. A "folder" is a key prefix — `images/photo1.jpg` is a
> single object whose name happens to contain a slash. The exam has been known to test this.

### 2.3 Create and upload sample files

On your own machine, create these two small files (any text editor will do).

`customers.csv` — tabular, structured:

```csv
customer_id,age,tenure_months,monthly_spend,region,churned
1001,34,18,82.50,APAC,0
1002,52,4,145.00,EMEA,1
1003,29,36,61.20,APAC,0
1004,41,9,210.75,AMER,1
1005,60,52,44.00,EMEA,0
```

`demand.csv` — time-series, structured:

```csv
timestamp,region,demand_mw
2026-01-01T00:00:00Z,APAC,4120
2026-01-01T01:00:00Z,APAC,3980
2026-01-01T02:00:00Z,APAC,3855
2026-01-01T03:00:00Z,APAC,3790
```

`reviews.txt` — unstructured text:

```text
The delivery was two days late but the packaging was excellent.
Battery life is far shorter than advertised. Disappointed.
Setup took five minutes and it has worked flawlessly since.
```

> **Teaching note:** these are illustrative sample records invented for this lab, not real
> customer or grid measurements. Never use production personal data in a training exercise.

Upload each file to its matching prefix using **Upload → Add files**.

### 2.4 Add images for the labelling job

You need a handful of images for Step 3. Use any 6–10 JPEG or PNG photos you own that fall
into two obvious visual categories — for example `cat` and `dog`, or `indoor` and
`outdoor`, or `damaged` and `undamaged`. Phone photos are fine. Keep them small
(under 1 MB each) so upload and labelling are quick.

Upload them all to the `images/` prefix.

> **Important:** do not upload photographs of identifiable people, or anything
> confidential. Ground Truth work team members will see every image you submit.

---

## Step 3 — Understand labelled versus unlabelled data

Of the files now in your bucket, only one is *ready* for supervised learning. Work out why.

### 3.1 The distinction

- **Labelled data** pairs each input with the correct answer — the **ground truth**.
  `customers.csv` is labelled: the `churned` column is the target. A supervised algorithm
  can learn the mapping from the other columns to that target.
- **Unlabelled data** has inputs only. Your `images/` prefix is unlabelled — S3 knows the
  file names, not what is in the pictures. `reviews.txt` is unlabelled too: there is no
  sentiment column.

Only labelled data can train a supervised model. Unlabelled data can still be used for
unsupervised learning (clustering, anomaly detection) or as pre-training material.

### 3.2 Why labelling is the bottleneck

Labelling is slow, expensive and where most data-quality problems originate:

- **Cost** — a human has to look at every example.
- **Consistency** — two annotators may disagree; ambiguous guidelines produce noisy labels.
- **Bias** — if annotators systematically mislabel one group, that bias is baked into the
  model. Lab 20 returns to this.
- **Class imbalance** — if 99% of examples are one class, accuracy becomes a misleading
  metric.

This is why AWS offers three ways to get labels, and why the exam expects you to choose
between them:

| Approach | When to use |
|---|---|
| **Ground Truth private workforce** | Confidential data, or labels that need domain expertise (medical, legal, internal defect codes) |
| **Ground Truth vendor workforce** | You need scale and a vetted supplier, and data sensitivity permits it |
| **Ground Truth public workforce (Amazon Mechanical Turk)** | Large volumes of non-confidential, general-knowledge labelling |

**Automated data labelling** (active learning) is an option within Ground Truth for large
jobs: a model is trained on the human-labelled examples and then labels the easy remainder,
sending only the uncertain ones to humans. It requires a substantial dataset to be
worthwhile, so this lab does not enable it.

### 3.3 Prepare a labelling plan

Write down, before touching the console:

1. **The label set** — the exact categories a worker may choose (e.g. `cat`, `dog`).
   Keep them mutually exclusive and exhaustive.
2. **The instruction** — one sentence a worker reads before labelling. Ambiguity here is
   the single biggest cause of inconsistent labels.
3. **The edge-case rule** — what should a worker do with an image containing both, or
   neither? Decide now, not halfway through.

You will type all three into the labelling job wizard in Step 4.

---

## Step 4 — Create a SageMaker Ground Truth labelling job

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

---

## Step 5 — Label the images and read the output manifest

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

---

## Step 6 — Clean up

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

---

## Verification

- [ ] You classified all five datasets in Step 1 and agree with the answer key
- [ ] An S3 bucket exists in `us-east-1` with `tabular/`, `timeseries/`, `text/`, `images/` and `output/` prefixes
- [ ] You can explain why `customers.csv` is labelled but `reviews.txt` is not
- [ ] A private work team was created and you received the labelling portal invitation
- [ ] The labelling job reached status **Completed** with every image labelled
- [ ] You opened `output.manifest` and can point to the label, the provenance flag and the confidence value in a record
- [ ] The S3 bucket has been emptied and deleted, and the work team removed

## Discussion questions

1. Your organisation must label 200,000 chest X-rays. Which Ground Truth workforce would you choose, and what would you need in place before any images leave your account?
2. Two annotators disagree on 15% of images in a labelling job. What would you change — the label set, the instructions, the workforce, or the task design — and how would you measure whether the change worked?
3. `reviews.txt` could be labelled by humans via Ground Truth or automatically by Amazon Comprehend. What are the trade-offs, and in what circumstances would the automated labels be unacceptable as training data?

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.
