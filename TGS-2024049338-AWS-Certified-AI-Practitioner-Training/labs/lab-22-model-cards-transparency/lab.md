# Lab 22 — Model Cards and Transparency

Create a SageMaker model card and complete each section, then distinguish model cards from Model Monitor and the Model Registry and examine AWS AI Service Cards.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 4 — Guidelines for Responsible AI (14%)
**Task statement:** 4.2 Recognize the importance of transparent and explainable models
**WSQ mapping:** LU3 · Topic 6 Responsible AI Practices · K8 · A3 · LO3
**Slide reference:** v11 deck slides 285–297
**Estimated time:** 30 minutes

**Learning objectives:**
- Create a SageMaker model card and complete intended use, out-of-scope uses, owner and review date
- Assign a risk rating based on consequence and autonomy, and justify it with evidence
- Record training provenance, time period, population coverage and known data gaps
- Record evaluation results disaggregated by facet group, together with caveats, failure modes and oversight mechanisms
- Distinguish model cards from the SageMaker Model Registry and Model Monitor and explain how the three interlock
- Explain what AWS AI Service Cards provide and what limitations you inherit from a managed AI service

**Prerequisites:**
- Labs 20 and 21 completed — this lab documents the same loan-approval scenario and reuses their findings.
- An AWS account with console access and permission to create and delete SageMaker model cards. **No model, dataset or compute is required** — a model card can be created standalone.

> **Note on cost:** Model cards are metadata and cost essentially nothing. However, SageMaker Studio apps and spaces, notebook instances, inference endpoints and Model Monitor schedules all bill continuously once started. This lab does not quote prices — check the current AWS pricing pages for your Region. Follow the Clean up step without exception; it also sweeps for anything left behind by Labs 19 to 21.

---

## Step 1 — Create a model card and declare intended use

Labs 19 to 21 produced controls, measurements and explanations. A model card is where all of
it becomes **documentation someone else can rely on**. It is the **transparency** artefact of
responsible AI, and the thing an auditor asks for first.

Amazon SageMaker Model Cards give you a structured, versioned place to record what a model
is for, how it was built, how it performs, and what it must not be used for.

### 1.1 Create the model card

1. Go to the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/).
2. In the left navigation, look under the governance section and choose **Model cards**.
3. Choose **Create model card**.
4. **Name:** `aif-lab22-loan-approval-card`
5. Optionally associate an existing model. **This is not required** — a model card can be
   created standalone, which is what makes this lab completable without provisioning
   anything.

> **Cost note:** Model cards themselves are metadata and do not run compute. If you attach a
> model or open Studio to reach the console, see the Clean up step — Studio apps and any
> endpoint bill continuously.

### 1.2 Declare the intended use

Complete the intended-use section. For the loan-approval model from Labs 20 and 21:

**Intended use.** Assist credit officers in triaging consumer personal-loan applications by
producing an approval-likelihood score. The score is a **recommendation input to a human
decision**, not an automated decision.

That last clause is doing real work. It sets the **controllability** posture, and everything
downstream — the appeal process, the level of explainability required, the risk rating —
follows from whether a human decides or the model does.

**Intended users.** Credit officers in the consumer lending team, and model risk reviewers.
Not customer-facing staff, and not the customer directly.

### 1.3 Declare what is out of scope — the part people skip

This section is more valuable than the intended-use section, and it is routinely left empty.

State explicitly that this model **must not** be used for:

- Fully automated approval or refusal without human review
- Commercial or business lending — it was trained on consumer applications only
- Pricing, interest-rate setting or credit-limit assignment — it predicts approval, not risk
  of loss, and those are different targets
- Any population materially different from the training population
- Marketing, prospecting or eligibility pre-screening

Every model gets reused. It gets reused by someone who was not in the room when it was built,
for a purpose that seems adjacent, under time pressure. The out-of-scope list is the only
control you have over that, and it works only if it is specific. "Do not misuse this model"
prevents nothing. "This model must not set credit limits because it predicts approval, not
loss" prevents a specific, plausible, damaging mistake.

Write your out-of-scope list by asking: **what would a reasonable person, six months from
now, mistakenly assume this model can do?**

### 1.4 Add owner and version

Record:

- **Owner** — a named accountable person or team, not "Data Science"
- **Version** — the model version this card describes
- **Review date** — when this card must next be revisited
- **Status** — draft, pending review, or approved

