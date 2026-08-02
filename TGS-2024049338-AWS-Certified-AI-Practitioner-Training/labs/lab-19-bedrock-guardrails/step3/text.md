# Step 3 — Configure denied topics

Denied topics block subject matter that is perfectly legal and entirely non-toxic, but is
off-limits for *your* application. This is the **business-policy** layer, and it is the
policy group most often missed in the exam and in practice.

A request for investment advice is not hateful, violent or criminal — no content filter
will stop it. But if you are a retail bank without a licence to give personalised financial
advice, letting your chatbot answer is a regulatory incident.

### 3.1 Add the first denied topic

1. Choose **Add denied topic**.
2. **Name:** `Financial Advice`
3. **Definition:**
   `Any request for personalised investment, trading, tax, or financial planning recommendations, including buy/sell/hold guidance on specific securities.`
4. **Sample phrases** — add two or three. These help the classifier calibrate:
   - `Should I put my CPF savings into tech stocks?`
   - `What shares should I buy this month?`
5. Choose **Confirm**.

### 3.2 Add a second denied topic of your own

Add one more that fits a scenario you care about. Suggestions:

| Name | Definition sketch |
|---|---|
| `Medical Diagnosis` | Requests to diagnose a condition or recommend treatment or dosage for an individual. |
| `Legal Advice` | Requests for a legal opinion or a recommendation on a specific dispute or contract. |
| `Employment Decisions` | Requests to evaluate, rank or recommend hiring, promotion or termination of a named individual. |

Write the definition yourself before reading the sketch — the drafting is the exercise.

### 3.3 Write definitions in terms of intent, not keywords

This is the single most important craft point in the whole guardrail.

**Weak definition:** `Blocks anything mentioning stocks, shares, bonds, crypto, CPF or ETFs.`

That is a word list wearing a costume. It fails twice over:

- It **over-blocks** — "Explain in general terms what a bond is" is education, not advice,
  and a keyword definition refuses it.
- It **under-blocks** — "Where should I park my retirement money for the next ten years?"
  contains none of those words and sails straight through.

**Strong definition:** describes the *intent* — a request for a personalised recommendation
that the user would act on financially. That generalises to phrasings you never listed.

> **Teaching point:** If your denied-topic definition would work equally well pasted into
> the word-filter box, you have written it wrong. Denied topics exist precisely because
> word filters cannot capture intent.

Choose **Next**.
