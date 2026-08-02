# Step 4 — Model cards versus Model Monitor versus Model Registry

These three are routinely confused, and the exam exploits that. They are not alternatives —
they answer different questions and a mature practice runs all three.

### 4.1 The distinction

| | **Model Cards** | **Model Registry** | **Model Monitor** |
|---|---|---|---|
| Question answered | *What is this model, and what was decided about it?* | *Which model versions exist, and which is approved for deployment?* | *Is the deployed model still behaving as expected?* |
| Nature | Documentation and judgement | Version catalogue and approval workflow | Continuous runtime observation |
| Time frame | Point in time, revised on review | Lifecycle of versions | Ongoing |
| Contains | Intended use, risk rating, training details, evaluation, caveats | Model packages, versions, approval status, lineage | Drift, data quality, bias drift and feature-attribution drift alerts |
| Written by | Humans making judgements | The pipeline, plus a human approver | The system, automatically |
| Cost profile | Metadata — negligible | Metadata — negligible | **Runs scheduled monitoring jobs on compute — billable** |

### 4.2 The one-line summary worth memorising

- **Model Registry** — *which* model.
- **Model Card** — *why* this model, and what we knew and decided.
- **Model Monitor** — *is it still working*.

### 4.3 How they connect

The three close a loop, and the loop is the actual governance system:

1. A model version is registered in the **Model Registry** and awaits approval.
2. A **Model Card** documents intended use, risk, evaluation and caveats. A reviewer reads
   it and approves — or does not.
3. The approved version deploys. **Model Monitor** watches for data drift, quality
   degradation, **bias drift** and **feature-attribution drift**.
4. Monitor raises an alert: attribution has shifted, and a feature that was minor at training
   time now dominates.
5. That alert invalidates a claim in the **Model Card**. The card is revised, or the model is
   retrained and a new version enters the Registry.

Note step 5 specifically. **Model Monitor is what stops a model card from becoming a lie
over time.** A card is accurate on the day it is written; the world moves; without monitoring
nobody notices that the documented behaviour and the actual behaviour have separated.

Note also that Model Monitor extends the fairness and explainability work of Labs 20 and 21
into production. Bias measured once at training time is a snapshot. **Bias drift** and
**feature-attribution drift** monitoring is the same measurement, continuously.

### 4.4 Check yourself

Answer without looking at the table:

1. A regulator asks which model version was serving traffic on a given date. Which of the
   three answers this?
2. A reviewer asks why a High risk rating was assigned. Which one?
3. Production input data has shifted so that a feature now falls outside its training range.
   Which one detects this?
4. A new team wants to reuse the model for business lending. Which one tells them not to?
5. Which of the three costs money to run continuously, and why?

*(Answers: 1 — Registry, for version and lineage. 2 — Model Card. 3 — Model Monitor. 4 —
Model Card, via the out-of-scope section. 5 — Model Monitor, because it runs scheduled
processing jobs on compute; the other two store metadata.)*
