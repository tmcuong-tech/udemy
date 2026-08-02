# Well done!

You have completed Lab 10 — Choosing Bedrock, SageMaker JumpStart or a Managed Service:

✅ The three options and the question that separates them
✅ Option A — a managed AI service
✅ Option B — Bedrock, and Option C — SageMaker JumpStart
✅ Build the decision table
✅ Classify ten scenarios
✅ Clean up

**Key takeaways:**

- The three layers differ by **what you manage**: a managed AI service gives you a task-specific API and nothing to run; Bedrock gives you foundation models through one API with no infrastructure; SageMaker gives you the tools and the responsibility to host models yourself.
- **The most specific service that solves the problem is usually the right answer.** "A foundation model could do it" is not the same as "a foundation model should do it".
- Managed services return **structured, typed output with a confidence score**, deterministically, in milliseconds. Foundation models return free text with no confidence signal, in seconds.
- Use **Bedrock** when no fixed API exists for the task — free-form generation, custom categories defined at request time, house style, RAG over your own documents.
- Use **SageMaker** when you need a specific or your own model, control of the weights, or control of hosting. Custom **data** does not force SageMaker — custom **model weights** do.
- **Idle billing is the decisive practical difference.** Bedrock on-demand and managed services cost nothing when unused; a SageMaker endpoint bills per instance-hour until deleted, and only deleting the *endpoint* stops the charge.
- The layers combine. Real systems often chain Textract, Comprehend and Bedrock in one workflow.

**Next:** Lab 11 — Amazon Q Business Getting Started
