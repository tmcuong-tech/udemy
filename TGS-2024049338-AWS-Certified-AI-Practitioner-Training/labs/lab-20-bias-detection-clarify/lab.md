# Lab 20 — Bias Detection with SageMaker Clarify

Frame a fairness question as facet, label and positive outcome, then compare pre-training and post-training bias metrics using either your own Clarify job or a guided bias report walkthrough.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 4 — Guidelines for Responsible AI (14%)
**Task statement:** 4.1 Explain the development of AI systems that are responsible
**WSQ mapping:** LU3 · Topic 6 Responsible AI Practices · K8 · A3 · LO3
**Slide reference:** v11 deck slides 273–284
**Estimated time:** 40 minutes

**Learning objectives:**
- Express a fairness question as facet, facet value, label and positive label value
- Explain Class Imbalance and Difference in Proportions of Labels and the phase they belong to
- Distinguish the post-training bias metric families and explain why error-rate gaps matter most
- Explain why pre-training and post-training analysis must both be run, using inherited versus amplified bias
- Configure a Clarify bias analysis job, or interpret a bias report without running one
- Draft an issue report stating observation, evidence, harm and recommendation

**Prerequisites:**
- An AWS account with console access. **Path 2 requires no AWS resources at all.**
- For Path 1 only: an existing trained SageMaker model, a tabular dataset in Amazon S3 with a header row, and permission to run SageMaker processing jobs.
- Lab 19 completed, or an equivalent understanding of what a guardrail does and does not control.

> **Note on cost:** Path 2 is free. **Path 1 starts billable compute** — a processing job plus a temporary inference endpoint that Clarify deploys to obtain predictions. SageMaker endpoints, notebook instances and Studio apps bill continuously until deleted. This lab does not quote prices — check the current AWS pricing pages for your Region. Follow the Clean up step without exception.

---

## Step 1 — Frame the fairness question: facet, label and positive outcome

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

---

## Step 2 — Pre-training bias metrics: measuring the data

Pre-training metrics look at the **dataset only**. No model is involved, nothing has been
trained, and you can run them the moment you have labelled data. That makes them the
cheapest fairness check available and the one most often skipped.

### 2.1 Class Imbalance (CI)

**Question it answers:** is one facet group far larger than another in the dataset?

If `under_35` is 20% of your rows and `35_and_over` is 80%, the model has four times as much
evidence about the older group. It will fit them better. Errors will concentrate on the
smaller group not because of malice in the algorithm but because of arithmetic in the data.

CI is reported as a value that is zero when the groups are equally represented and moves
toward its extremes as one group dominates. You do not need to memorise the formula. You
need to know it is a **dataset composition** measure and that a large imbalance predicts
worse performance for the minority group.

### 2.2 Difference in Proportions of Labels (DPL)

**Question it answers:** does one facet group already receive the positive outcome more
often in the **training labels**, before any model exists?

This is the metric that catches inherited unfairness. If historical loan officers approved
41% of older applicants and 22% of younger ones, that gap is sitting in your labels. Train
on it and the model learns it as ground truth.

DPL is zero when both groups receive the positive label at the same rate, and grows as the
gap widens in either direction.

### 2.3 The distribution-based measures

Clarify also offers pre-training measures that compare the *distribution* of labels or
features between groups — divergence-based and distance-based comparisons, and measures of
how well the facet can be predicted from the other features. That last family is how you
detect **proxies**: if a model can guess someone's age band from the rest of the row with
high accuracy, dropping the age column achieves nothing.

Describe these by their purpose rather than quoting exact names unless you can see the label
in the console. The exam tests the concept, not the nomenclature.

### 2.4 Why you cannot skip this phase

Here is the trap, and it is the single most important idea in this lab:

> **A model can score perfectly on post-training bias metrics simply because it faithfully
> reproduced bias that was already in the labels.**

If the data says one group is approved at 22% and another at 41%, a model that predicts
exactly those rates has near-zero *difference* between what the data said and what the model
did. Post-training metrics that compare model behaviour to the labels will look excellent.
The system is still discriminating; it has just done so accurately.

Pre-training metrics protect you from congratulating yourself on inherited unfairness.
**Always run both phases.**

### 2.5 There is no universal threshold

Do not treat any numeric cutoff as authoritative. There is no value of DPL that is
"fair" across all contexts. Acceptable ranges are a **policy decision** made with domain,
legal and affected-community input — and the decision, its rationale, and its author must be
documented. A number without a documented rationale is not governance; it is a number.

---

## Step 3 — Post-training bias metrics: measuring the model

