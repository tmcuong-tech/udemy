# Domain 1 — Fundamentals of AI and ML (20%)

Part of the [AWS Certified AI Practitioner Training (AIF-C01) Learner Guide](../LEARNER%20GUIDE.md) · course code TGS-2024049338

---

## Lab 01 — AI, ML and Deep Learning Terminology

Build a precise vocabulary for AI, machine learning, deep learning and generative AI, and locate each concept in the AWS console.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 1 — Fundamentals of AI and ML (20%)
**Task statement:** 1.1 Explain basic AI concepts and terminologies
**WSQ mapping:** LU2 · Topic 4 Fundamentals of ML and AI · K4 · A2 · LO2
**Slide reference:** v11 deck slides 25–51
**Estimated time:** 30 minutes

**Learning objectives:**
- Define artificial intelligence, machine learning, deep learning and generative AI, and explain how they nest inside one another
- Classify a described workload as supervised, unsupervised or reinforcement learning, and name the common sub-types of each
- Use the terms algorithm, training, model, inference, parameter and hyperparameter precisely
- Describe what a neural network is in terms of layers, weights, biases and activation functions
- Select an appropriate inferencing option — real-time, batch, asynchronous or serverless — for a given scenario

---

### Step 1 — Survey the AWS AI and ML console landscape

Before defining terms, see where each idea lives in the AWS console. The console layout
itself teaches the hierarchy: AWS groups its AI/ML offerings into layers, and those layers
map almost exactly onto the vocabulary the exam tests.

### 1.1 Sign in

