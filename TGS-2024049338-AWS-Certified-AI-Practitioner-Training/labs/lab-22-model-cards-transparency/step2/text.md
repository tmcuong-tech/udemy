# Step 2 — Set the risk rating and record training details

### 2.1 Assign a risk rating

SageMaker Model Cards include a **risk rating** field. Assign one and — more importantly —
record *why*.

A workable rubric, driven by consequence and autonomy rather than by model complexity:

| Rating | Typically when |
|---|---|
| **Low** | Errors are cheap and reversible; no decision about a person; a human reviews output routinely |
| **Medium** | Affects a person's experience but not their rights or access to a service; human oversight exists |
| **High** | Affects access to credit, employment, housing, healthcare, insurance or legal outcomes; regulated; errors are hard to reverse |

For the loan model, rate it **High** and justify:

> *Rated High. The model influences access to consumer credit, a regulated decision affecting
> the applicant's financial position. Lab 20 bias analysis found a disparity by age band that
> the model amplified relative to the training labels. A false negative — a creditworthy
> applicant refused — produces no observable loss to the institution and therefore will not
> be caught by performance monitoring alone. Human review is mandatory and is the primary
> mitigating control.*

Note what that justification does: it ties the rating to specific evidence from an earlier
analysis and names the mitigating control. A rating without a rationale is an opinion in a
dropdown.

> **Common error:** rating risk by *model sophistication*. A simple logistic regression
> deciding who gets a mortgage is high risk. A large deep-learning model recommending films
> is low risk. **Consequence and autonomy determine risk, not architecture.**

### 2.2 Record the training details

Complete the training section. Cover at minimum:

| Field | What to record | Why it matters |
|---|---|---|
| **Algorithm / architecture** | Model family and framework | Determines whether explanations are exact or post-hoc (Lab 21) |
| **Training data source** | Where the data came from and who owns it | Provenance — the basis of any later data-rights question |
| **Time period covered** | The date range of the training data | The most common silent failure: a model trained on pre-shock economic conditions |
| **Population covered** | Who is in the data and who is not | Defines the boundary beyond which predictions are unsupported |
| **Known gaps** | Under-represented groups, missing fields, exclusions | Directly connects to the Class Imbalance finding from Lab 20 |
| **Preprocessing** | Feature engineering, imputation, resampling, reweighting | A fairness intervention applied at this stage is invisible later unless recorded |
| **Hyperparameters** | Key settings | Reproducibility |

For the loan model, record explicitly:

> *Trained on 10,000 consumer personal-loan applications. Facet `applicant_age_band` is
> imbalanced at approximately 1:4 (`under_35` 2,000 rows, `35_and_over` 8,000 rows). This
> imbalance is a known gap and is expected to degrade performance for the `under_35` group.*
> *(Figures are illustrative teaching data carried over from Lab 20, not real measurements.)*

### 2.3 Provenance is a governance requirement, not bookkeeping

The training-data section answers questions you will be asked under pressure and cannot
reconstruct afterwards:

- **A data subject requests erasure.** Which models were trained on their data?
- **A data source is found to be improperly licensed.** Which models are affected?
- **Performance degrades.** Has the world moved away from the training period, or is
  something else wrong?
- **A regulator asks whether a protected attribute influenced the model.** Which features
  existed, and which were proxies for what?

None of these are answerable from the model artefact. They are answerable only from the
documentation, and only if it was written at the time.
