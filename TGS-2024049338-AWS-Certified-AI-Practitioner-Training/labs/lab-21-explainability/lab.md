# Lab 21 — Explainability and Feature Attribution

Use SHAP feature attribution in SageMaker Clarify to produce global and local explanations, then decide when a regulated use case requires an interpretable model instead.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 4 — Guidelines for Responsible AI (14%)
**Task statement:** 4.2 Recognize the importance of transparent and explainable models
**WSQ mapping:** LU3 · Topic 6 Responsible AI Practices · K8 · A3 · LO3
**Slide reference:** v11 deck slides 285–297
**Estimated time:** 35 minutes

**Learning objectives:**
- Distinguish global from local explanations and match each to its audience and purpose
- Explain SHAP feature attribution, including why contributions are signed and additive
- Explain why the SHAP baseline determines what an explanation means, and why it must be documented
- Configure a SageMaker Clarify explainability analysis, or interpret one without running it
- Translate a local attribution table into a plain-language reason a person can act on
- Argue when a more accurate but less interpretable model should be rejected in a regulated use case

**Prerequisites:**
- Lab 20 completed — this lab continues the same loan-approval scenario and depends on its bias findings.
- An AWS account with console access. **Path 2 requires no AWS resources at all.**
- For Path 1 only: an existing trained SageMaker model, a tabular dataset in Amazon S3, and permission to run SageMaker processing jobs.

> **Note on cost:** Path 2 is free. **Path 1 starts billable compute** — a processing job plus a temporary inference endpoint that Clarify calls once per SHAP sample per row, which is more inference traffic than a bias job. SageMaker endpoints, notebook instances and Studio apps bill continuously until deleted. This lab does not quote prices — check the current AWS pricing pages for your Region. Follow the Clean up step without exception.

---

## Step 1 — Global versus local explanations

Lab 20 told you *whether* the model treats groups differently. It did not tell you *why*.
Explainability is the discipline of answering "why did the model produce this output?" — and
the answer has two entirely different shapes depending on who is asking.

### 1.1 The two scopes

| | **Global** explanation | **Local** explanation |
|---|---|---|
| Question | Which features drive this model's behaviour overall? | Why did the model decide *this* case *this* way? |
| Scope | The whole dataset or population | One row, one prediction, one person |
| Typical audience | Model developers, validators, governance boards | The affected individual, a caseworker, an appeals process |
| Typical use | Debugging, feature review, detecting proxies | Contesting a decision, explaining a refusal |

Both are computed from feature attributions. They differ in whether you aggregate across all
predictions or inspect a single one.

### 1.2 Why the distinction is not academic

Consider the loan model from Lab 20.

**Global finding:** across the whole population, `employment_tenure_years` is the largest
single driver of the model's decisions. This is what you take to a feature review — it tells
you where to look for proxies, and it is the finding that connects explainability back to
fairness. If a feature that correlates strongly with age dominates the model, you now have a
concrete, testable hypothesis for the disparity Lab 20 measured.

**Local finding:** for applicant #4417, the largest contributors to the refusal were a short
employment tenure and a high requested-amount-to-income ratio. This is what a person can
actually act on or contest. A global explanation is useless to them — "on average this model
weights tenure heavily" does not tell anyone why *they* were refused.

> **Key point:** an organisation that computes only global explanations has satisfied its
> engineers and given the affected customer nothing. An organisation that computes only
> local explanations can answer every complaint individually while never noticing a
> systematic proxy. **Governance needs both.**

### 1.3 The regulatory angle

Where a "right to an explanation" or a right to contest an automated decision exists in law,
what is being demanded is almost always the **local** explanation — a reason specific to that
person's case, in language they can understand and challenge.

Note the second half of that requirement. A local explanation expressed as a vector of
signed floating-point contributions across forty features is technically an explanation and
practically useless to the recipient. Translating attributions into a small number of
plain-language reasons is a design problem, and it is where most explainability programmes
actually fail — not in the mathematics.

### 1.4 Note what explainability is not

Explainability is not the same as:

- **Transparency** — disclosing that a system is AI, what it is for, and how it was built.
  You can be fully transparent about an unexplainable model. (Lab 22.)
- **Interpretability** — a property of the *model itself* being directly readable. Covered
  in Step 5, where the distinction turns out to matter a great deal.
- **Veracity** — whether the output is *correct*. A confidently wrong prediction can be
  explained beautifully. The explanation tells you why the model said it, not whether it
  was right.

---

## Step 2 — SHAP feature attribution and the baseline

SageMaker Clarify implements explainability using **SHAP** (SHapley Additive exPlanations),
a feature-attribution method that assigns each input feature a signed contribution to a
prediction.

### 2.1 The core idea

SHAP originates in cooperative game theory. Treat the prediction as a payout and the
features as players who cooperated to produce it. SHAP distributes the payout among the
features according to how much each one contributed.

