# Step 3 — Post-training bias metrics: measuring the model

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