Post-training metrics need the model's **predictions**. Clarify obtains them either from a
predictions file you supply or by deploying your model to a temporary endpoint and calling
it — which is why this phase costs money and the pre-training phase does not.

### 3.1 The three families you should recognise

| Family | Question it answers |
|---|---|
| Difference in **positive prediction rates** between groups | Does the model approve one group more often than another? |
| Differences in **error rates** — accuracy, recall or specificity gaps | Does the model make more mistakes for one group, and *which kind* of mistake? |
| **Treatment-equality** style comparisons | Is the *ratio* of false positives to false negatives the same across groups? |

Know which family a described symptom belongs to. That is what the exam asks.

### 3.2 Error rates matter more than approval rates

An approval-rate gap tells you the model treats groups differently. An error-rate gap tells
you **who is being harmed and how**, which is the question that actually drives remediation.

Consider a lending model with a higher **false negative** rate for one group. A false
negative here is a creditworthy applicant refused. The harm is invisible: nobody defaults,
no loss appears in any report, the model's headline accuracy is fine, and the affected
people simply go elsewhere and never appear in your data again. Bias that produces no
observable loss is the bias most likely to survive for years.

Now flip the error type. A higher **false positive** rate for one group means more
applicants approved who should not have been — they receive credit they cannot service.
Which is worse depends entirely on the domain:

| Domain | False positive | False negative | Usually worse |
|---|---|---|---|
| Lending | Approved, then defaults | Refused unfairly | Contested — depends on loan size and consequences of default |
| Medical screening | Unnecessary follow-up test | Missed disease | False negative, decisively |
| Content moderation | Legitimate post removed | Harmful post left up | Depends on platform and harm severity |

You cannot answer "is this model fair?" without answering "fair with respect to which
error, in which domain, for whom?"

### 3.3 Amplification

Compare the label gap to the prediction gap. If the model's approval gap is **wider** than
the gap in the training labels, the model has *amplified* the bias rather than merely
inheriting it.

This happens routinely. A model optimising overall accuracy can find that being more
decisive on a majority pattern improves its loss, and the minority group's already-thin
evidence gets rounded away. The model did exactly what you asked. You asked for the wrong
thing.

Amplification is the strongest single argument for running pre-training and post-training
metrics **together** — neither one alone reveals it.

### 3.4 Mitigation is not just "rebalance the data"

When a finding is confirmed, the response options span the whole lifecycle:

- **Data** — collect more data for the under-represented group, reweight, or resample.
- **Features** — remove or constrain a feature identified as an unlawful proxy.
- **Training** — apply fairness constraints during optimisation.
- **Post-processing** — adjust decision thresholds per group. This is effective and legally
  fraught; in many jurisdictions treating groups differently at the threshold is itself
  prohibited, even when done to improve fairness.
- **Process** — route affected cases to human review, or narrow the model's scope so it
  never decides alone.

The last option is underrated. "This model should not make this decision unaided" is a
legitimate and often correct engineering conclusion.

---

## Step 4 — Path 1: run a Clarify bias job against your own model

> ### COST WARNING — this step starts billable compute
> A Clarify processing job runs on instances you choose and bills for the duration.
> Post-training analysis additionally causes Clarify to **deploy your model to a temporary
> (shadow) endpoint**. If the job fails midway, that endpoint can be left behind and will
> **bill continuously until you delete it**. Do not start this step unless you intend to
> follow Step 6 immediately afterwards.

**Only do this step if you already have a trained SageMaker model and a tabular dataset in
S3.** Otherwise skip to Step 5, which is the expected route and fully sufficient.

### 4.1 Prepare the inputs

You need:

- A **dataset** in S3 as CSV or Parquet, with a header row, containing your facet column
  and your label column.
- An **output S3 prefix** where the bias report and analysis JSON will be written.
- A **model** already registered in SageMaker, if you want post-training metrics.

### 4.2 Configure the job

1. Go to the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/).
2. In the left navigation, open SageMaker Studio, or the Clarify/processing entry point
   available in your console version.
3. Create a **Clarify processing job** and supply:

**Data configuration**
- Input dataset S3 URI and content type
- Output S3 prefix
- `label` — the target column name
- Header row and dataset format

**Bias configuration**
- `label_values_or_threshold` — which value(s) count as the positive outcome
- `facet` — the sensitive column, plus the facet value(s) under analysis
- **Analysis type** — pre-training only, post-training only, or both

**Model configuration** (required for post-training bias)
- The model name, the instance type and count for the shadow endpoint, and the
  accept/content types the model expects