An undated card with no owner is a card nobody maintains. The review date is what converts
the model card from a document into a **process**.

---

## Step 2 — Set the risk rating and record training details

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

---

## Step 3 — Record evaluation results and caveats

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

---

## Step 4 — Model cards versus Model Monitor versus Model Registry

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

---

## Step 5 — AWS AI Service Cards and the transparency you inherit

A model card documents a model **you** built. But most AI in most organisations is consumed
as a managed service — you did not train it, cannot inspect it, and have no access to its
training data. The transparency question does not disappear; it moves.

### 5.1 What an AI Service Card is

**AWS AI Service Cards** are AWS's published transparency documents for its own AI services.
They are the managed-service equivalent of a model card: AWS documents the service so that
you can make an informed decision about using it.

An AI Service Card typically covers:

- The **intended use cases** for the service, and uses AWS considers out of scope
- **Design choices** and how the service was built and tested
- **Performance considerations** and factors that affect accuracy
- **Best practices** for deploying the service responsibly, including where human review is
  recommended
- **Limitations** and known factors that degrade performance

You can find the published AI Service Cards through the responsible AI pages on
[aws.amazon.com](https://aws.amazon.com/). Do not assume every service has one — check which
services are covered rather than asserting it.

### 5.2 Why this matters to you as a consumer of the service

When you build on a managed AI service, you inherit its properties and remain accountable
for the outcome. The service card is your primary evidence about a component you cannot
inspect.

| You cannot | So the service card is how you |
|---|---|
| Inspect the training data | Learn what population it was built for |
| Run your own bias analysis on the model internals | Learn what testing AWS performed and what it found |
| Change the model | Learn what AWS recommends as a mitigating control |
| Explain a specific decision from the weights | Learn the accuracy factors that plausibly affected it |

> **The accountability does not transfer.** If you deploy a managed service in a decision
> that affects people, *you* are accountable for that decision — not AWS. The service card
> tells you what AWS knows; deciding whether that is sufficient for your use case is your
> responsibility, and documenting that decision is your governance obligation.

### 5.3 The composition problem

Your model card must document the **system**, not just any model you personally trained.

If your application is a managed AI service plus a foundation model plus a guardrail plus
some business logic, then:

- The managed service's limitations are your limitations
- The foundation model's caveats are your caveats
- Your guardrail (Lab 19) is a documented control that belongs in the card
- The **combination** may have failure modes none of the parts do individually

Record in your card **which components you built and which you consumed**, and cite the AI
Service Card or model provider documentation for each consumed component. A card that
documents only the thin layer you wrote is technically accurate and practically misleading.

### 5.4 Complete the exercise

Write a short additional section for `aif-lab22-loan-approval-card`:

1. **Component inventory.** Suppose the loan system also uses a managed document-analysis
   service to extract fields from uploaded payslips. List the components, and for each state
   whether you built or consumed it.
2. **Inherited limitations.** For the consumed extraction component, what would you need
   from its service card before you would rely on it in a High risk decision? Name three
   specific things.
3. **Composition failure.** Describe one failure mode that arises only from the combination
   — for example, extraction accuracy varying by document quality, feeding a model that has
   no way to know a field was uncertain. What control would you add?
4. **The honest sentence.** Write one sentence for the card stating what you do *not* know
   about the components you consumed. This sentence is the difference between a transparency
   document and a marketing document.

---

## Step 6 — Clean up

> ### IMPORTANT — SageMaker bills continuously
> **SageMaker notebook instances, Studio applications and spaces, and inference endpoints
> are charged for every hour they exist, whether or not you are using them.** They do
> **not** stop by themselves. Model cards themselves are metadata and cost essentially
> nothing — but if you opened Studio to reach the console, or attached a model with a live
> endpoint, those are billing right now.

### 6.1 Delete the model card

1. Go to the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/).
2. In the left navigation, under the governance section, choose **Model cards**.
3. Select `aif-lab22-loan-approval-card`.
4. Choose **Delete** and confirm.

Or from the CLI:

```bash
aws sagemaker list-model-cards --region us-east-1
aws sagemaker delete-model-card --model-card-name aif-lab22-loan-approval-card --region us-east-1
```

> **In production you would not do this.** A model card is a governance record with an audit
> trail, and deleting it destroys the evidence of what was known and decided. You are
> deleting it here only because this is a training account.

### 6.2 Shut down anything that bills

Check the left navigation and clear:

