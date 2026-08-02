# Step 5 — Defence layers 3 and 4: output filtering and Guardrails

Layers 1 and 2 tried to stop bad input reaching the model. Layers 3 and 4 assume that sometimes it will, and catch the consequences.

## Layer 3 — Output filtering and schema validation

This is the most under-appreciated control on the list, and often the most effective. **Never let model output reach a downstream system unvalidated.**

For the triage application, your code should enforce:

1. **Schema validation.** Parse the response as JSON. If it does not parse, or lacks exactly the expected keys, reject it. Do not attempt to repair it.
2. **Enumerated value checks.** `severity` must be exactly `LOW`, `MEDIUM` or `HIGH`. `refund_warranted` must be exactly `YES`, `NO` or `NEEDS_REVIEW`. Anything else is rejected. **This is the enforcement that the prompt could only ever steer toward** — the point made in Lab 13, now made concrete.
3. **Content scanning.** Check the summary field for things that must never appear: currency amounts, dates, the string `NWL-TRIAGE-CONFIG`, or fragments of your system prompt. Any hit is an incident to log, not just a value to strip.
4. **A defined failure mode.** On rejection, do you retry once, fail closed to human review, or return a generic error? Decide deliberately. **Failing closed to human review is the right default for a decision that affects a customer.**
5. **Never execute model output.** Do not pass it to a shell, an eval, a SQL string or an HTTP request without treating it as fully untrusted. This is where indirect injection turns into a real breach: the model was merely the courier.

Test it: take the worst output any probe produced and confirm your rules would have rejected it.

## Layer 4 — Amazon Bedrock Guardrails

Guardrails is a **managed, model-independent** control that evaluates input and output against policies you configure. Because it sits outside the prompt, it is not subject to being talked out of its instructions.

To see what it offers:

1. In the Bedrock console left navigation, choose **Guardrails**.
2. Create a guardrail, or open an existing one, and step through the configuration to see the available policy types. Depending on what is offered in your Region, you will typically find:
   - **Content filters** — configurable strength thresholds across harmful content categories, applied to prompts and to responses.
   - **Denied topics** — topics you define in natural language that the application must not engage with. For the triage app, "refund amounts" and "delivery date commitments" are natural candidates.
   - **Word filters** — including profanity and your own custom word or phrase lists.
   - **Sensitive information filters** — detection of PII, with the option to block or mask, plus custom patterns via regular expression. This is how you stop a customer's phone number flowing into your triage record.
   - **Contextual grounding checks** — assessment of whether a response is grounded in the provided source material and relevant to the query. This is directly aimed at hallucination and at responses driven by injected content rather than by real source data, which makes it especially relevant to Labs 15 and 16.
3. Use the guardrail **test window** in the console to evaluate a prompt and a response against your policy without wiring it into an application.
4. Note that a guardrail is applied by referencing it when you invoke a model, so one guardrail can be shared across many applications and models.

Check the Guardrails page for the policy types and options available in your Region — capabilities differ, and the console is the source of truth.

> **Guardrails is covered in depth in Lab 19.** Here, place it correctly: it is your **outermost, model-independent** layer, and it is the only control in this lab that applies uniformly no matter which model you invoke or how the prompt is worded.

## Layer 5 — Architecture and least privilege

The controls that matter most are often not about text at all.

- **Least privilege.** If the model-driven component can only read the ticket table and write a severity field, a successful injection cannot delete customers. Scope the IAM role of the component that acts on model output to the narrowest permissions that work. Covered in Lab 23.
- **Human in the loop for consequential actions.** Auto-closing a ticket is reversible. Issuing a refund is not. Route irreversible actions through a person.
- **Never put secrets in prompts.** Probe 3 demonstrated why. Use a secrets manager and inject values in code, never into model context.
- **Log and monitor.** Log every flagged input, every schema rejection and every guardrail intervention. A rising rate of interventions is your early warning that someone is working on your application.
- **Treat retrieved content as untrusted.** Every document in a knowledge base is attacker-controllable if anyone but you can write to the source bucket. Apply the same delimiting and validation to retrieved chunks as to user input.

### Final defence table

| Layer | Control | Deterministic? | Stops direct injection | Stops indirect injection | Stops leaking |
|---|---|---|---|---|---|
| 1 | Prompt hardening | No | Partly | Partly | Partly |
| 2 | Input validation | Yes | Partly | Partly | No |
| 3 | Output filter / schema | Yes | Limits impact | Limits impact | Yes, for known strings |
| 4 | Guardrails | Yes | Limits impact | Limits impact | Partly |
| 5 | Least privilege / HITL | Yes | Limits impact | Limits impact | No |

Read the table's real lesson: **no row is "yes" everywhere.** Security here comes from combination, and the deterministic layers are the ones you can actually promise a compliance team.

**Checkpoint:** You have inspected the Guardrails policy types in the console, defined schema and enumerated-value rules for your output, and can explain why Guardrails is not subject to prompt injection in the way prompt hardening is.
