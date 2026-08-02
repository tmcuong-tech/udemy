# Step 5 — Train, tune and evaluate

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
