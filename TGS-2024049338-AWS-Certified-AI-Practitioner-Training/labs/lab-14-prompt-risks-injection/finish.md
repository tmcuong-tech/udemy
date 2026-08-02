# Well done!

You have completed Lab 14 — Prompt Misuse, Injection and Defences:

✅ The application you own, and its threat model
✅ The four risk classes
✅ Probe your own application
✅ Defence layers 1 and 2 — prompt hardening and input validation
✅ Defence layers 3 and 4 — output filtering and Guardrails
✅ Clean up

**Key takeaways:**

- A foundation model has **no separation between its instruction channel and its data channel**. System prompt, retrieved documents and user message all arrive as one token sequence. This is the root cause of prompt injection, and there is no prompt wording that fully solves it.
- **Prompt injection** subverts your application's instructions. **Jailbreaking** subverts the model's own safety alignment. **Prompt leaking** discloses your instructions. **Poisoning** corrupts the source data. **Hijacking** repurposes your paid application. Defending one does not defend the others.
- **Indirect injection** — malicious text arriving inside retrieved content the user never sees — is the more serious risk, because it lets one author influence someone else's session. Attaching a knowledge base makes every document part of your attack surface.
- Assume the system prompt is **eventually public**. Never place a credential, key or genuine secret in it. Removing the asset beats protecting it.
- Prompt hardening — delimiting untrusted input, restating instructions after it, and giving an explicit escape route — measurably reduces risk but is **probabilistic**, and results vary between runs of the same input.
- **Input validation and output filtering run in your code and are deterministic.** Schema validation and enumerated value checks are the enforcement that a prompt can only steer towards.
- **Never execute or trust model output downstream.** In many real incidents the model was the courier, not the victim.
- **Amazon Bedrock Guardrails** is a managed, model-independent layer applied at invocation, offering content filters, denied topics, word filters, sensitive information filters and contextual grounding checks. Because it sits outside the prompt it cannot be talked out of its instructions. Covered in depth in Lab 19.
- **Architecture beats wording.** Least privilege and a human in the loop for irreversible actions limit blast radius no matter how well an injection is crafted.

**Next:** Lab 15 — RAG with Knowledge Bases for Amazon Bedrock
