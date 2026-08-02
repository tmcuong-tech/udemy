# Well done!

You have completed Lab 13 — Advanced Prompting and Prompt Templates:

✅ Set up and define the scenario
✅ System prompts and role assignment
✅ Chain-of-thought prompting
✅ Negative prompting and constraints
✅ Build a reusable prompt template
✅ Test the template against edge cases
✅ Clean up

**Key takeaways:**

- The **system prompt** carries persistent instructions written by the application developer and is trusted. The **user prompt** carries this turn's request, may contain anything, and is untrusted. Everything in Lab 14 rests on this boundary.
- **Role assignment** constrains vocabulary, depth and framing in very few tokens — one of the highest value-per-token techniques available.
- **Chain-of-thought** improves accuracy on multi-step and multi-rule tasks because intermediate reasoning becomes context the final answer is conditioned on. It costs extra output tokens and latency, and the reasoning it produces is **not a verified audit trail**.
- **Negative prompting is weaker than positive instruction.** Saying "do not mention X" raises the salience of X. Replace each negative with a positive that occupies the same space, ideally an enumerated value set or a fixed literal.
- Prompt instructions are **steering, not enforcement**. Anything that must never happen needs a control outside the prompt: schema validation, output filtering, or Amazon Bedrock Guardrails.
- A **prompt template** with named placeholders gives you versioning, a clean trust boundary, and testability. Wrap untrusted input in an explicit delimiter so the model can tell your instructions from text that merely looks like instructions.
- Prompt changes are **not local**. Tightening one rule can loosen another, so maintain a golden set of test inputs and re-run all of it on every change.

**Next:** Lab 14 — Prompt Misuse, Injection and Defences
