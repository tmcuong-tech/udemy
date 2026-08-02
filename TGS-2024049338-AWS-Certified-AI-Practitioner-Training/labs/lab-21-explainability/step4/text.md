# Step 4 — Read and interpret a feature attribution report

Work through this step whichever path you took. If you ran Path 1, read your own report
alongside the walkthrough.

### 4.1 The global report

Continuing the loan-approval model from Lab 20.

> ### These figures are illustrative teaching data
> The attribution values below were constructed for this lab. They are **not** real
> measurements and not drawn from any AWS or public dataset. They exist to make the
> reasoning concrete.

Global attributions, mean absolute SHAP contribution across the evaluation set, baseline =
dataset median row:

| Feature | Mean absolute contribution | Rank |
|---|---|---|
| `employment_tenure_years` | 0.31 | 1 |
| `debt_to_income_ratio` | 0.24 | 2 |
| `requested_amount` | 0.17 | 3 |
| `savings_balance` | 0.11 | 4 |
| `postal_district` | 0.09 | 5 |
| `existing_customer` | 0.05 | 6 |

**Read this and answer in writing:**

1. `employment_tenure_years` dominates. In Lab 20 you found `under_35` applicants were
   approved at 19% against 44%. State the hypothesis this attribution suggests, and describe
   the test you would run to confirm or reject it.
2. `postal_district` ranks fifth but is non-trivial. Postal district correlates with income,
   ethnicity and housing type in most cities. Is its presence in this model defensible? What
   would you need to know to decide?
3. Rank order tells you what the model *uses*, not what is *legitimate*. Name a feature that
   could rank first while being completely unacceptable, and explain why the ranking alone
   would never reveal that.

### 4.2 The local report

Applicant #4417, refused. Baseline = dataset median row. Contributions are signed, where
negative pushes toward refusal:

| Feature | Value | Contribution |
|---|---|---|
| `employment_tenure_years` | 0.8 | −0.29 |
| `debt_to_income_ratio` | 0.61 | −0.18 |
| `requested_amount` | high | −0.07 |
| `savings_balance` | moderate | +0.04 |
| `existing_customer` | yes | +0.06 |

**Answer in writing:**

4. Write the refusal reason you would actually send to applicant #4417. Plain language, no
   numbers, no feature names as they appear in the schema, two sentences maximum. This is
   harder than it looks, and it is the real deliverable of explainability.
5. The applicant replies: "What would I have to change to be approved?" Can you answer that
   from this table? What does the answer depend on — and specifically, what would you have
   needed to choose differently in Step 2.2 to answer it well?
6. Two features pushed *toward* approval and were outweighed. Should the explanation mention
   them? Argue both ways, then decide.

### 4.3 Connect it back to fairness

The chain you have now built across two labs:

1. **Lab 20 measured a disparity.** `under_35` applicants are approved far less often, and
   the model amplified a gap already present in the labels.
2. **Lab 21 located a candidate mechanism.** The dominant feature is employment tenure,
   which is mechanically correlated with age — a younger person has had less time to
   accumulate any tenure at all.
3. **The remaining question is not technical.** Is `employment_tenure_years` legitimately
   predictive of default risk, an unlawful proxy for age, or genuinely both at once?

Most real cases are "both". The feature carries real predictive signal *and* encodes a
protected characteristic. There is no computation that resolves this. It is decided by
domain experts, legal counsel and whoever is accountable for the model — informed by the
evidence you have just produced, and documented in the model card you will build in Lab 22.

> **This is the honest summary of explainability's role:** it does not make decisions
> defensible. It makes them *discussable* by the people who are accountable for them.
