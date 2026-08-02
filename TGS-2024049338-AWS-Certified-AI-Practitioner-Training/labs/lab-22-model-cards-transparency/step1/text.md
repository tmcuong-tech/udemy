# Step 1 — Create a model card and declare intended use

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
