# Step 5 — Performance versus interpretability, and when to reject the better model

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