- [ ] **Studio apps and spaces** — shut down running apps, spaces and kernel sessions.
      **Closing the browser tab does not shut them down.** This is the most likely charge
      from this lab.
- [ ] **Endpoints** — delete any endpoint. **Delete the endpoint itself, not just the
      endpoint configuration.**
- [ ] **Notebook instances** — **Stop** first, then **Delete**.
- [ ] **Model Monitor schedules** — if you created a monitoring schedule while exploring
      Step 4, delete it. Monitoring schedules run processing jobs on compute repeatedly and
      will bill indefinitely.
- [ ] **Models** — delete any model entry created for this lab.

Useful CLI checks:

```bash
aws sagemaker list-apps --region us-east-1
aws sagemaker list-endpoints --region us-east-1
aws sagemaker list-monitoring-schedules --region us-east-1
```

### 6.3 Domain 4 sweep

This is the last lab in Domain 4. Confirm nothing survives from Labs 19 to 21:

- [ ] Lab 19 — `aif-lab19-guardrail` deleted from the Bedrock console.
- [ ] Lab 20 — no Clarify processing job InProgress, no stranded shadow endpoint.
- [ ] Lab 21 — no explainability job InProgress, no online-explainability endpoint.
- [ ] Any S3 objects from Clarify outputs or uploaded datasets removed.

### 6.4 Check every Region and confirm billing

- [ ] Resources in another Region do not appear in your current view. If you switched
      Regions at any point, check **each** one.
- [ ] Open **AWS Billing → Bills** or Cost Explorer the following day and confirm no
      unexpected SageMaker or Bedrock charges are accruing.

### 6.5 Keep your artefacts

Delete the AWS resources, but **keep your completed model card content** — the intended use
and out-of-scope list from Step 1, the risk rating justification from Step 2, the
disaggregated evaluation and caveats from Step 3, and the composition exercise from Step 5.

Across Domain 4 you have produced a guardrail findings table, a bias issue report, a
plain-language decision explanation and a model card. That set is a defensible
responsible-AI posture for one system — and it is the evidence that you can identify and
report issues with AI applications and their data.

---

## Verification

- [ ] A model card named `aif-lab22-loan-approval-card` was created.
- [ ] The intended-use section states the purpose **and** whether a human or the model makes the final decision.
- [ ] The out-of-scope section lists at least four specific uses the model must not be put to, each with a reason.
- [ ] A risk rating is assigned **with a written justification** that cites evidence, not just a dropdown value.
- [ ] Training details record data source, time period, population covered and known gaps including the class imbalance.
- [ ] Evaluation results are recorded **disaggregated by facet group**, not as a single headline figure.
- [ ] The fairness metrics chosen are recorded together with *why* they were chosen.
- [ ] Explainability findings from Lab 21 are recorded together with the **baseline** used.
- [ ] Caveats cover known limitations, failure modes, human oversight and appeal, and recommendations.
- [ ] Owner, version and review date are recorded.
- [ ] You can state the one-line distinction between Model Cards, Model Registry and Model Monitor, and say which of the three bills continuously.
- [ ] You completed the component inventory and composition exercise in 5.4.
- [ ] The model card is deleted and no Studio app, endpoint, notebook instance or monitoring schedule was left running.
- [ ] The Domain 4 sweep in 6.3 confirms nothing survives from Labs 19 to 21.

## Discussion questions

1. Who is the real audience for a model card — engineers, auditors, or the affected customer? Does one document genuinely serve all three, and if not, what is the second document and who writes it?
2. Your out-of-scope section says the model must not set credit limits. A product team does it anyway because "it was already there and it works". What would have prevented this — and is documentation ever sufficient on its own?
3. A model card records a limitation that was known and accepted at release. Harm later occurs through exactly that limitation. Does the card protect the organisation, indict it, or both? Argue it.
4. Model Monitor detects that feature-attribution has drifted since training. Which specific sections of the model card are now potentially false, and what should the review process do next?
5. You build on a managed AI service whose service card discloses accuracy varies by input quality, but gives no per-group breakdown. You need this for a High risk decision. What are your options, and which do you take?
6. Across Labs 19 to 22 you have used guardrails, bias metrics, feature attribution and model cards. Map each of the nine responsible-AI dimensions — fairness, explainability, robustness, privacy and security, transparency, veracity, governance, safety, controllability — to the lab and control that addresses it. Which dimension is served weakest by this toolset, and what would you add?

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.