1. Sign in to the [AWS Management Console](https://console.aws.amazon.com/) with an IAM
   user or role that has read access. Everything in this lab is read-only or free.
2. In the Region selector (top right), choose **US East (N. Virginia) `us-east-1`**.
   AI/ML features appear in `us-east-1` first, so screenshots and menus in this course
   assume that Region.

### 1.2 Walk the three layers

Open each of the following from the console **Services** menu (or the search bar) in a new
browser tab. Do not create anything yet — just look at the landing page and read the
one-line description AWS gives the service.

| Layer | Open this | What the landing page tells you |
|---|---|---|
| Managed AI services | **Amazon Rekognition** | Pre-trained models exposed as an API. No training, no model artefacts. |
| ML platform | **Amazon SageMaker AI** | You bring data, choose an algorithm, train, and host a model yourself. |
| Generative AI | **Amazon Bedrock** | Foundation models accessed through a single API; you prompt rather than train. |

> **Note:** If a service page prompts you to enable something or create a domain, stop
> and close the tab. Step 1 is observation only.

### 1.3 Record what distinguishes the layers

In your notes, write one sentence for each layer answering: *who supplies the model, and
who supplies the data?*

- **Managed AI service** — AWS supplies the model, you supply only the input at inference time.
- **ML platform (SageMaker)** — you supply the data and choose the algorithm; AWS supplies
  the compute, the container and the hosting.
- **Generative AI (Bedrock)** — a third party (or AWS) supplies a large pre-trained
  foundation model; you supply prompts, and optionally your own data for customisation.

This "who supplies what" question is the fastest way to answer AIF-C01 scenario questions
that ask which AWS service fits a described workload.

---

### Step 2 — Map the AI, ML, deep learning and generative AI hierarchy

The exam repeatedly asks you to place a described technique in the right box. The four
terms are **nested**, not parallel — each is a subset of the one before it.

### 2.1 The nesting

```
Artificial Intelligence
└── Machine Learning
    └── Deep Learning
        └── Generative AI
```

- **Artificial intelligence (AI)** — any technique that lets a machine perform tasks that
  normally need human intelligence. This includes hand-written rule engines and search
  algorithms that do no learning at all.
- **Machine learning (ML)** — a subset of AI in which the system learns patterns from data
  instead of being explicitly programmed with rules.
- **Deep learning (DL)** — a subset of ML that uses neural networks with many hidden
  layers. It excels where features are hard to hand-engineer: images, audio, raw text.
- **Generative AI** — a subset of deep learning whose models *produce new content*
  (text, image, audio, code) rather than only producing a label or a number.

### 2.2 Classify these workloads

Write **AI only**, **ML**, **DL** or **GenAI** against each row. Choose the *narrowest*
box that fits.

| # | Workload | Your answer |
|---|---|---|
| 1 | A tax form validator built from 400 hand-written `if` rules | |
| 2 | A linear regression that predicts house price from floor area | |
| 3 | A convolutional network that flags manufacturing defects in photos | |
| 4 | A model that writes a product description from five bullet points | |
| 5 | A decision tree that scores loan applications from tabular data | |
| 6 | A model that produces a photo-realistic image from a text prompt | |

**Answer key:** 1 = AI only (no learning from data) · 2 = ML · 3 = DL · 4 = GenAI ·
5 = ML · 6 = GenAI.

### 2.3 Check the boundary cases

Two distinctions catch people out on the exam:

- **Rule engines are AI but not ML.** If a human wrote the rules, nothing was learned.
- **All generative AI is deep learning, but most deep learning is not generative.** An
  image classifier is deep learning; it outputs a label, not new content.

---

### Step 3 — Distinguish supervised, unsupervised and reinforcement learning

The three learning paradigms differ in **what feedback the model receives during
training**. Get that one idea right and the rest follows.

### 3.1 The three paradigms

| Paradigm | Training data | Feedback signal | Typical output |
|---|---|---|---|
| Supervised | Labelled — every example carries the correct answer | The known label | Classification or regression |
| Unsupervised | Unlabelled — inputs only | None; the algorithm finds structure | Clusters, reduced dimensions, anomaly scores |
| Reinforcement | No fixed dataset; an agent acts in an environment | A reward after each action | A policy — what to do in each state |

### 3.2 Sub-types you should be able to name

- **Supervised → classification** predicts a category (spam / not spam). **Binary**
  classification has two classes; **multi-class** has more than two.
- **Supervised → regression** predicts a continuous number (tomorrow's demand).
- **Unsupervised → clustering** groups similar records (customer segments).
- **Unsupervised → dimensionality reduction** compresses many features into few (PCA).
- **Unsupervised → anomaly detection** flags records unlike the rest (fraud screening).
- **Semi-supervised** learning uses a small labelled set plus a large unlabelled set —
  common when labelling is expensive, which is exactly the problem Lab 02 addresses.

### 3.3 Confirm against SageMaker's built-in algorithms

1. Open the **Amazon SageMaker AI** console.
2. In the left navigation, choose **JumpStart** (under Studio or the getting-started
   section, depending on your console version), then browse the model and solution
   listings. If JumpStart is unavailable in your account, use the SageMaker developer
   documentation's built-in algorithms page instead.
3. Find at least one algorithm in each of these families and note the paradigm it belongs to:

| Built-in algorithm | Paradigm | Task |
|---|---|---|
| XGBoost | Supervised | Classification or regression on tabular data |
| Linear Learner | Supervised | Classification or regression |
| K-Means | Unsupervised | Clustering |
| Principal Component Analysis (PCA) | Unsupervised | Dimensionality reduction |
| Random Cut Forest | Unsupervised | Anomaly detection |

> **Teaching note:** the table above is a study aid, not a live listing. AWS adds and
> retires built-in algorithms over time — always confirm current availability in the
> SageMaker console for your Region.

### 3.4 Where RLHF fits

**Reinforcement learning from human feedback (RLHF)** is how many foundation models are
aligned to human preference: humans rank model outputs, a reward model is trained on
those rankings, and reinforcement learning then tunes the model against that reward.
It is worth remembering as the one place reinforcement learning appears prominently in
the generative AI part of the exam.

---

### Step 4 — Separate algorithm, model, training and inference

These four words are used loosely in conversation and precisely on the exam.

### 4.1 Definitions

- **Algorithm** — the *procedure* for learning. XGBoost, K-Means and a neural network
  architecture are algorithms. An algorithm on its own has learned nothing.
- **Training** — running the algorithm over a dataset so that it adjusts internal
  parameters (in a neural network, the **weights** and **biases**) to reduce error.
- **Model** — the *artefact produced by training*: the learned parameters plus enough
  structure to reproduce the computation. In SageMaker this is a `model.tar.gz` file in
  Amazon S3, registered as a SageMaker **model** object.
- **Inference** — using a trained model to produce an output for new, unseen input. Also
  called prediction or scoring.

A one-line summary worth memorising: **algorithm + data → training → model → inference → prediction.**

### 4.2 Neural network vocabulary

A neural network is layers of connected **neurons** (nodes):

- **Input layer** takes the features.
- **Hidden layers** transform them. "Deep" simply means more than one hidden layer.
- **Output layer** produces the prediction.
- **Weights and biases** are the learned parameters adjusted during training.
- **Activation function** introduces non-linearity, letting the network model curves and
  interactions a linear model cannot.
- An **epoch** is one full pass over the training data.

Distinguish **parameters** (learned by training — weights and biases) from
**hyperparameters** (set *before* training — learning rate, number of layers, batch size).
The exam tests this pair often, and Lab 05 revisits hyperparameter tuning.

### 4.3 See the artefacts in the console

1. Open the **Amazon SageMaker AI** console.
2. In the left navigation, expand the training section and choose **Training jobs**. This
   is where *training* runs are recorded — each has an input data location, an algorithm
   or container image, hyperparameters, and an output S3 path.
3. In the left navigation, find **Models** (under the inference section). This is the
   registry of trained *model* artefacts that can be deployed.
4. Still under inference, open **Endpoints**. An endpoint is where *inference* happens.

If your account is new all three lists will be empty. That is expected — the point is to
see that AWS gives training, models and inference three separate console pages, because
they are three separate stages with separate costs and separate lifecycles. Lab 04 fills
all three lists in.

---

### Step 5 — Compare inferencing options: real-time versus batch

Once a model exists, *how* you run inference is a design decision with direct cost and
latency consequences. AIF-C01 expects you to pick the right option from a scenario.

### 5.1 The options

| Option | Latency | Input | Infrastructure | Bills |
|---|---|---|---|---|
| **Real-time endpoint** | Milliseconds | One request at a time | Always-on instances | Continuously, while the endpoint exists |
| **Batch transform** | Minutes to hours | A whole dataset in S3 | Spun up for the job, then torn down | Only for the job's duration |
| **Asynchronous inference** | Seconds to minutes | Large payloads, queued | Can scale to zero when idle | Only while processing (plus storage) |
| **Serverless inference** | Milliseconds, plus cold start | One request at a time | Managed, no instance to choose | Per request and duration |

### 5.2 Choosing between them

Ask two questions:

1. **Does a user or system wait for the answer?** If yes, you need real-time (or
   serverless) inference. A fraud check during checkout cannot wait.
2. **Do you have all the inputs already?** If yes, and nobody is waiting, batch transform
   is cheaper because nothing runs between jobs. Scoring last night's transactions,
   generating monthly churn scores, or captioning an archive of images are batch jobs.

Serverless inference is the middle ground for **intermittent, spiky traffic** where an
always-on endpoint would idle expensively and an occasional cold start is acceptable.
Asynchronous inference suits **large payloads or long processing times** — a several-minute
video, for example — where a synchronous HTTP request would time out.

### 5.3 Match the scenario

| Scenario | Best option |
|---|---|
| Recommend products as a shopper browses | |
| Score 40 million customer records once a month | |
| Caption uploaded 1 GB videos; results emailed when ready | |
| An internal tool used by 12 staff a few times a day | |

**Answer key:** real-time endpoint · batch transform · asynchronous inference ·
serverless inference.

### 5.4 Confirm in the console

1. In the **Amazon SageMaker AI** console left navigation, open **Batch transform jobs**
   (under the inference section) and note that a job has a *start* and an *end* — it is not
   a standing resource.
2. Open **Endpoints** again and note that an endpoint has a *status* of **InService** — it
   stands there until you delete it. That difference is exactly why Lab 04 carries a cost
   warning and this lab does not.

---

### Step 6 — Clean up

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

---

### Verification

- [ ] You can name the three layers of the AWS AI/ML stack and say who supplies the model in each
- [ ] You classified all six workloads in Step 2 and agree with the answer key
- [ ] You can state the feedback signal that defines supervised, unsupervised and reinforcement learning
- [ ] You can explain the difference between a parameter and a hyperparameter
- [ ] You located Training jobs, Models and Endpoints as three separate pages in the SageMaker console
- [ ] You matched all four scenarios in Step 5 to an inferencing option
- [ ] No SageMaker notebook instance, Studio application, Canvas session or endpoint is running in your account

### Discussion questions

1. A colleague describes their spam filter as "AI". What follow-up questions would you ask to decide whether it is a rule engine, classical machine learning, or deep learning — and why does the answer change how the system is maintained?
2. A team wants product recommendations refreshed nightly for 20 million customers, and also shown live as a shopper browses. Which inferencing options would you use for each requirement, and why is using one option for both a poor design?
3. Labelling data is the expensive part of supervised learning. Given that, why would an organisation still choose supervised learning over unsupervised learning for a fraud-detection problem?

---

---

## Lab 02 — Data Types and Labelling for ML

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

### Step 1 — Classify structured, semi-structured and unstructured data

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

### Step 2 — Create an S3 bucket and organise a dataset

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

### Step 3 — Understand labelled versus unlabelled data

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

### Step 4 — Create a SageMaker Ground Truth labelling job

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

### Step 5 — Label the images and read the output manifest

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

### Step 6 — Clean up

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

### Verification

- [ ] You classified all five datasets in Step 1 and agree with the answer key
- [ ] An S3 bucket exists in `us-east-1` with `tabular/`, `timeseries/`, `text/`, `images/` and `output/` prefixes
- [ ] You can explain why `customers.csv` is labelled but `reviews.txt` is not
- [ ] A private work team was created and you received the labelling portal invitation
- [ ] The labelling job reached status **Completed** with every image labelled
- [ ] You opened `output.manifest` and can point to the label, the provenance flag and the confidence value in a record
- [ ] The S3 bucket has been emptied and deleted, and the work team removed

### Discussion questions

1. Your organisation must label 200,000 chest X-rays. Which Ground Truth workforce would you choose, and what would you need in place before any images leave your account?
2. Two annotators disagree on 15% of images in a labelling job. What would you change — the label set, the instructions, the workforce, or the task design — and how would you measure whether the change worked?
3. `reviews.txt` could be labelled by humans via Ground Truth or automatically by Amazon Comprehend. What are the trade-offs, and in what circumstances would the automated labels be unacceptable as training data?

---

---

## Lab 03 — AWS Managed AI Services Tour

Use Amazon Comprehend, Translate, Polly, Transcribe and Rekognition from the console, and learn to match each managed AI service to a business use case.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 1 — Fundamentals of AI and ML (20%)
**Task statement:** 1.2 Identify practical use cases for AI
**WSQ mapping:** LU3 · Topic 5 Exploring AI Use Cases · K7 · A3 · LO3
**Slide reference:** v11 deck slides 52–83
**Estimated time:** 40 minutes

**Learning objectives:**
- Use Amazon Comprehend to extract sentiment, entities, key phrases, language and PII from free text
- Perform neural machine translation with Amazon Translate and describe how custom terminology controls brand terms
- Synthesise speech with Amazon Polly and control pronunciation and pacing with SSML
- Create an Amazon Transcribe job and evaluate the transcript against known ground truth
- Detect labels, moderate content and read text in images with Amazon Rekognition, and distinguish it from Amazon Textract
- Select the correct AWS AI service for a described business requirement

---

### Step 1 — Extract meaning from text with Amazon Comprehend

Amazon Comprehend is a managed **natural language processing** service. You send text, it
returns sentiment, entities, key phrases, language and PII — with no model to train and no
infrastructure to run.

> **Cost note:** every service in this lab bills per unit of input processed (characters,
> characters translated, seconds of audio, images analysed). The volumes here are tiny, and
> several of these services include a free tier for new accounts. Nothing you create in
> Steps 1–5 runs continuously; Step 7 removes the one storage resource you make.

### 1.1 Open real-time analysis

1. Open the [Amazon Comprehend console](https://console.aws.amazon.com/comprehend/) in
   `us-east-1`.
2. In the left navigation, choose **Real-time analysis**.
3. Leave the analysis type set to the built-in option (rather than a custom model).

### 1.2 Analyse a sample

1. Clear the sample text and paste this in the input box:

```text
I ordered the AeroTrack X2 from Contoso Retail in Singapore on 14 March. Delivery was
three days late and the courier left it in the rain, so the box was soaked. Support did
answer within an hour and shipped a replacement, which arrived perfectly. Call me on
+65 6555 0100 if you need the order number.
```

2. Choose **Analyze**.

### 1.3 Read each output tab

Work through the result tabs and note what each one gives you:

| Tab | What it returns | Why it matters |
|---|---|---|
| **Sentiment** | One of `POSITIVE`, `NEGATIVE`, `NEUTRAL`, `MIXED`, with confidence scores | Note that this text should score **MIXED** — a late, damaged delivery but good support. A single overall label hides that nuance. |
| **Entities** | Detected entities with types such as `ORGANIZATION`, `LOCATION`, `DATE`, `COMMERCIAL_ITEM`, `QUANTITY` | This is how you turn free text into structured fields. |
| **Key phrases** | The noun phrases that carry the content | Useful for tagging and search. |
| **Language** | Detected dominant language with a confidence score | Feeds the translation step that follows. |
| **PII** | Detected personally identifiable information and its offsets | It should flag the phone number. This is the feature you use for redaction. |
| **Targeted sentiment** | Sentiment attached to each specific entity | Shows negative sentiment towards delivery and positive towards support — the nuance the overall label lost. |

### 1.4 Note the confidence scores

Every result carries a **confidence score** between 0 and 1. Managed AI services are
probabilistic, not deterministic. Two consequences the exam expects you to know:

- You should set a **confidence threshold** appropriate to the risk of being wrong, and
  route low-confidence results to a human.
- Confidence is **not** accuracy. A high-confidence wrong answer is entirely possible.

### 1.5 Note what Comprehend does not do

Comprehend classifies and extracts. It does not *generate* text. If the requirement is
"summarise these reviews in a paragraph" or "draft a reply", that is a generative AI job
for Amazon Bedrock (Domain 2), not Comprehend. Choosing between an analytical managed
service and a foundation model is a recurring exam theme.

> **Optional:** Comprehend also supports **custom classification** and **custom entity
> recognition**, where you supply labelled examples and it trains a model for you. Those
> create asynchronous training jobs and take longer than this lab allows — look at the
> **Custom classification** page in the left navigation to see where they live, but do not
> start a job.

---

### Step 2 — Translate text with Amazon Translate

Amazon Translate is managed **neural machine translation**. It pairs naturally with
Comprehend: detect the language, then translate it.

### 2.1 Run a real-time translation

1. Open the [Amazon Translate console](https://console.aws.amazon.com/translate/) in
   `us-east-1`.
2. In the left navigation, choose **Real-time translation**.
3. Set **Source language** to **Auto (auto)** — Translate will call language detection for
   you, the same capability you saw in Comprehend.
4. Set **Target language** to a language you can sanity-check, or to **Chinese (Simplified)**.
5. Paste the review text from Step 1.2 into the source box.

The translation appears as you type. Note the detected source language shown next to the
**Auto** setting.

### 2.2 Translate back and inspect the loss

1. Copy the translated output.
2. Swap the languages: set the source to your target language and the target back to
   **English**.
3. Paste the translation in and compare the round-trip result with your original.

Round-tripping is a quick, informal quality check. Product names, idioms and units are
where meaning drifts. Two things follow:

- Machine translation output should be **reviewed by a human when the stakes are high** —
  legal, medical or safety-critical text.
- Named entities such as `AeroTrack X2` and `Contoso Retail` should usually be left
  untranslated.

### 2.3 See how you would control brand terms

You cannot fix brand-name translations by prompting — Translate has no prompt. Instead it
offers two customisation features. Open each page in the left navigation and read the
description; do not create anything.

| Feature | What it does | Use when |
|---|---|---|
| **Custom terminology** | A CSV of source-to-target term pairs that Translate applies verbatim | Brand names, product names, internal jargon |
| **Parallel data / Active Custom Translation** | Example translated sentence pairs that adapt output style and domain | Domain-specific tone, e.g. legal or medical register |

### 2.4 Note the batch option

**Real-time translation** handles one piece of text at a time. For a folder of documents,
the **Batch translation** page runs an asynchronous job that reads from one S3 prefix and
writes to another — the same real-time-versus-batch trade-off you met in Lab 01. Look at
the page, but do not start a job; batch jobs take longer than this lab allows.

---

### Step 3 — Synthesise speech with Amazon Polly

Amazon Polly is managed **text-to-speech (TTS)**. It turns written text into lifelike
spoken audio.

### 3.1 Create an S3 bucket for this lab

You will need somewhere to keep the audio file for Step 4.

1. Open the [Amazon S3 console](https://console.aws.amazon.com/s3/) and choose
   **Create bucket**.
2. **Bucket name:** `aif-lab03-<your-initials>-<random-digits>`.
3. **Region:** `us-east-1`. Leave **Block all public access** enabled.
4. Choose **Create bucket**.

### 3.2 Synthesise speech

1. Open the [Amazon Polly console](https://console.aws.amazon.com/polly/) in `us-east-1`.
2. In the left navigation, choose the text-to-speech page.
3. Paste this text — write it exactly, because you will check whether Transcribe recovers
   it in Step 4:

```text
Good morning. This is a test recording for the AWS Certified AI Practitioner course.
Our quarterly revenue increased by fourteen percent, and customer satisfaction reached
ninety two points.
```

4. Choose an **engine**. The console lists the engines available to your account and
   Region — the neural and newer engines generally sound more natural than the standard
   engine, and voice availability differs per engine.
5. Choose a **language** and a **voice**.
6. Choose **Listen** to preview the audio.

### 3.3 Compare voices and engines

1. Re-synthesise the same text with a different engine or voice and listen again.
2. Note where the two differ: prosody, pauses, and how each handles "ninety two points".

Voice choice is a real product decision — the exam frames Polly use cases as accessibility,
IVR/contact-centre prompts, e-learning narration, and reading long-form content aloud.

### 3.4 Control pronunciation with SSML

1. Switch the input mode from plain text to **SSML**.
2. Try this, which wraps the text in the required `speak` element and inserts a pause:

```xml
<speak>
  Good morning. This is a test recording.
  <break time="1s"/>
  Our quarterly revenue increased by <prosody rate="slow">fourteen percent</prosody>.
</speak>
```

3. Choose **Listen** and note the inserted pause and the slowed phrase.

**Speech Synthesis Markup Language (SSML)** is how you control pauses, emphasis, speaking
rate and pronunciation. **Lexicons** (in the left navigation) go further, mapping specific
words — an acronym, a brand name — to a fixed pronunciation across all your text.

### 3.5 Save the audio

1. Switch back to plain text mode and restore the Step 3.2 text.
2. Use the download option to save the synthesised audio as an MP3 to your machine.
3. In the S3 console, upload that MP3 into your `aif-lab03-...` bucket.

> **Note:** Polly can also write directly to S3 from the console using an asynchronous
> synthesis task, which is the right choice for long documents. Downloading and uploading
> is simpler for a single short clip.

You now have a **real audio file with known ground-truth text** — exactly what you need to
evaluate a speech-to-text service.

---

### Step 4 — Convert speech to text with Amazon Transcribe

Amazon Transcribe is managed **automatic speech recognition (ASR)** — the inverse of Polly.
You will transcribe the audio you just generated and compare the result with the text you
typed.

### 4.1 Create a transcription job

1. Open the [Amazon Transcribe console](https://console.aws.amazon.com/transcribe/) in
   `us-east-1`.
2. In the left navigation, under the transcription section, choose **Transcription jobs**,
   then **Create job**.
3. **Name:** `aif-lab03-transcribe`.
4. **Language settings:** choose **Specific language** and select the language you used in
   Polly. (**Automatic language identification** is the alternative when you do not know
   the language in advance.)
5. **Input data — S3 location:** browse to the MP3 you uploaded in Step 3.5.
6. **Output data:** choose the service-managed S3 bucket, or your own bucket if you prefer
   to keep the JSON.
7. Choose **Next**.

### 4.2 Review the configuration options

On the configure page, note these without enabling most of them:

| Option | What it does | When you would use it |
|---|---|---|
| **Speaker diarization / partitioning** | Labels which speaker said what | Meetings, interviews, contact-centre calls |
| **Custom vocabulary** | A list of domain words and their pronunciations | Drug names, part numbers, internal jargon |
| **Custom language model** | Trained on your own domain text | Heavily domain-specific speech, at scale |
| **Vocabulary filtering** | Masks or removes unwanted words | Redaction, profanity filtering |
| **PII redaction** | Detects and masks personal data in the transcript | Contact-centre recordings under privacy rules |
| **Automatic language identification** | Detects the spoken language | Multilingual inbound audio |

Turn on **PII redaction** if the option is available for your language, then choose
**Create job**.

### 4.3 Read the transcript

1. The job appears with status **In progress**, then **Complete** — usually within a
   minute for a short clip. Refresh the list.
2. Select the job name to open it and read the transcript preview.
3. Compare it word by word with the text you typed into Polly in Step 3.2.

Answer these:

- Did it recover "fourteen percent" and "ninety two points" as words, or convert them to
  digits?
- Are the sentence boundaries and punctuation right?
- Is anything wrong, and would that error matter in a real transcript?

**Word error rate (WER)** is the standard ASR metric — the proportion of words inserted,
deleted or substituted relative to the reference. You have just done a one-sample WER
evaluation by hand.

### 4.4 Inspect the JSON output

If you sent output to your own bucket, open the resulting `.json` file in S3. It contains
the full transcript plus per-word items with **start time**, **end time** and a
**confidence** score. That per-word timing is what makes captioning, search-within-audio
and call analytics possible — and it is another reminder that these services return
probabilities, not certainties.

### 4.5 Note the streaming option

Transcription jobs are **batch**: audio in S3, transcript out when finished. Transcribe
also offers **streaming transcription** over a live audio stream for real-time captions
and live agent assist. The **Real-time transcription** page in the left navigation
demonstrates this with your microphone — try it if your browser permits, then stop it. It
is the same batch-versus-real-time trade-off from Lab 01, applied to speech.

---

### Step 5 — Analyse images with Amazon Rekognition

Amazon Rekognition is managed **computer vision**. It detects objects, scenes, text, faces
and unsafe content in images and video.

### 5.1 Detect labels

1. Open the [Amazon Rekognition console](https://console.aws.amazon.com/rekognition/) in
   `us-east-1`.
2. In the left navigation, choose **Label detection** (it may sit under a demos or
   analysis grouping).
3. The page loads with a sample image. Choose **Upload** and select one of the photos you
   used in Lab 02 — or use the provided sample.
4. Read the **Results** panel.

Note three things:

- Each label carries a **confidence score**, just like Comprehend's sentiment.
- Labels are **hierarchical** — `Dog` typically comes with parent categories such as
  `Animal` and `Pet`.
- **Bounding boxes** appear for objects Rekognition can localise, so you get *where* as
  well as *what*.

Expand the **Response** or JSON view to see the raw API response. That structure —
`Labels[].Name`, `Confidence`, `Instances[].BoundingBox` — is what your application code
would parse.

### 5.2 Try the other capabilities

Work through these pages in the left navigation, using the supplied sample images. Each
takes under a minute.

| Page | What it returns | Representative use case |
|---|---|---|
| **Image moderation** | Moderation labels with confidence, in a category hierarchy | Screening user-uploaded content before publication |
| **Facial analysis** | Attributes of a detected face — pose, eyes open, apparent emotion | Photo tooling, engagement analytics |
| **Face comparison** | A similarity score between two faces | Identity verification against a reference photo |
| **Text in image** | Detected text with bounding boxes | Reading signs, plates, screenshots |
| **PPE detection** | Whether people are wearing head, face and hand cover | Worksite safety compliance |

### 5.3 Draw the boundary against other services

This is exactly the discrimination the exam tests:

- **Rekognition** finds objects, scenes, faces and unsafe content in **photos and video**.
- **Amazon Textract** extracts **structured text** from documents — forms, tables, key-value
  pairs from an invoice or a form. If the requirement mentions a *document*, a *form* or a
  *table*, the answer is Textract, not Rekognition's text detection.
- **Amazon Rekognition Custom Labels** trains on your own labelled images when the
  built-in labels do not cover your domain — a specific defect type, or your own product
  SKUs. That is where the augmented manifest from Lab 02 would be used.

### 5.4 Consider the responsible-AI dimension

Facial analysis and face comparison are the most sensitive features in this lab. Before
using them in production you would need to consider consent, applicable biometric
regulation, demonstrated accuracy across demographic groups, and a confidence threshold
with human review for consequential decisions. Domain 4 (Labs 19–22) covers this in depth
— note the concern here and carry it forward.

---

### Step 6 — Match services to use cases

You have now used five managed AI services. The exam rarely asks what a service *is* — it
describes a business requirement and asks which service meets it. This step builds the
lookup table you need.

### 6.1 The AWS managed AI service map

| Service | Modality | Core capability |
|---|---|---|
| **Amazon Comprehend** | Text | Sentiment, entities, key phrases, language, PII, topic modelling |
| **Amazon Translate** | Text | Neural machine translation between languages |
| **Amazon Polly** | Text → audio | Text-to-speech synthesis |
| **Amazon Transcribe** | Audio → text | Speech-to-text, batch and streaming |
| **Amazon Rekognition** | Image, video | Objects, scenes, faces, moderation, text in images |
| **Amazon Textract** | Document image → structured text | Forms, tables, key-value extraction |
| **Amazon Lex** | Text, voice | Conversational bot — intents, slots, dialogue |
| **Amazon Kendra** | Documents | Intelligent enterprise search over your content |
| **Amazon Personalize** | User-item interactions | Recommendations and personalised ranking |
| **Amazon Fraud Detector** | Tabular events | Online fraud risk scoring |

> **Teaching note:** this table lists capabilities, not availability. Confirm service and
> feature availability for your own Region in the console before designing a solution.

### 6.2 Match the requirement

For each requirement, name the service. Some need more than one.

| # | Requirement | Service(s) |
|---|---|---|
| 1 | Publish a news article as an audio version for visually impaired readers | |
| 2 | Automatically pull the invoice number and total from scanned supplier PDFs | |
| 3 | Flag user-uploaded photos containing unsafe content before they go live | |
| 4 | Route inbound support emails by topic and urgency | |
| 5 | Produce searchable, speaker-attributed transcripts of recorded sales calls | |
| 6 | Show a Japanese customer your English product catalogue in Japanese | |
| 7 | Recommend the next product to each shopper based on browsing history | |
| 8 | Let staff ask questions in plain English across an internal document store | |
| 9 | Build a voice bot that books appointments | |
| 10 | Caption a live webinar in real time | |

**Answer key:** 1 Polly · 2 Textract · 3 Rekognition (image moderation) · 4 Comprehend
(sentiment plus custom classification) · 5 Transcribe with speaker partitioning ·
6 Translate · 7 Personalize · 8 Kendra · 9 Lex (with Polly and Transcribe underneath) ·
10 Transcribe streaming.

### 6.3 The decision rule for the exam

Work through these questions in order:

1. **Is there a managed AI service for this exact task?** If yes, choose it. It needs no
   training data, no infrastructure and no ML expertise.
2. **Does it need to generate new content, reason over a prompt, or hold a conversation?**
   Then it is a foundation model on **Amazon Bedrock** (Domain 2).
3. **Is the task specific to your own data and unlike anything pre-trained?** Then it is a
   custom model on **SageMaker** (Lab 04), or a customisation feature such as Comprehend
   custom classification or Rekognition Custom Labels.

Choosing SageMaker when a managed service would do is the classic wrong answer: it adds
training data requirements, ML expertise and undifferentiated operational effort for no
benefit.

### 6.4 The shared characteristics

Every service in this lab shares four traits worth stating explicitly, because they turn
up as distractors:

- **Pre-trained** — you supply no training data to use the base capability.
- **API-driven and serverless to you** — no instances to size, no endpoints to keep alive.
- **Pay per unit processed** — characters, seconds of audio, images. No idle cost.
- **Probabilistic** — every result has a confidence score, and every design needs a
  threshold and a human-review path for low-confidence or high-stakes cases.

---

### Step 7 — Clean up

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

---

### Verification

- [ ] Comprehend returned a MIXED sentiment for the sample review and flagged the phone number as PII
- [ ] You round-tripped the review through Amazon Translate and identified at least one point where meaning drifted
- [ ] Polly produced audible speech, and the SSML sample inserted an audible pause
- [ ] An MP3 of the Step 3.2 text exists in your lab S3 bucket
- [ ] The Transcribe job reached status **Complete** and you compared its transcript with the original text
- [ ] Rekognition returned labels with confidence scores and at least one bounding box
- [ ] You completed the ten-row matching table in Step 6.2
- [ ] The S3 bucket is deleted, the transcription job removed, and no Comprehend endpoint or Rekognition Custom Labels model is running

### Discussion questions

1. Comprehend scored the sample review as MIXED overall while targeted sentiment showed negative delivery and positive support. If you were building a review dashboard, which output would you use, and what would you lose either way?
2. A contact centre wants to transcribe every call and analyse sentiment. Sketch the service chain, and identify every point where personal data appears and what control you would apply there.
3. A team proposes training a custom SageMaker image classifier to detect whether uploaded photos contain unsafe content. Argue against it using what you saw in Step 5, then describe the one circumstance in which they would be right.

---

---

## Lab 04 — Train and Deploy a Model with SageMaker

Train a binary classifier with the SageMaker built-in XGBoost algorithm, deploy it to a real-time endpoint, evaluate it, and delete every billing resource.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 1 — Fundamentals of AI and ML (20%)
**Task statement:** 1.3 Describe the ML development lifecycle
**WSQ mapping:** LU4 · Topic 7 Developing ML Solutions · K3 · A4 · LO4
**Slide reference:** v11 deck slides 84–135
**Estimated time:** 45 minutes

> **⚠️ COST WARNING:** this lab creates a SageMaker notebook instance and a real-time
> inference endpoint. **Both bill continuously until deleted, whether you use them or not.**
> Step 7 removes everything — do not skip it. If you must stop part-way through, go
> straight to Step 7.

**Learning objectives:**
- Explain the SageMaker cost model and identify which resources bill continuously versus per job
- Create a notebook instance and describe the role of the SageMaker execution role
- Prepare tabular data into train, validation and test splits in the format a built-in algorithm requires
- Run a training job with the built-in XGBoost algorithm and interpret its console record
- Deploy a model as a real-time endpoint and explain the model, endpoint configuration and endpoint objects
- Evaluate a classifier using accuracy, precision, recall, F1 and AUC, and explain how the decision threshold trades precision against recall
- Delete every chargeable resource and verify the account is clean

---

### Step 1 — Read the cost warning and plan the run

> ## ⚠️ COST WARNING — READ BEFORE YOU START
>
> **This is the first lab in the course that creates resources which bill continuously.**
>
> | Resource | Bills | Stops billing when |
> |---|---|---|
> | SageMaker **notebook instance** | Per hour, whenever the status is `InService` | You **stop** or **delete** it |
> | SageMaker **Studio application** (JupyterLab, Code Editor, Canvas) | Per hour, whenever it is running | You **delete the app** — closing the browser tab does nothing |
> | SageMaker **real-time endpoint** | Per hour, continuously, **even with zero requests** | You **delete the endpoint** |
> | SageMaker **training job** | Only for the seconds the job runs | Automatically, when the job finishes |
> | Amazon **S3** objects | Per GB-month stored | You delete the objects |
>
> An endpoint left running is the single most common source of unexpected AWS bills for
> people learning SageMaker. **Do not skip Step 7.** If you have to abandon the lab
> part-way through, jump straight to Step 7 and delete everything.
>
> Confirm current instance pricing on the AWS SageMaker pricing page for your Region before
> you start, and check whether your account still has AWS Free Tier coverage.

### 1.1 What you will build

You will run the full lifecycle you defined in Lab 01, end to end:

```
data in S3  →  training job  →  model artefact  →  endpoint  →  prediction
```

The task is **binary classification** on a small tabular dataset, using the SageMaker
**built-in XGBoost algorithm**. XGBoost is the standard first choice for tabular data and
appears constantly in AIF-C01 scenarios.

### 1.2 Prerequisites

- An AWS account with permission to create SageMaker, IAM and S3 resources.
- Region **US East (N. Virginia) `us-east-1`** selected in the console.
- About 45 minutes of uninterrupted time — the notebook instance bills the whole time it
  is running, so do not start and walk away.

### 1.3 Set a billing guard (recommended)

1. Open the **Billing and Cost Management** console.
2. Under **Budgets**, create a small monthly cost budget — for example 5 USD — with an
   email alert at 80%.

This will not stop anything running, but it is the cheapest insurance available and takes
two minutes. Cost awareness is itself an exam topic.

### 1.4 Note the instance types you will use

| Purpose | Instance type used in this lab |
|---|---|
| Notebook instance | `ml.t3.medium` — the smallest generally suitable notebook size |
| Training job | `ml.m5.large` |
| Inference endpoint | `ml.m5.large` |

If a chosen type is unavailable or your account quota does not permit it, the console will
say so; choose the next smallest type it offers rather than a larger one.

---

### Step 2 — Create a SageMaker notebook instance

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

---

### Step 3 — Prepare the dataset and upload it to S3

SageMaker training jobs read from Amazon S3. This step produces the exact format the
built-in XGBoost algorithm expects and puts it there.

### 3.1 Load and inspect the data

In a new cell:

```python
import pandas as pd
from sklearn.datasets import load_breast_cancer

data = load_breast_cancer(as_frame=True)
df = data.frame

print(df.shape)
print(df["target"].value_counts())
df.head()
```

This is a small, well-known binary classification dataset bundled with scikit-learn: 30
numeric features per record and a 0/1 target. It stands in for any tabular business
problem — churn, default, defect.

Note the **class balance** printed above. A roughly balanced dataset means accuracy is a
reasonable headline metric; a heavily imbalanced one would not be. Lab 05 returns to this.

### 3.2 Put the target in the first column

The built-in XGBoost algorithm has a strict CSV contract:

- **The target must be the first column.**
- **No header row.**
- **No index column.**
- Numeric values only.

```python
cols = ["target"] + [c for c in df.columns if c != "target"]
df = df[cols]
df.head()
```

Getting this wrong is the most common cause of a failed XGBoost training job — the
algorithm will happily train on your target as if it were a feature and produce nonsense.

### 3.3 Split into train, validation and test

```python
from sklearn.model_selection import train_test_split

train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df["target"])
train_df, val_df = train_test_split(train_df, test_size=0.2, random_state=42, stratify=train_df["target"])

print("train:", train_df.shape, "validation:", val_df.shape, "test:", test_df.shape)
```

Three splits, three distinct jobs:

| Split | Used for | Seen by the algorithm? |
|---|---|---|
| **Training** | Fitting the model parameters | Yes, directly |
| **Validation** | Watching for overfitting during training and tuning hyperparameters | Yes, but only to score, not to fit |
| **Test** | A final honest estimate of performance | **No** — held back until the very end |

`stratify` keeps the class proportions the same in every split. Without it, a small split
can end up with a badly skewed class mix.

### 3.4 Write the CSVs and upload

```python
train_df.to_csv("train.csv", index=False, header=False)
val_df.to_csv("validation.csv", index=False, header=False)

prefix = "aif-lab04-xgboost"

train_uri = sess.upload_data("train.csv", bucket=bucket, key_prefix=f"{prefix}/train")
val_uri   = sess.upload_data("validation.csv", bucket=bucket, key_prefix=f"{prefix}/validation")

print(train_uri)
print(val_uri)
```

`index=False, header=False` is what satisfies the contract from 3.2 — check both flags.

### 3.5 Confirm in the S3 console

Open the [Amazon S3 console](https://console.aws.amazon.com/s3/), find the
`sagemaker-...` default bucket, and browse to `aif-lab04-xgboost/`. You should see the
`train/` and `validation/` prefixes with one CSV each.

You have now completed the *data* half of the pipeline. Keep `test_df` in memory in the
notebook — you will use it against the endpoint in Step 6.

---

### Step 4 — Train a model with the built-in XGBoost algorithm

Now run the training job. This is where the algorithm meets the data and produces a model
artefact.

> **Cost note:** a training job bills only for the seconds it runs, then the instance is
> torn down automatically. This job should take a few minutes. Training is *not* the
> expensive part of this lab — the endpoint in Step 6 is.

### 4.1 Get the algorithm container

```python
from sagemaker.image_uris import retrieve

container = retrieve(framework="xgboost", region=region, version="1.7-1")
print(container)
```

`retrieve` returns the URI of the AWS-managed container image holding the built-in
algorithm. You did not build it, do not maintain it, and do not pay for it separately —
this is what "built-in algorithm" means in practice.

> **Note:** if this call reports that the version is unavailable, list the versions your
> SDK supports and choose a current one. Do not hard-code a version you have not verified.

### 4.2 Configure the estimator

```python
from sagemaker.estimator import Estimator

xgb = Estimator(
    image_uri=container,
    role=role,
    instance_count=1,
    instance_type="ml.m5.large",
    output_path=f"s3://{bucket}/{prefix}/output",
    sagemaker_session=sess,
    base_job_name="aif-lab04-xgboost",
)
```

Read each argument as a piece of exam vocabulary:

- `image_uri` — the **algorithm**.
- `role` — the **execution role** from Step 2.2, which lets the job read your S3 data.
- `instance_type` / `instance_count` — the **training compute**, separate from the
  inference compute you choose later. They do not have to match.
- `output_path` — where the **model artefact** (`model.tar.gz`) will be written.

### 4.3 Set hyperparameters

```python
xgb.set_hyperparameters(
    objective="binary:logistic",
    num_round=100,
    max_depth=5,
    eta=0.2,
    subsample=0.8,
    eval_metric="auc",
)
```

These are **hyperparameters** — you set them *before* training. Contrast them with the
tree structures XGBoost learns, which are **parameters**.

| Hyperparameter | Effect | Increase it and… |
|---|---|---|
| `num_round` | Number of boosting rounds | More capacity, more risk of overfitting |
| `max_depth` | Maximum tree depth | More complex interactions, more overfitting |
| `eta` | Learning rate | Faster convergence, less stable |
| `subsample` | Fraction of rows sampled per round | Lower values add regularisation |

`objective="binary:logistic"` declares this a binary classification problem returning a
probability. Changing it to a regression objective would change the whole task.

### 4.4 Run the training job

```python
from sagemaker.inputs import TrainingInput

xgb.fit({
    "train": TrainingInput(train_uri, content_type="text/csv"),
    "validation": TrainingInput(val_uri, content_type="text/csv"),
})
```

Watch the streamed log. Two things to observe:

1. The per-round `train-auc` and `validation-auc` values. If training AUC keeps improving
   while validation AUC stalls or falls, that is **overfitting** — the model is memorising
   the training set rather than learning a generalisable pattern.
2. The final lines report **billable seconds**, which is the concrete meaning of "training
   bills only while it runs".

### 4.5 Inspect the job in the console

1. Open the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/) → in the
   left navigation, **Training jobs**.
2. Select the job that begins `aif-lab04-xgboost-`.
3. Note on the detail page:
   - **Algorithm / image** — the container from 4.1
   - **Hyperparameters** — exactly what you set in 4.3
   - **Input data configuration** — the two S3 channels, `train` and `validation`
   - **S3 model artifact** — the path to `model.tar.gz`
   - **Monitor** — links to CloudWatch metrics and logs
4. Confirm the status is **Completed** and note the **Billable time**.

This page is the answer to "how do I reproduce this model six months from now?" — the job
record captures the data location, the algorithm, the hyperparameters and the output.

---

### Step 5 — Deploy the model to a real-time endpoint

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

---

### Step 6 — Run inference and evaluate the model

The endpoint is live. Send it the held-back test data and find out how good the model
actually is.

### 6.1 Predict a single record

```python
X_test = test_df.drop(columns=["target"])
y_test = test_df["target"].values

single = X_test.iloc[0].tolist()
result = predictor.predict(single).decode("utf-8")
print("Raw response:", result)
print("Actual label:", y_test[0])
```

The endpoint returns a **probability** between 0 and 1, not a class. That is what
`objective="binary:logistic"` asked for.

### 6.2 Apply a threshold

```python
prob = float(result)
threshold = 0.5
predicted_class = 1 if prob >= threshold else 0
print(f"probability={prob:.4f}  predicted={predicted_class}  actual={y_test[0]}")
```

**The threshold is a business decision, not a model property.** Lowering it catches more
positives at the cost of more false alarms. In a medical screening context you would
lower it deliberately, because a missed positive costs far more than a false alarm.

### 6.3 Score the whole test set

```python
import numpy as np

payload = "\n".join(",".join(str(v) for v in row) for row in X_test.values)
raw = predictor.predict(payload).decode("utf-8")
probs = np.array([float(p) for p in raw.strip().split("\n")])
preds = (probs >= 0.5).astype(int)

print("predictions:", preds.shape)
```

### 6.4 Build the confusion matrix

```python
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

tn, fp, fn, tp = confusion_matrix(y_test, preds).ravel()

print(f"True negatives : {tn}")
print(f"False positives: {fp}")
print(f"False negatives: {fn}")
print(f"True positives : {tp}")
print()
print(f"Accuracy : {accuracy_score(y_test, preds):.4f}")
print(f"Precision: {precision_score(y_test, preds):.4f}")
print(f"Recall   : {recall_score(y_test, preds):.4f}")
print(f"F1       : {f1_score(y_test, preds):.4f}")
print(f"AUC      : {roc_auc_score(y_test, probs):.4f}")
```

Learn these definitions — Domain 1 and Domain 3 both test them:

| Metric | Formula | Answers |
|---|---|---|
| **Accuracy** | (TP + TN) / all | What fraction did it get right? Misleading when classes are imbalanced. |
| **Precision** | TP / (TP + FP) | Of the ones it flagged, how many were real? Optimise when false positives are costly. |
| **Recall (sensitivity)** | TP / (TP + FN) | Of the real ones, how many did it catch? Optimise when misses are costly. |
| **F1** | Harmonic mean of precision and recall | A single balanced score. |
| **AUC-ROC** | Area under the ROC curve | Ranking quality across *all* thresholds, independent of the one you chose. |

Precision and recall trade off against each other; moving the threshold in 6.2 moves you
along that trade-off. AUC does not depend on the threshold at all, which is why it is the
better headline number when the operating point is still undecided.

### 6.5 Try moving the threshold

```python
for t in [0.2, 0.35, 0.5, 0.65, 0.8]:
    p = (probs >= t).astype(int)
    print(f"threshold={t:<5} precision={precision_score(y_test, p):.3f}  recall={recall_score(y_test, p):.3f}")
```

Watch precision rise and recall fall as the threshold increases. **The model did not
change** — only the decision rule you wrapped around it. This is one of the most useful
practical insights in the whole course.

### 6.6 Invoke from outside the SDK (optional)

The endpoint is an ordinary HTTPS service any authorised application can call:

```python
import boto3, json

runtime = boto3.client("sagemaker-runtime", region_name=region)
row = ",".join(str(v) for v in X_test.iloc[1].values)

response = runtime.invoke_endpoint(
    EndpointName="aif-lab04-endpoint",
    ContentType="text/csv",
    Body=row,
)
print(response["Body"].read().decode("utf-8"))
```

This is what a web application, a Lambda function or an API Gateway integration would do.
The model is now a piece of infrastructure, not a notebook artefact.

**Now go straight to Step 7 and delete the endpoint.**

---

### Step 7 — Clean up

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

---

### Verification

- [ ] A billing budget with an alert exists in your account
- [ ] The notebook instance reached **InService** and `sagemaker.__version__`, the Region, the default bucket and the role ARN all printed
- [ ] `train.csv` and `validation.csv` exist in S3 under `aif-lab04-xgboost/`, with the target in the first column and no header row
- [ ] The training job shows status **Completed**, and you noted its billable time and model artefact path
- [ ] All three of Models, Endpoint configurations and Endpoints contained an entry after deployment
- [ ] You produced a confusion matrix and can state what each of TP, FP, TN and FN means for this dataset
- [ ] You observed precision rise and recall fall as the threshold increased, without retraining
- [ ] **The endpoint is deleted** — `aws sagemaker list-endpoints` returns an empty list
- [ ] The endpoint configuration, model, and notebook instance are deleted, and no Studio app is running
- [ ] The `aif-lab04-xgboost/` objects have been removed from the S3 default bucket

### Discussion questions

1. Your training AUC reaches 0.99 while validation AUC sits at 0.82. Name the problem, then give three distinct changes you could make — one to the data, one to the hyperparameters, one to the algorithm choice.
2. This model screens for a medical condition. Where would you set the threshold, and what would you have to build around the endpoint to make that choice safe in practice?
3. The same trained artefact could be served by a real-time endpoint, batch transform, serverless inference or asynchronous inference. For each of the four, describe a workload where it is clearly the right answer and state what would make it the wrong one.

---

---

## Lab 05 — The ML Pipeline and Data Preparation

Design a complete ML pipeline for a churn scenario, from business framing through data preparation and feature engineering to deployment and monitoring, grounded in the SageMaker console.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 1 — Fundamentals of AI and ML (20%)
**Task statement:** 1.3 Describe the ML development lifecycle
**WSQ mapping:** LU4 · Topic 7 Developing ML Solutions · K3 · A4 · LO4
**Slide reference:** v11 deck slides 84–135
**Estimated time:** 40 minutes

> **⚠️ Cost note:** the core of this lab is console navigation and design work, which
> creates nothing chargeable. The **optional** Data Wrangler walkthrough in Step 3.4 starts
> a SageMaker Canvas or Studio application that **bills per hour until you shut it down**.
> If you do that section, Step 7.4 is mandatory.

**Learning objectives:**
- Translate a business goal into an ML question, with distinct model metrics and business metrics
- Describe the stages of the ML lifecycle and name the AWS service that supports each
- Perform the checks that make up exploratory data analysis, and detect target leakage
- Apply pre-processing treatments for missing values, outliers, categorical variables, scaling and class imbalance without leaking data
- Engineer features for a tabular problem and explain how SageMaker Feature Store prevents training/serving skew
- Distinguish underfitting from overfitting and describe how automatic model tuning searches hyperparameters
- Select an evaluation metric appropriate to an imbalanced problem and a business constraint
- Choose a deployment option and design drift monitoring with SageMaker Model Monitor, Pipelines and the Model Registry

---

### Step 1 — Frame the business problem and map the pipeline

Lab 04 walked one narrow path through the ML lifecycle. This lab widens it to the full
pipeline the exam expects you to describe, and to the AWS service that supports each stage.

### 1.1 The scenario

You will design — not build — a pipeline for this brief:

> **Northwind Utilities** wants to reduce customer churn. It has 400,000 residential
> accounts, 3 years of monthly billing records, a support-ticket system, and a marketing
> team that can offer a retention discount to 5,000 customers a month. They want to know
> which 5,000.

Before anything technical, answer these:

1. **What is the ML question?** Not "reduce churn" — that is a business goal. The ML
   question is: *what is the probability that this account cancels in the next 90 days?*
2. **What kind of ML problem is it?** Supervised binary classification on tabular data.
3. **What does success look like?** Both a **model metric** (for example AUC, or recall at
   the top 5,000 ranked accounts) and a **business metric** (churn rate, revenue retained).
   These are not the same thing, and the exam tests that they are not.
4. **Is ML even the right tool?** If a simple rule — "anyone whose bill rose more than 40%"
   — captures most of the value, use the rule. ML is justified when the pattern is complex,
   the data volume is large, and the pattern changes over time.

> **Exam framing:** "business problem framing" is the first stage of the lifecycle and the
> one most often skipped. A model with excellent AUC that answers the wrong question is a
> failed project.

### 1.2 The full pipeline

| # | Stage | What happens | Primary AWS support |
|---|---|---|---|
| 1 | **Business problem framing** | Define the question, the metrics, and whether ML is warranted | — |
| 2 | **Data collection** | Gather and centralise raw data | Amazon S3, AWS Glue, Amazon Kinesis |
| 3 | **Exploratory data analysis (EDA)** | Understand distributions, missing values, correlations, leakage | SageMaker Data Wrangler, Amazon Athena, QuickSight |
| 4 | **Data pre-processing** | Clean, impute, deduplicate, encode, scale, split | SageMaker Data Wrangler, SageMaker Processing |
| 5 | **Feature engineering** | Create the variables the model actually learns from | SageMaker Data Wrangler, SageMaker Feature Store |
| 6 | **Model training** | Fit the algorithm to the training data | SageMaker training jobs, built-in algorithms, JumpStart |
| 7 | **Hyperparameter tuning** | Search for the best training settings | SageMaker automatic model tuning (AMT) |
| 8 | **Model evaluation** | Measure performance on held-out data; check bias | SageMaker evaluation, SageMaker Clarify |
| 9 | **Deployment** | Serve predictions | SageMaker endpoints, batch transform |
| 10 | **Monitoring** | Detect drift and degradation in production | SageMaker Model Monitor, Amazon CloudWatch |

Two points to fix in memory:

- **The pipeline is a loop, not a line.** Monitoring feeds back into data collection and
  retraining. A model is not "finished" at deployment.
- **Stages 2–5 typically consume the majority of a project's effort.** The exam reflects
  this: data preparation questions outnumber training questions.

### 1.3 Record your version

Write out the ten stages for the Northwind scenario, one line each, saying what you would
actually do at that stage for *this* problem. You will fill in the detail as you work
through Steps 2–6.

---

### Step 2 — Collect data and explore it

Stages 2 and 3 of the pipeline: get the data into one place, then look at it before you
touch it.

### 2.1 Data collection for the scenario

Northwind's data lives in three places. Map each to a data type and a collection approach:

| Source | Data type | How it reaches S3 |
|---|---|---|
| Billing records (relational database) | Structured, tabular and time-series | Scheduled extract, or AWS Glue / AWS DMS into S3 |
| Support tickets (free text) | Unstructured text | Export to S3; enrich with Amazon Comprehend |
| Meter readings (streaming) | Time-series | Amazon Kinesis Data Firehose into S3 |

Two design facts worth stating:

- **Amazon S3 is the centre of gravity.** Whatever the source, ML data lands in S3 because
  every SageMaker component reads from it.
- **A data lake plus a catalogue beats scattered extracts.** AWS Glue crawlers populate the
  Glue Data Catalog so Amazon Athena can query the raw files with SQL — often the cheapest
  possible EDA.

### 2.2 Look at the exploration tooling in the console

1. Open the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/) in
   `us-east-1`.
2. In the left navigation, look for **Data Wrangler** (it may appear under a data
   preparation grouping, or inside **SageMaker Canvas**, depending on your console version).
3. Read the description on the landing page. Do **not** launch it yet — Step 3 covers
   that, with a cost warning.

Data Wrangler is a visual data preparation tool. It imports from S3, Athena, Amazon
Redshift and other sources, profiles the data, offers built-in transforms, and exports
either a processed dataset or a repeatable processing job.

### 2.3 What EDA actually looks for

Whether you use Data Wrangler, Athena or pandas, EDA answers the same six questions.
Write down, for the Northwind data, what you would check for each:

| Question | What you are looking for | Why it matters |
|---|---|---|
| **What is the distribution of each feature?** | Skew, unexpected ranges, unit errors | Skewed features may need transformation |
| **How much is missing, and is it missing randomly?** | Null counts per column and per segment | Non-random missingness is itself a signal — and a bias risk |
| **Are there outliers?** | Extreme values | Could be errors to fix, or the rare events you care most about |
| **What is the class balance?** | Ratio of churned to retained | Churn is usually 2–5%; heavy imbalance changes metrics and sampling |
| **Which features correlate with the target — and with each other?** | Correlation matrix | Strong feature-to-feature correlation is redundancy; strong target correlation may be leakage |
| **Is there target leakage?** | Features unavailable at prediction time | The single most damaging silent error in ML |

### 2.4 The leakage trap

**Target leakage** is when a feature encodes information that would not exist at the moment
you actually need the prediction. For Northwind, a column called `cancellation_reason_code`
is perfect at predicting churn — and useless, because it is only populated *after* the
customer cancels.

Symptoms: implausibly high validation performance, and a model that collapses in
production. Test for it by asking of every feature: **"would I have this value, with this
value, at the moment I score a live customer?"**

Go through your Northwind feature list now and mark any column that fails that test.

---

### Step 3 — Pre-process the data

Stage 4: turn raw records into something an algorithm can consume without being misled.

### 3.1 The pre-processing checklist

| Problem | Typical treatment | Trap |
|---|---|---|
| **Missing values** | Impute with mean, median or a constant; or drop the row or column | Imputing with the mean of the *whole* dataset leaks test information into training |
| **Duplicates** | Deduplicate on a business key | Near-duplicates often survive an exact-match dedupe |
| **Outliers** | Cap (winsorise), transform, or remove | Removing outliers destroys the signal in fraud and fault detection |
| **Inconsistent categories** | Standardise (`SG`, `Singapore`, `sg` → one value) | Unseen categories at inference time will break naive encoders |
| **Categorical variables** | One-hot encoding for low cardinality; ordinal encoding where order is real | One-hot on a high-cardinality column explodes dimensionality |
| **Numeric scale differences** | Normalisation (0–1) or standardisation (mean 0, sd 1) | Fit the scaler on **training data only**, then apply it to validation and test |
| **Class imbalance** | Resampling, class weights, or a threshold chosen on a ranking metric | Oversampling before splitting puts copies of the same record on both sides of the split |
| **Text fields** | Tokenise, or extract features with Amazon Comprehend | — |

The single rule underneath half of these: **fit every transformation on the training split
only, then apply it to validation and test.** Anything else is data leakage.

### 3.2 Splitting, revisited

You split in Lab 04 with a random shuffle. For Northwind that would be **wrong**.

- The data is **time-series-flavoured** — you are predicting the future from the past. A
  random split lets the model train on March and be tested on February, which it will never
  do in production. Split by time: train on months 1–30, validate on 31–33, test on 34–36.
- The data has **grouped records** — many rows per account. If rows from the same account
  land in both train and test, the model can memorise the account rather than learn the
  pattern. Split by **account**, not by row.

Choosing the split strategy is a modelling decision, not a formality.

### 3.3 See where pre-processing runs on AWS

In the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/) left
navigation, find **Processing jobs**.

A **SageMaker Processing job** runs a container over your data on managed compute and then
shuts down — the same billing model as a training job. It is how you run pre-processing at
scale and, critically, how you run **the same transformation code at training time and at
inference time**. Divergence between the two is a classic production failure known as
**training/serving skew**.

The list is probably empty. Note what a job record would contain: an input S3 path, a
container, an instance type, and an output S3 path.

### 3.4 Optional hands-on — SageMaker Data Wrangler

> **⚠️ COST WARNING:** Data Wrangler runs inside a **SageMaker Canvas or Studio
> application**, which **bills per hour while it is running** and does not stop when you
> close the browser tab. If you do this section you **must** complete Step 7.4 to shut the
> application down. Skip this section if you are unsure — Steps 3.1–3.3 carry the
> examinable content.

If you choose to proceed:

1. In the SageMaker console, launch **SageMaker Canvas** (or Studio) and create a
   **Data Wrangler** data flow.
2. Import a CSV from S3 — the `customers.csv` from Lab 02 works, or any small tabular file.
3. Open the **Data quality and insights report**, which profiles the dataset: column types,
   missing values, distributions, and warnings about likely issues.
4. Add two or three transforms from the built-in list — for example handle missing values,
   encode a categorical column, and scale a numeric column. Each appears as a node in the
   flow.
5. Note the **Export** options: you can export the flow as a SageMaker Processing job,
   which is precisely the reproducibility point from 3.3 — the visual flow becomes runnable,
   version-controllable code.
6. **Immediately** go to Step 7.4 and shut the application down when you are finished.

---

### Step 4 — Engineer features and store them

Stage 5. Pre-processing makes data *usable*; feature engineering makes it *predictive*.

### 4.1 What feature engineering is

A **feature** is an input variable the model learns from. Feature engineering is creating
better ones from the raw columns — usually by encoding domain knowledge the algorithm has
no way to discover on its own.

For Northwind, the raw table has `monthly_bill` per account per month. None of these
columns exists yet, and every one is more predictive than the raw value:

| Engineered feature | How it is built | Why it helps |
|---|---|---|
| `bill_change_pct_3m` | Current bill ÷ mean of previous 3 months | A sudden bill jump is a churn trigger |
| `tenure_months` | Today − signup date | New customers churn at different rates |
| `tickets_last_90d` | Count of support tickets in a window | Dissatisfaction signal |
| `avg_ticket_sentiment` | Amazon Comprehend sentiment over ticket text, averaged | Turns unstructured text into a numeric feature |
| `days_since_last_payment` | Recency | Payment behaviour precedes cancellation |
| `is_winter_month` | Calendar flag | Separates seasonal bill rises from real ones |
| `usage_vs_similar_homes` | Ratio to a peer group | Normalises for household size |

Note the pattern: **aggregations over time windows, ratios, recency counts, and
domain-derived flags**. That set covers most tabular feature engineering.

### 4.2 Feature engineering as dimensionality change

Two directions, both examinable:

- **Feature creation** adds columns — the table above.
- **Feature selection and dimensionality reduction** remove them. Drop features that are
  redundant (highly correlated with another), useless (near-zero variance), or leaky.
  **Principal component analysis (PCA)** compresses many correlated numeric features into
  fewer components.

More features is not better. Too many relative to the number of rows increases overfitting
and training cost, and makes the model harder to explain — which matters for Domain 4.

### 4.3 The reproducibility problem, and SageMaker Feature Store

Here is the failure mode Feature Store exists to solve:

- The data science team computes `bill_change_pct_3m` in a training notebook.
- The application team recomputes it in production code, subtly differently — a different
  window, or a different null-handling rule.
- The model receives inputs at inference time that do not match what it was trained on, and
  quietly degrades. This is **training/serving skew**.

**Amazon SageMaker Feature Store** is a purpose-built repository for engineered features:

| Concept | Meaning |
|---|---|
| **Feature group** | A named schema — a table of features sharing a record identifier and an event time |
| **Record identifier** | The key, e.g. `account_id` |
| **Event time** | The timestamp each feature value became true |
| **Online store** | Low-latency lookup for real-time inference |
| **Offline store** | Historical values in S3 for training and batch scoring |

The online and offline stores are populated from the same ingestion, so **training and
inference read the same definition of each feature**. The event time makes **point-in-time
correct** training sets possible: when building a training row for 1 March, you retrieve
feature values as they were on 1 March, not today's values. Without that, you leak the
future into the past.

### 4.4 Find it in the console

1. In the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/) left
   navigation, open **Feature Store** (under a data or governance grouping depending on
   your console version).
2. Read the **Feature groups** page. It is empty in a new account.
3. Note what creating a feature group would require: a name, a record identifier column, an
   event time column, a schema, and a choice of online store, offline store or both.

> **Cost note:** a feature group with an **online store** enabled provisions capacity and
> incurs ongoing charges; an offline-only store is S3 storage. This lab does not create
> one. If you experiment beyond the lab, delete the feature group afterwards.

### 4.5 Sketch your feature group

On paper, define the feature group you would create for Northwind:

- **Name:** `northwind-account-features`
- **Record identifier:** `account_id`
- **Event time:** `feature_date`
- **Features:** the seven from 4.1, each with a type
- **Stores:** offline for training; online as well, if the retention offer needs to be
  decided live rather than in a monthly batch

That last decision links straight back to Lab 01: **real-time inference needs an online
store; a monthly batch job does not.**

---

### Step 5 — Train, tune and evaluate

Stages 6, 7 and 8. You ran stage 6 by hand in Lab 04; this step adds the two that surround
it.

### 5.1 Training, in one paragraph

Choose an algorithm suited to the data type — XGBoost or Linear Learner for tabular, a
neural network for images or text, or a foundation model where the task is generative.
Supply the training and validation channels, set hyperparameters, and run the job. Training
bills only while it runs.

For Northwind: **XGBoost, binary classification, tabular** — the same shape as Lab 04.

### 5.2 Underfitting, overfitting, and the bias-variance trade-off

| Condition | Training performance | Validation performance | Cause | Fix |
|---|---|---|---|---|
| **Underfitting** | Poor | Poor | Model too simple, features too weak, trained too briefly | More capacity, better features, more rounds |
| **Good fit** | Good | Good, close to training | — | — |
| **Overfitting** | Excellent | Noticeably worse | Model memorised the training set | More data, fewer features, regularisation, early stopping, simpler model |

- **Bias** (in the statistical sense) is error from an over-simple model — it underfits.
- **Variance** is error from over-sensitivity to the training sample — it overfits.
- Reducing one tends to raise the other. Finding the balance is what tuning does.

> Note the collision of vocabulary: **statistical bias** here means systematic model error.
> **Societal bias** — unfair outcomes across demographic groups — is a different concept,
> covered in Domain 4 and Lab 20. The exam uses both senses.

### 5.3 Hyperparameter tuning

Manually guessing `max_depth` and `eta` as you did in Lab 04 does not scale. **SageMaker
automatic model tuning (AMT)** runs many training jobs across a hyperparameter search space
and returns the best.

1. In the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/) left
   navigation, open **Hyperparameter tuning jobs** (near Training jobs).
2. The list is empty. Note what a tuning job specifies:
   - The **objective metric** to optimise, e.g. `validation:auc`, and whether to maximise
     or minimise it
   - **Ranges** for each hyperparameter to search
   - The **maximum number of training jobs** and how many run in **parallel**
   - The **search strategy** — Bayesian (learns from previous trials), random, grid, or
     Hyperband (stops unpromising jobs early)

> **⚠️ Cost warning:** a tuning job launches *many* training jobs. Cost scales with the
> maximum-jobs setting. Always cap it. This lab does not run one.

### 5.4 Evaluation

Evaluate on the **test split**, untouched until now.

For Northwind's binary classifier, use the metrics from Lab 04 — accuracy, precision,
recall, F1, AUC-ROC — with two additions:

- With churn at perhaps 3%, a model that predicts "no churn" for everyone scores **97%
  accuracy** and is worthless. Accuracy is the wrong headline metric here.
- The actual business constraint is "5,000 offers a month". So the right metric is
  **precision within the top 5,000 ranked accounts** — of the 5,000 you contact, how many
  would really have churned? That is a ranking question, which is why AUC and
  precision-at-k beat accuracy for this problem.

For **regression** problems the metric set is different, and the exam expects both:

| Metric | Meaning |
|---|---|
| **MAE** | Mean absolute error — average size of error, in the units of the target |
| **MSE / RMSE** | Squared error; punishes large errors much more heavily |
| **R²** | Proportion of variance explained |

### 5.5 Evaluate for more than accuracy

A complete evaluation also asks:

- **Is performance equal across segments?** Overall AUC can hide a model that works well
  for urban accounts and badly for rural ones. **SageMaker Clarify** measures this — Lab 20.
- **Can we explain individual predictions?** Feature attribution, also Clarify — Lab 21.
- **What is the cost of each error type?** A false positive is a wasted discount; a false
  negative is a lost customer. They are rarely equal, and that inequality should set the
  threshold.

---

### Step 6 — Deploy, monitor and close the loop

Stages 9 and 10, plus the automation that ties the pipeline together.

### 6.1 Deployment choice for Northwind

The business offers 5,000 discounts a month, decided in advance. Nobody is waiting for an
answer, and all the inputs already exist.

**Therefore: batch transform, run monthly.** Not a real-time endpoint.

Choosing a real-time endpoint here would mean paying for always-on instances to answer
twelve requests a year. Recognising this is worth more marks than any amount of algorithm
knowledge — it is the most common cost-optimisation question in Domain 1.

The design changes only if the requirement changes: if the retention offer must appear
while a customer is on the phone to the call centre, then it is a real-time endpoint, and
Feature Store's **online store** becomes necessary.

### 6.2 Why monitoring is a stage, not an afterthought

Models decay. Three named causes:

| Type | What changes | Northwind example |
|---|---|---|
| **Data drift** (covariate shift) | The distribution of the *inputs* changes | A tariff change shifts every bill upward |
| **Concept drift** | The *relationship* between inputs and target changes | A competitor enters the market and churn behaviour changes entirely |
| **Data quality issues** | The pipeline breaks | An upstream schema change silently sends nulls |

None of these is visible from the model itself. The endpoint keeps returning confident
predictions that are increasingly wrong.

### 6.3 SageMaker Model Monitor

1. In the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/) left
   navigation, find **Model Monitor** or the monitoring section under inference.
2. Read the available monitor types. SageMaker Model Monitor can watch for:

| Monitor | Detects |
|---|---|
| **Data quality** | Input statistics or schema deviating from a captured baseline |
| **Model quality** | Predictions diverging from actual outcomes, once ground truth arrives |
| **Bias drift** | Bias metrics moving beyond a threshold over time |
| **Feature attribution drift** | The relative importance of features shifting |

The mechanism to remember: **capture a baseline from the training data, enable data capture
on the endpoint, schedule monitoring jobs to compare live traffic against the baseline, and
alert through Amazon CloudWatch when a constraint is violated.**

Note that **model quality** monitoring requires ground truth. For Northwind, whether an
account actually churned is only known 90 days later — so model quality can only be
measured with a lag, while data quality can be measured immediately. That lag is a real
design constraint.

### 6.4 Closing the loop

When monitoring fires, the response is to retrain — which means going back to stage 2 with
fresh data. Doing that reliably by hand is not realistic, so AWS provides:

1. **SageMaker Pipelines** — a CI/CD workflow service for ML. Look for **Pipelines** in the
   left navigation. A pipeline chains processing, training, evaluation, conditional
   approval and registration steps into one repeatable, version-controlled definition.
2. **SageMaker Model Registry** — open **Model registry** (under models or governance). It
   holds **model groups** containing **versioned model packages**, each with an approval
   status. A pipeline registers a new version as `PendingManualApproval`; a human approves
   it; approval triggers deployment.

Together these give you **MLOps**: the same discipline software engineering applies to code,
applied to models — versioning, automated testing, approval gates and reproducible
deployment.

### 6.5 Review your pipeline

Return to the ten-line pipeline you wrote in Step 1.3 and fill in, for every stage:

- what you would do for Northwind
- which AWS service supports it
- what would go wrong if you skipped it

Check specifically that you have:

- Split by **account and by time**, not randomly (Step 3.2)
- Removed the leaky `cancellation_reason_code` (Step 2.4)
- Chosen **precision-at-5000 or AUC**, not accuracy (Step 5.4)
- Chosen **batch transform**, not a real-time endpoint (Step 6.1)
- Planned **data quality monitoring now** and **model quality monitoring at a 90-day lag**
  (Step 6.3)

Those five decisions are the substance of this lab.

---

### Step 7 — Clean up

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

---

### Verification

- [ ] You wrote the Northwind ML question as a prediction, not as a business goal, with both a model metric and a business metric
- [ ] You produced a ten-line pipeline in Step 1.3 and completed it in Step 6.5
- [ ] You identified `cancellation_reason_code` as target leakage and can explain the test that catches it
- [ ] You can explain why a random row-level split is wrong for this dataset, and what to split by instead
- [ ] You listed at least five engineered features and can name the pattern each one follows
- [ ] You located Feature Store, Processing jobs, Hyperparameter tuning jobs, Model Monitor, Pipelines and Model registry in the SageMaker console
- [ ] You can state why accuracy is the wrong headline metric at a 3% churn rate
- [ ] You justified batch transform over a real-time endpoint for this scenario
- [ ] No SageMaker endpoint, notebook instance, Studio or Canvas application, or feature group is running in your account

### Discussion questions

1. Northwind's model performs well for three months and then degrades sharply. Walk through how you would diagnose whether this is data drift, concept drift or a broken pipeline, and say which SageMaker monitor would have caught each first.
2. The data science team wants to add `avg_ticket_sentiment` from Amazon Comprehend as a feature. What must be true about how that value is computed at training time and at inference time, and which service exists specifically to guarantee it?
3. The marketing director asks for "the most accurate model possible". Rewrite that request as a set of requirements a data scientist could actually build against, and explain what you would have to ask about the cost of a false positive versus a false negative.

---

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.