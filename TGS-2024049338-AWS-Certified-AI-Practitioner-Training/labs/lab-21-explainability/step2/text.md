# Step 2 — SHAP feature attribution and the baseline

SageMaker Clarify implements explainability using **SHAP** (SHapley Additive exPlanations),
a feature-attribution method that assigns each input feature a signed contribution to a
prediction.

### 2.1 The core idea

SHAP originates in cooperative game theory. Treat the prediction as a payout and the
features as players who cooperated to produce it. SHAP distributes the payout among the
features according to how much each one contributed.

Two properties follow, and they are what make SHAP useful:

- **Signed.** A feature can push a prediction *up* or *down*. "Short employment tenure
  contributed −0.14 to the approval score" is more informative than "tenure was important".
  Methods that report only importance magnitude lose the direction.
- **Additive.** The contributions sum back to the difference between this prediction and the
  baseline. Nothing is unexplained, and the attributions form a complete account.

Aggregate the absolute attributions across many rows and you get a **global** explanation.
Inspect one row and you get a **local** one. Same computation, different scope — this is why
SHAP is the default choice for tooling that must serve both audiences.

### 2.2 The baseline is the part everyone gets wrong

SHAP attributions are always measured **relative to a baseline**. The question SHAP actually
answers is not "why did the model predict this?" but:

> "Why did the model predict *this* rather than what it would have predicted for the
> **baseline** input?"

Change the baseline and every attribution changes. The baseline is not a technical detail —
it defines the counterfactual, and therefore defines what the explanation *means*.

| Baseline choice | The explanation then means |
|---|---|
| Dataset average or median row | Why this applicant differs from a typical applicant |
| A specific reference cohort | Why this applicant differs from that cohort |
| All-zeros or "no information" row | Why this applicant differs from a meaningless input — usually the wrong choice |

**A poorly chosen baseline produces confident, well-formatted, misleading explanations.**
This is worse than no explanation, because it survives review.

Concretely: explain a refusal against an average-applicant baseline and you learn what made
this person weaker than average. Explain it against a baseline of *approved* applicants and
you learn what would have needed to change for approval. Those are different questions and
different answers, from the same model and the same row.

> **Governance point:** the baseline must be **documented alongside the explanation**. An
> attribution figure quoted without its baseline is uninterpretable, and it will be quoted
> without its baseline unless you make that impossible.

### 2.3 The other configuration parameters

| Parameter | What it controls |
|---|---|
| **Number of samples** | SHAP values for complex models are approximated by sampling. More samples give more stable attributions and cost more compute. |
| **Baseline rows** | One row or a set. A set generally gives a more robust reference than a single hand-picked row. |
| **Aggregation** | How per-row attributions are combined into the global view — typically mean absolute contribution. |

Instability is a real failure mode. If you run the analysis twice with too few samples and
get materially different attributions, the explanation is noise. Check for this before you
brief anyone on the results.

### 2.4 The honest limitations

SHAP is the best widely available tool for this job, which is not the same as being
reliable in all conditions. Know these before you present SHAP output as truth:

- **Correlated features split credit unpredictably.** If `income` and `employment_tenure`
  move together, the attribution divided between them depends on the algorithm's internals,
  not on which one the model "really" used. Do not read a small difference between two
  correlated features as meaningful.
- **Attribution is not causation.** SHAP tells you what the *model* used. It says nothing
  about what causes the real-world outcome. A model can rely heavily on a feature that has
  no causal relationship to default risk at all.
- **It is post-hoc.** SHAP explains a model it did not build and cannot inspect the true
  reasoning of. This is the crux of Step 5.