- For post-training metrics Clarify also needs to know how to read the model's output —
  which field holds the probability or the predicted label, and any threshold to apply

**Job resources**
- Instance type and instance count for the processing job itself

4. Run the job and wait for completion.

### 4.3 Retrieve and read the outputs

From your S3 output prefix you will get:

- **`analysis.json`** — the computed metric values, machine-readable
- A **generated report** summarising the analysis in readable form
- Supporting artefacts depending on which analyses you enabled

Read the pre-training section first, then the post-training section, and compare them —
that comparison is where amplification (Step 3.3) shows up.

### 4.4 Immediately verify nothing is left running

Before you do anything else:

- [ ] The processing job shows **Completed**, **Stopped** or **Failed** — not **InProgress**.
- [ ] **Endpoints** — check the endpoints list even if you did not deliberately create one.
      Clarify's shadow endpoint is normally cleaned up automatically, but a failed job can
      strand it.

Then complete Step 6 in full.

### 4.5 If you cannot run Path 1

That is the expected case, and it is not a gap in your learning. The exam tests whether you
can **read and reason about** a bias report, choose the right metric family for a described
symptom, and report a finding responsibly. Step 5 exercises all three.

---

## Step 5 — Path 2: guided walkthrough of a bias report

No AWS resources are required for this step. Work through it in your notes or in
discussion. This is the expected route for most learners.

### 5.1 The scenario

A bank trains a model to predict `loan_approved` (1 = approved). The training set has
10,000 rows. The facet is `applicant_age_band` with values `under_35` and `35_and_over`.

> ### These figures are illustrative teaching data
> The numbers below were constructed for this lab. They are **not** real measurements, not
> drawn from any AWS dataset, and not representative of any actual lending institution. They
> exist to make the metric relationships concrete.

| Group | Rows in dataset | Approved in training labels | Approved by the model |
|---|---|---|---|
| `under_35` | 2,000 | 22% | 19% |
| `35_and_over` | 8,000 | 41% | 44% |

### 5.2 Work through the findings

Answer each in writing. The written answers, not the reading, are the exercise.

**1. Class Imbalance.**
Which group is under-represented, and by how much? The split is 2,000 against 8,000 — a
1:4 ratio. What risk does that create for the model's learned behaviour on the smaller
group, and which of the three post-training metric families would you expect to reveal it?

**2. DPL — pre-training.**
There is a 19-point gap in the *training labels* between the two groups (22% against 41%).
Does this gap originate in the model? What are the plausible sources — historical lending
decisions, proxy variables such as income or employment tenure, sampling of who applied in
the first place, or something else? Name at least two and say how you would test each.

**3. Post-training amplification.**
The model's approval gap is 25 points (19% against 44%), *wider* than the 19-point label
gap. State in one sentence what it means when a model amplifies a bias present in the data,
and explain why a post-training metric alone would not have told you this.

**4. Error rates.**
Suppose the model's false-negative rate is materially higher for `under_35`. Who bears the
harm? Is a false negative or a false positive worse in a lending context? Would your answer
change for a medical screening model — and what does that tell you about whether "fairness"
can be defined once and reused?

**5. Proxies.**
Suppose the largest single driver of rejections for `under_35` turns out to be
`employment_tenure_years`. Is that feature legitimately predictive of default risk, an
unlawful proxy for age, or both at once? How would you decide, and who else needs to be in
that conversation? (Lab 21 gives you the tooling — SHAP — that produces this finding.)

**6. Remediation.**
Pick two mitigations from Step 3.4 and argue for one over the other for this specific case.
Include what each would cost and what new risk each introduces.

### 5.3 Write the issue report

This is your assessment artefact for **A3 — identify and report any issues with the AI
applications and data collected**.

Draft three to four sentences you would send to the model owner. It must state:

1. **What you observed** — the specific behaviour, with the group named.
2. **Which metric evidences it** — name the metric and the phase it belongs to.
3. **What harm it plausibly causes** — to whom, and how visible that harm is.
4. **What you recommend next** — a concrete action with an owner, not "investigate further".

A worked structure, to react against rather than copy:

> *The loan-approval model approves `under_35` applicants at 19% against 44% for
> `35_and_over`. Pre-training DPL shows a 19-point gap already present in the training
> labels, so the model has inherited and then widened an existing disparity rather than
> created one. The likely harm is creditworthy younger applicants being refused, which
> produces no observable loss on our side and so will not surface in performance monitoring.
> I recommend a feature-attribution review of `employment_tenure_years` before the next
> release, owned by the modelling lead, and that the fairness thresholds for this model be
> set and signed off by the risk committee rather than by the modelling team.*

