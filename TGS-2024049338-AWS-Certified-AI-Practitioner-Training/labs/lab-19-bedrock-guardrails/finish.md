# Well done!

You have completed Lab 19 — Amazon Bedrock Guardrails:

✅ Create the guardrail and set blocked messages
✅ Configure content filters
✅ Configure denied topics
✅ Configure word filters
✅ Configure sensitive information filters (PII)
✅ Test the guardrail and record findings
✅ Clean up

**Key takeaways:**

- A guardrail is a policy applied **on top of** a model, evaluated in **both directions** — on the incoming prompt and on the outgoing response.
- The four policy groups cover different failure modes: content filters are semantic harm controls, denied topics are business policy, word filters are literal matches, and sensitive-information filters are privacy controls.
- Denied topics must be written in terms of **intent**. A definition that reads like a word list duplicates the word filter and generalises poorly.
- **Mask** preserves utility by redacting a value; **block** refuses the request outright. Choose per entity type according to real risk.
- Every strength setting is a **false-positive versus false-negative** trade-off. There is no setting that eliminates both, so the choice must follow from the use case and be documented.
- Guardrails deliver **safety**, **privacy and security** and **controllability**. They deliver nothing on **fairness**, **explainability** or **veracity** — those need the tooling in the next three labs.

**Next:** Lab 20 — Bias Detection with SageMaker Clarify