Two properties follow, and they are what make SHAP useful:

- **Signed.** A feature can push a prediction *up* or *down*. "Short employment tenure
  contributed −0.14 to the approval score" is more informative than "tenure was important".
  Methods that report only importance magnitude lose the direction.
- **Additive.** The contributions sum back to the difference between this prediction and the
  baseline. Nothing is unexplained, and the attributions form a complete account.

Aggregate the absolute attributions across many rows and you get a **global** explanation.
Inspect one row and you get a **local** one. Same computation, different scope — this is why
SHAP is the default choice for tooling that must serve both audiences.

### 2.2 The baseline is the part everyone gets wrong

SHAP attributions are always measured **relative to a baseline**. The question SHAP actually
answers is not "why did the model predict this?" but:

> "Why did the model predict *this* rather than what it would have predicted for the
> **baseline** input?"

Change the baseline and every attribution changes. The baseline is not a technical detail —
it defines the counterfactual, and therefore defines what the explanation *means*.

| Baseline choice | The explanation then means |
|---|---|
| Dataset average or median row | Why this applicant differs from a typical applicant |
| A specific reference cohort | Why this applicant differs from that cohort |
| All-zeros or "no information" row | Why this applicant differs from a meaningless input — usually the wrong choice |

**A poorly chosen baseline produces confident, well-formatted, misleading explanations.**
This is worse than no explanation, because it survives review.

Concretely: explain a refusal against an average-applicant baseline and you learn what made
this person weaker than average. Explain it against a baseline of *approved* applicants and
you learn what would have needed to change for approval. Those are different questions and
different answers, from the same model and the same row.

> **Governance point:** the baseline must be **documented alongside the explanation**. An
> attribution figure quoted without its baseline is uninterpretable, and it will be quoted
> without its baseline unless you make that impossible.

### 2.3 The other configuration parameters

| Parameter | What it controls |
|---|---|
| **Number of samples** | SHAP values for complex models are approximated by sampling. More samples give more stable attributions and cost more compute. |
| **Baseline rows** | One row or a set. A set generally gives a more robust reference than a single hand-picked row. |
| **Aggregation** | How per-row attributions are combined into the global view — typically mean absolute contribution. |

Instability is a real failure mode. If you run the analysis twice with too few samples and
get materially different attributions, the explanation is noise. Check for this before you
brief anyone on the results.

### 2.4 The honest limitations

SHAP is the best widely available tool for this job, which is not the same as being
reliable in all conditions. Know these before you present SHAP output as truth:

- **Correlated features split credit unpredictably.** If `income` and `employment_tenure`
  move together, the attribution divided between them depends on the algorithm's internals,
  not on which one the model "really" used. Do not read a small difference between two
  correlated features as meaningful.
- **Attribution is not causation.** SHAP tells you what the *model* used. It says nothing
  about what causes the real-world outcome. A model can rely heavily on a feature that has
  no causal relationship to default risk at all.
- **It is post-hoc.** SHAP explains a model it did not build and cannot inspect the true
  reasoning of. This is the crux of Step 5.

---

## Step 3 — Configure a Clarify explainability analysis

Clarify computes explainability in the same processing-job framework as bias analysis. As in
Lab 20, there are two paths.

> ### COST WARNING — Path 1 starts billable compute
> An explainability job **requires model predictions**, so Clarify deploys your model to a
> temporary (shadow) endpoint and calls it many times — once per SHAP sample per row. This
> is more inference traffic than a bias job. The processing instances and the endpoint both
> bill for their duration, and a failed job can strand the endpoint, which then **bills
> continuously until deleted**. Do not start Path 1 unless you will complete Step 6.

### 3.1 Path 1 — run it against your own model

1. Go to the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/).
2. Open SageMaker Studio, or the Clarify/processing entry point in your console version.
3. Create a Clarify processing job with an **explainability** configuration:

**Data configuration**
- Input dataset S3 URI, format and header row
- Output S3 prefix for the analysis and report
- The label column, and which feature columns to analyse

**Model configuration**
- The model to explain, plus instance type and count for the shadow endpoint
- How to read the model's output — which field carries the score or probability

**SHAP configuration**
- **Baseline** — one row or a set of rows representing your chosen reference. Decide this
  deliberately using Step 2.2, and write down *why* you chose it.
- **Number of samples** — more samples, more stable attributions, more cost
- Whether to emit **global** aggregated attributions, **local** per-row attributions, or both

**Job resources**
- Processing instance type and count

4. Run the job and wait for completion.
5. Collect the outputs from your S3 prefix — the analysis JSON containing attribution values
   and the generated report.

Then go **straight to Step 6** and verify nothing is left running.

### 3.2 Path 2 — no resources required

