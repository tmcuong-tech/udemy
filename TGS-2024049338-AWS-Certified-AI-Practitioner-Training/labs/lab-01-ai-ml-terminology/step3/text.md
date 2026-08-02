# Step 3 — Distinguish supervised, unsupervised and reinforcement learning

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