Notice what that report does **not** do: it does not claim the model is illegal, does not
assert a threshold, and does not prescribe the fix. It states the evidence and routes the
decision to whoever is accountable for it. That is what a good finding looks like.

---

## Step 6 — Clean up

> ### IMPORTANT — SageMaker bills continuously
> **SageMaker notebook instances, Studio applications and spaces, and inference endpoints
> are charged for every hour they exist, whether or not you are using them.** They do
> **not** stop by themselves. An endpoint left running overnight, over a weekend or over a
> term break keeps accruing charges until you delete it. This is the single most common
> source of unexpected AWS bills in training accounts.

**If you completed Path 2 only, you created nothing and there is nothing to delete.** Read
Section 6.1 anyway — the failure modes it describes are exam-relevant and career-relevant.

### 6.1 Delete SageMaker resources (Path 1 only)

Go to the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/) and work
through the left navigation:

- [ ] **Endpoints** — delete every endpoint. **Delete the endpoint itself, not just the
      endpoint configuration** — deleting only the configuration leaves the endpoint running
      and billing. A Clarify job can strand a shadow endpoint if it failed midway, so check
      even if you never created one deliberately.
- [ ] **Endpoint configurations** — delete after the endpoints.
- [ ] **Models** — delete model entries created for this lab.
- [ ] **Processing jobs** — confirm the Clarify job shows **Completed**, **Stopped** or
      **Failed**, not **InProgress**. Stop any still running.
- [ ] **Notebook instances** — **Stop** first, then **Delete**. A stopped instance still
      incurs storage charges; a deleted one does not.
- [ ] **Studio apps and spaces** — shut down running apps, spaces and kernel sessions.
      **Closing the browser tab does not shut them down.**

Useful CLI checks:

```bash
aws sagemaker list-endpoints --region us-east-1
aws sagemaker list-notebook-instances --region us-east-1
aws sagemaker list-processing-jobs --status-equals InProgress --region us-east-1
```

### 6.2 Clear storage

- [ ] Delete Clarify output objects from your S3 output prefix if you no longer need the
      report.
- [ ] Remove any dataset you uploaded solely for this lab — particularly if it contained
      real personal data, which should not linger in a training account.

### 6.3 Check every Region you used

- [ ] Resources in another Region do not appear in your current view. If you switched
      Regions at any point, check **each** one.

### 6.4 Final confirmation

- [ ] Open **AWS Billing → Bills** or Cost Explorer the following day and confirm no
      unexpected SageMaker charges are accruing.

### 6.5 Keep your artefacts

Delete the AWS resources, but **keep your written answers from 5.2 and the issue report from
5.3**. Those are the deliverables that evidence the ability code.

---

## Verification

- [ ] You can state the facet, facet value, label and positive label value for the lab scenario without looking them up.
- [ ] You can explain, in your own words, the difference between **pre-training** and **post-training** bias metrics and why both are needed.
- [ ] You can name one pre-training metric that measures group representation and one that measures label disparity.
- [ ] You can describe the three post-training metric families and say which one identifies *who is harmed*.
- [ ] You can define **amplification** and explain why a single-phase analysis cannot detect it.
- [ ] Your written answers to all six questions in 5.2 are complete.
- [ ] Your issue report from 5.3 names the observation, the evidencing metric, the plausible harm and a concrete recommendation with an owner.
- [ ] You can explain why removing the sensitive column does not remove the bias.
- [ ] **Path 1 only:** the processing job is not InProgress, and no endpoint, notebook instance or Studio app was left running.

## Discussion questions

1. Your organisation does not collect ethnicity data, so it cannot measure ethnicity bias. Argue both sides: should it start collecting a sensitive attribute purely to test for discrimination against it? Which responsible-AI dimensions are in tension, and how would you decide?
2. A model shows near-zero post-training bias but a large pre-training DPL. A colleague says "the model is fine, the data is the problem, not our issue". Rebut this in three sentences.
3. For the lending scenario, would you rather reduce the false-negative gap or the false-positive gap, and what would you need to know about the product to answer properly? Now answer the same question for a cancer-screening model.
4. Adjusting the decision threshold separately for each group is technically the most direct fairness fix and is prohibited in many jurisdictions. Why would a law forbid a measure intended to improve fairness?
5. Who should own the decision about what fairness threshold is acceptable — the data scientist, the product owner, legal and compliance, or a governance board? Justify your answer, then say what each of the others should contribute.

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.
