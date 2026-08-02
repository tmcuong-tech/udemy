# Step 1 — Frame the fairness question: facet, label and positive outcome

Guardrails (Lab 19) control *what a model is allowed to say*. Clarify answers a different
question entirely: *is the model treating groups of people fairly?* A guardrail will happily
pass a polite, well-formatted, systematically discriminatory answer. **Fairness** needs its
own instrumentation.

Before you can measure bias you must state precisely what you are measuring. Clarify forces
this, which is the most valuable thing about it.

### 1.1 The vocabulary

| Term | Meaning |
|---|---|
| **Facet** | The sensitive attribute you are analysing — gender, age band, postal region. The column Clarify groups by. |
| **Facet value** | The specific group treated as the focus of the analysis (facet = `gender`, facet value = `female`). |
| **Label (target)** | The outcome column the model predicts — for example `loan_approved`. |
| **Positive label value** | The outcome considered favourable (`approved = 1`). Bias is measured with respect to who receives it. |
| **Pre-training bias** | Bias measured in the **dataset alone**, before any model exists. Needs data only. |
| **Post-training bias** | Bias measured in the **model's predictions**. Needs a trained model or a file of predictions. |

### 1.2 The scenario used throughout this lab

A bank trains a model to predict `loan_approved` (1 = approved). You will analyse it for
age-related bias.

- **Facet:** `applicant_age_band`
- **Facet values:** `under_35` and `35_and_over`
- **Label:** `loan_approved`
- **Positive label value:** `1`

Write these four lines down. Every metric in the rest of the lab is defined relative to
them, and a bias report without them stated is uninterpretable.

### 1.3 The hard part is choosing the facet, not computing the metric

Clarify computes whatever you ask it to. Deciding *what to ask* is a judgement call with
legal and ethical weight:

- **The facet may not be in your data.** Many organisations do not collect ethnicity, and
  cannot measure bias they cannot see. Collecting it raises its own privacy questions —
  a genuine tension between **fairness** and **privacy**, not a puzzle with a clean answer.
- **Proxies leak.** Removing `age` does not remove age bias if `years_since_graduation`
  remains. "Fairness through unawareness" is the most common and most confidently wrong
  approach to this problem.
- **Intersectionality.** A model can look fair on gender alone and fair on age alone while
  disadvantaging a specific combination. Single-facet analysis is a floor, not a ceiling.

> **Governance point:** who chose this facet, and who signed off? Facet selection should be
> a documented decision involving domain, legal and — where possible — affected-community
> input. If it was chosen by whoever wrote the notebook, that is a finding in itself.

### 1.4 Decide your path

| | Path 1 | Path 2 |
|---|---|---|
| Requires | An existing trained SageMaker model plus a tabular dataset in S3 | Nothing |
| Cost | **Billable compute** — processing job plus a temporary endpoint | None |
| Covered in | Step 4 | Step 5 |

**Path 2 is the expected route for most learners and is fully sufficient for the learning
outcome.** Steps 2 and 3 apply to both paths — do them regardless.