Skip the job. Steps 4 and 5 are written to be completed entirely from the illustrative
report in Step 4, and they carry the learning outcome on their own.

### 3.3 Two things worth noticing about the configuration

**Bias and explainability share a job type.** That is not an accident of packaging. The
workflow is: measure the disparity (Lab 20), then explain what produces it (this lab). A
fairness finding without an attribution analysis tells you a problem exists but gives you
nothing to act on. An attribution analysis without a fairness finding tells you what the
model uses but not whether that matters to anyone.

**Explainability can also be run online.** Clarify supports attaching explainability to a
real-time endpoint so individual predictions carry their attributions with them. That is the
architecture you need when a caseworker must explain a decision at the moment it is made,
rather than in a batch report a month later — and it is what makes a contestability process
operationally possible.

Note the cost consequence: online explainability means the attribution computation runs on
every explained request, adding latency and inference cost per call. Whether every prediction
needs an explanation, or only contested ones, is a design decision with a real bill attached.

---

## Step 4 — Read and interpret a feature attribution report

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

---

## Step 5 — Performance versus interpretability, and when to reject the better model

This step is a structured decision exercise. No AWS resources are required.

### 5.1 The trade-off

Broadly, model families trade predictive power against how directly a human can read their
reasoning:

| Model family | Interpretability | Typical performance on tabular data |
|---|---|---|
| Linear / logistic regression | Read the coefficients directly | Lower |
| Small decision tree | Follow the path to the leaf | Lower |
| Gradient-boosted ensemble | Not directly readable | Higher |
| Deep neural network | Not directly readable | Higher on unstructured data |
| Foundation model | Not directly readable at all | Highest on language tasks |

The trade-off is a tendency, not a law. Sometimes a well-specified linear model matches an
ensemble, and you should always check before assuming you must give up interpretability.

### 5.2 Interpretable versus explainable — the distinction that matters

| | **Interpretable** model | **Explainable** (post-hoc) model |
|---|---|---|
| What it is | The model's structure *is* the explanation | A second method approximates why the first model behaved as it did |
| Fidelity | Exact, by construction | An approximation, with error |
| Can it be wrong? | No — it is the model | **Yes.** The explanation can be a plausible story about a model that decided for other reasons |
| Example | Logistic regression coefficients | SHAP over a gradient-boosted ensemble |

**A post-hoc explanation is not equivalent to an inherently interpretable model.** SHAP over
a black box is a *model of a model*. It is a good one, and it is still an approximation with
its own assumptions, its own baseline dependence, and its own failure modes on correlated
features. When you tell a customer "you were refused because of your employment tenure", an
interpretable model lets you assert that as fact. A post-hoc explanation lets you assert it
as your best current estimate — and if challenged in a tribunal, that distinction is the
entire case.

### 5.3 The scenario

A gradient-boosted ensemble outperforms logistic regression on the loan dataset by a
meaningful margin. Its decisions cannot be read off the model. SHAP can approximate an
explanation after the fact.

Decide, in writing:

**(a)** Is the post-hoc explanation equivalent to an inherently interpretable model? Use
5.2 and give your own reasoning, not the table's.

**(b)** In which situations should the more accurate but less interpretable model be
**rejected outright**? Work through:

- **Regulated decisions.** Credit, insurance, employment, housing, healthcare. Where a
  regulator can demand the basis of a specific decision, "our approximation method suggests"
  may not meet the standard.
- **The right to an explanation.** If the person is legally entitled to reasons, can you
  give reasons you would defend under challenge?
- **Contestability.** Can the person meaningfully dispute the decision? A dispute process
  built on an approximation invites the response "your explanation is wrong" — and you may
  have no way to prove otherwise.
- **Consequence severity.** A 2% accuracy gain on a product recommendation is worth having.
  A 2% gain on a decision that denies someone housing is a different calculation entirely.

**(c)** Who should own this decision — the data scientist, the product owner, legal and
compliance, or a governance board? Name the owner, then say what each of the others must
contribute for the owner to decide well.

### 5.4 The framing that resolves most cases

Ask: **what is the cost of being unable to explain a single decision, multiplied by how
often you will be asked?**

- A film recommender: near zero cost per unexplained decision, asked essentially never.
  Take the accuracy.
- A loan refusal: material cost per unexplained decision — regulatory exposure, a complaint,
  possible litigation — and you will be asked regularly. The interpretable model may be
  cheaper overall even though it predicts worse.

Framed this way, interpretability stops being a nice-to-have that engineering trades away
and becomes a quantifiable operational requirement. That is the framing that survives
contact with a product manager who wants the extra 2%.

### 5.5 Three positions worth considering

1. **The hybrid.** Use the accurate model to triage and an interpretable model, or a human,
   for cases with adverse outcomes. You keep the accuracy where it is harmless and the
   explainability where it is required.
