# Step 1 — Global versus local explanations

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
