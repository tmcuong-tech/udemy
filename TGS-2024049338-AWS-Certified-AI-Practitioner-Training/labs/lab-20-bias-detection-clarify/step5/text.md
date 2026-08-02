# Step 5 — Path 2: guided walkthrough of a bias report

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