2. **The constrained model.** Use a model family that is more powerful than linear
   regression but still structurally readable — monotonic constraints, small rule sets,
   generalised additive models. The trade-off is often less severe than assumed.
3. **The honest refusal.** Sometimes the correct answer is that no model should make this
   decision unaided. Narrowing scope so the model recommends and a human decides is a
   legitimate engineering conclusion, not a failure.

Write down which of the three you would propose for the loan model, and what you would need
to be true to change your mind.

---

## Step 6 — Clean up

> ### IMPORTANT — SageMaker bills continuously
> **SageMaker notebook instances, Studio applications and spaces, and inference endpoints
> are charged for every hour they exist, whether or not you are using them.** They do
> **not** stop by themselves. An explainability job deploys a shadow endpoint to obtain
> predictions; if the job failed midway that endpoint can be left running and will keep
> billing until you delete it.

**If you took Path 2 only, you created nothing and there is nothing to delete.** Read 6.1
anyway — the failure modes are exam-relevant.

### 6.1 Delete SageMaker resources (Path 1 only)

Go to the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker/) and work
through the left navigation:

- [ ] **Endpoints** — delete every endpoint. **Delete the endpoint itself, not just the
      endpoint configuration.** Check the list even if you never deliberately created one:
      the Clarify shadow endpoint appears here.
- [ ] **Endpoint configurations** — delete after the endpoints.
- [ ] **Models** — delete model entries created for this lab.
- [ ] **Processing jobs** — confirm the explainability job shows **Completed**, **Stopped**
      or **Failed**, not **InProgress**. Stop any still running.
- [ ] **Notebook instances** — **Stop** first, then **Delete**. A stopped instance still
      incurs storage charges; a deleted one does not.
- [ ] **Studio apps and spaces** — shut down running apps, spaces and kernel sessions.
      **Closing the browser tab does not shut them down.**
- [ ] **Online explainability** — if you attached explainability to a real-time endpoint in
      3.3, that endpoint is billing continuously. Delete it.

Useful CLI checks:

```bash
aws sagemaker list-endpoints --region us-east-1
aws sagemaker list-processing-jobs --status-equals InProgress --region us-east-1
aws sagemaker list-apps --region us-east-1
```

### 6.2 Clear storage

- [ ] Delete Clarify explainability outputs from your S3 prefix if you no longer need them.
- [ ] Remove any dataset uploaded solely for this lab.

### 6.3 Check every Region you used

- [ ] Resources in another Region do not appear in your current view. If you switched
      Regions at any point, check **each** one.

### 6.4 Final confirmation

- [ ] Open **AWS Billing → Bills** or Cost Explorer the following day and confirm no
      unexpected SageMaker charges are accruing.

### 6.5 Keep your artefacts

Keep your written answers from 4.1, 4.2 and 5.3 — especially the plain-language refusal
reason from question 4. That single sentence is the whole point of explainability, and you
will reuse this material when you complete the caveats and limitations sections of the model
card in Lab 22.

---

## Verification

- [ ] You can state the difference between a **global** and a **local** explanation and name the audience each serves.
- [ ] You can explain why SHAP contributions are **signed** and what is lost by reporting importance magnitude alone.
- [ ] You can explain in one sentence why changing the **baseline** changes every attribution.
- [ ] You can name two honest limitations of SHAP — correlated features and attribution-is-not-causation.
- [ ] Your written answers to questions 1–3 in 4.1 are complete.
- [ ] Your written answers to questions 4–6 in 4.2 are complete, including the two-sentence plain-language refusal reason.
- [ ] You can state the distinction between an **interpretable** model and an **explainable** one, and why a post-hoc explanation can be wrong.
- [ ] You have chosen and justified one of the three positions in 5.5 for the loan model.
- [ ] You can explain why explainability alone does not resolve whether a proxy feature is acceptable.
- [ ] **Path 1 only:** no endpoint, processing job, notebook instance or Studio app was left running.

## Discussion questions

1. Is a post-hoc explanation of a complex model equivalent to an inherently interpretable model? Answer as if you were being cross-examined about a specific customer's refusal.
2. Your local explanation says a refusal was driven by employment tenure. The applicant says this is age discrimination. Using your Lab 20 bias findings and your Lab 21 attributions together, how would you investigate — and what evidence would make you conclude the feature must be removed?
3. Your team computes global explanations for the governance board and nothing else. Name the specific failures this creates, and the ones it does not — global explanations are not worthless, so be precise.
4. A colleague quotes "employment tenure contributes 0.31" in a slide with no baseline stated. What is wrong with the claim, and what process change would prevent it recurring?
5. Under what circumstances is "no model should make this decision unaided" the correct engineering recommendation? Who in your organisation is empowered to make that call, and what happens if nobody is?

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.
