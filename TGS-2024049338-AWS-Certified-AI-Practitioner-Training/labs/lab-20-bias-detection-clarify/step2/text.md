# Step 2 — Pre-training bias metrics: measuring the data

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
