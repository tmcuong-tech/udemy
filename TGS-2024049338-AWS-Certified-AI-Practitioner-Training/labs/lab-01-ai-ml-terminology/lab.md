# Lab 01 — AI, ML and Deep Learning Terminology

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

## Step 1 — Survey the AWS AI and ML console landscape

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

## Step 2 — Map the AI, ML, deep learning and generative AI hierarchy

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

## Step 3 — Distinguish supervised, unsupervised and reinforcement learning

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

## Step 4 — Separate algorithm, model, training and inference

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

## Step 5 — Compare inferencing options: real-time versus batch

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

## Step 6 — Clean up

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

## Verification

- [ ] You can name the three layers of the AWS AI/ML stack and say who supplies the model in each
- [ ] You classified all six workloads in Step 2 and agree with the answer key
- [ ] You can state the feedback signal that defines supervised, unsupervised and reinforcement learning
- [ ] You can explain the difference between a parameter and a hyperparameter
- [ ] You located Training jobs, Models and Endpoints as three separate pages in the SageMaker console
- [ ] You matched all four scenarios in Step 5 to an inferencing option
- [ ] No SageMaker notebook instance, Studio application, Canvas session or endpoint is running in your account

## Discussion questions

1. A colleague describes their spam filter as "AI". What follow-up questions would you ask to decide whether it is a rule engine, classical machine learning, or deep learning — and why does the answer change how the system is maintained?
2. A team wants product recommendations refreshed nightly for 20 million customers, and also shown live as a shopper browses. Which inferencing options would you use for each requirement, and why is using one option for both a poor design?
3. Labelling data is the expensive part of supervised learning. Given that, why would an organisation still choose supervised learning over unsupervised learning for a fraud-detection problem?

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.
