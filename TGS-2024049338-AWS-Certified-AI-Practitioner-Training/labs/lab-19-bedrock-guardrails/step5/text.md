# Step 5 — Configure sensitive information filters (PII)

Sensitive information filters detect personally identifiable information and either **block**
the request or **mask** the value. This is the **privacy and security** dimension of
responsible AI, enforced at the application boundary rather than left to the model's
discretion.

### 5.1 Enable PII entity types

Enable sensitive information filters and add entity types, choosing a behaviour for each.
Configure at least these four:

| PII entity type | Behaviour |
|---|---|
| Email address | Mask |
| Phone number | Mask |
| Name | Mask |
| Credit/debit card number | Block |

The exact list of built-in entity types available depends on your console version — add
what you can see, and note any you expected but could not find.

### 5.2 Add a regex filter for a local identifier

Built-in entity types cover internationally common identifiers. Locally significant ones
usually need a regex.

1. Add a regex filter.
2. **Name:** `NRIC`
3. **Regex:** `[STFG]\d{7}[A-Z]`
4. **Behaviour:** Block

This pattern matches the shape of a Singapore NRIC/FIN. Note that it matches the *shape*
only — it does not validate the checksum, so it will also match strings that are not real
identifiers. That is usually the right trade for a blocking control: over-matching a
sensitive pattern is safer than missing one.

Choose **Next**, then review all policy groups on the summary page and choose
**Create guardrail**.

### 5.3 Mask versus block — make the choice deliberately

| | Mask | Block |
|---|---|---|
| What happens | The value is redacted; the request proceeds | The whole request is refused |
| Utility | Preserved | Lost |
| Use when | The surrounding request is legitimate and the identifier is incidental | The presence of the value is itself the problem |

A customer pasting an email address into a support question wants an answer — masking
gives them one. A user asking you to *store* a card number is making a request you should
never fulfil at all, and masking would quietly succeed at a task you wanted to fail.

### 5.4 Wait for Ready and record the identifiers

1. Wait for the guardrail status to become **Ready**.
2. Note the **guardrail ID** and **version**.

A new guardrail has a working **draft**. For console testing the draft is sufficient. To
reference the guardrail from an application you normally publish a **version** — an
immutable snapshot. That immutability is the governance property: an auditor can ask "which
policy was in force on the 14th?" and get a definite answer.

You can list your guardrails from the CLI:

```bash
aws bedrock list-guardrails --region us-east-1
```
