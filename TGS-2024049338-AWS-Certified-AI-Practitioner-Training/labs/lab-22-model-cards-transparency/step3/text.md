# Step 3 — Record evaluation results and caveats

### 3.1 Evaluation results — disaggregated, not headline

Complete the evaluation section. The rule that matters:

> **A single headline accuracy figure is not an evaluation. It is a summary that hides
> exactly the information a model card exists to surface.**

Record metrics **disaggregated by facet group**, using your Lab 20 analysis.

> *Figures below are illustrative teaching data carried over from Lab 20, not real
> measurements.*

| Group | Approval rate (labels) | Approval rate (model) | Notes |
|---|---|---|---|
| `under_35` | 22% | 19% | Under-represented in training data (2,000 rows) |
| `35_and_over` | 41% | 44% | 8,000 rows |
| Overall | — | — | Record your headline metric here, but never *only* here |

Also record:

- **Which fairness metrics you chose and why.** Not just the values. A card that reports DPL
  without saying why DPL was the right measure for this decision leaves the most contestable
  judgement undocumented.
- **The evaluation dataset** — its source, date and whether it shares any bias with the
  training set. An evaluation set drawn from the same biased history validates nothing.
- **Explainability findings from Lab 21** — the dominant features, and the **baseline** used.
  An attribution figure without its baseline is uninterpretable.

### 3.2 Caveats, limitations and recommendations

This is the section that determines whether the card is honest. Record:

**Known limitations**
- Degraded performance expected for `under_35` due to under-representation
- The model amplifies an age-band disparity present in the training labels
- `employment_tenure_years` is the dominant feature and is mechanically correlated with age;
  its status as legitimate predictor or unlawful proxy is **unresolved and under review**
- Trained on consumer applications only; behaviour on other populations is unknown

**Failure modes**
- False negatives — creditworthy applicants refused — produce **no observable loss** and will
  not surface in standard performance monitoring
- Performance will degrade if economic conditions diverge from the training period

**Human oversight and appeal**
- Every adverse recommendation is reviewed by a credit officer before communication
- The applicant can request the reasons for a decision and can contest it
- Local explanations are available per decision; see the baseline caveat above

**Recommendations**
- Re-run the Lab 20 bias analysis at each retrain, not only at initial release
- Resolve the `employment_tenure_years` proxy question before the next release, owned by the
  modelling lead
- Fairness thresholds to be set by the risk committee, not the modelling team

### 3.3 The test of an honest card

An unresolved limitation stated plainly is worth more than a polished card that omits it.

Ask yourself: **if this model caused harm and this card were read aloud in an inquiry, would
it look like an honest account or like a document written to look compliant?**

Cards fail that test in a predictable way. They record what was measured and quietly omit
what was found. Every limitation in 3.2 is uncomfortable; every one of them is what a
reviewer needs.

### 3.4 Who is the audience?

Consider three readers of the same card:

| Reader | Wants |
|---|---|
| **Engineer** | Architecture, hyperparameters, data schema, reproducibility |
| **Auditor / regulator** | Provenance, disaggregated evaluation, oversight mechanisms, sign-off, dates |
| **Affected customer** | Why was I refused, and what can I do about it |

One document does not genuinely serve all three. The engineer's detail is noise to the
customer; the customer's question is not answered by any aggregate statistic. In practice
the model card serves the first two, and the third is served by a **separate, plain-language
disclosure** built from the same underlying facts — the local explanation from Lab 21.

Recognising that is the mark of someone who has actually built one of these. Write down, in
one sentence, what your organisation would put in front of the customer.
