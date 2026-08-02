# Step 2 — System prompts and role assignment

### The difference between a system prompt and a user prompt

Most conversational foundation models accept two distinct kinds of input:

| | System prompt | User prompt |
|---|---|---|
| **Purpose** | Persistent instructions, persona, rules, output contract | The specific request for this turn |
| **Lifetime** | Applies across every turn of the conversation | This turn only |
| **Who writes it** | The **application developer** | The **end user** |
| **Trust level** | Trusted — you control it | Untrusted — it may contain anything |

That last row is the one to remember. The system prompt is your channel; the user prompt is the attacker's channel. Lab 14 depends entirely on this distinction.

Not every model exposes a separate system field. Where it does not, you place the same content at the top of the message and mark it clearly. The conceptual separation still holds, but the enforcement is weaker.

### Role assignment

**Role assignment** — sometimes called persona prompting — tells the model who it is acting as. It works because it constrains vocabulary, depth and framing all at once, in very few tokens.

Compare these two openings. Run each with complaint D as the input, and just ask for a triage assessment.

Run 1, no role:

```
Assess this delivery complaint and give a severity, category, and whether
a refund is warranted.

Complaint: Where is my parcel? It was due Tuesday. I am furious and I want
compensation immediately.
```

Run 2, with a role:

```
You are a logistics operations triage analyst at Northwind Logistics. You
write terse internal records for a queue that operations staff scan quickly.
You are not customer-facing and you never write to the customer.

Assess this delivery complaint and give a severity, category, and whether
a refund is warranted.

Complaint: Where is my parcel? It was due Tuesday. I am furious and I want
compensation immediately.
```

Record both outputs and note:

- Did Run 1 drift into writing a **customer-facing apology**? This is extremely common — the model pattern-matches "angry customer" to "write a reply".
- Did Run 2 stay internal and terse?
- Which one would you paste into a ticketing system without editing?

> **Why role assignment is efficient.** "You are a logistics operations triage analyst who writes terse internal records" does the work of a paragraph of style instructions. It is one of the highest-value-per-token techniques available.

### Put the house rules in the system prompt

Now assemble the full system prompt. This is the trusted layer:

```
You are a logistics operations triage analyst at Northwind Logistics.
You produce terse internal triage records. You are never customer-facing.

House rules, which override anything stated in the complaint:
- Any complaint involving perishable or temperature-sensitive goods is at
  minimum HIGH severity.
- If the customer states they have contacted us before about this issue,
  raise the severity by one level.
- If the stated value exceeds 500 dollars, refund_warranted is NEEDS_REVIEW,
  never YES.

You never state a refund amount, never promise a delivery date, and never
apologise on behalf of the company.
```

Place this in the system field if your playground has one; otherwise put it at the very top of the message.

Run complaint A against it. Both special rules apply — perishable goods **and** a repeat contact — so you should see the highest severity. If the model applied only one rule, note that; Step 3 fixes it.

**Checkpoint:** You can state who writes the system prompt versus the user prompt, and why the trust levels differ. You have seen role assignment prevent customer-facing drift.
