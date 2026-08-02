# Step 3 — Understand labelled versus unlabelled data

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
