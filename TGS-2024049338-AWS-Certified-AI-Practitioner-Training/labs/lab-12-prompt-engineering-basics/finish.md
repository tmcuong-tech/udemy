# Well done!

You have completed Lab 12 — Prompt Engineering Basics — Zero-Shot and Few-Shot:

✅ Set up the playground and fix one task
✅ The anatomy of a prompt
✅ Zero-shot prompting
✅ One-shot and few-shot prompting
✅ Compare, and find where more examples stop helping
✅ Clean up

**Key takeaways:**

- A prompt has four components — **instructions, context, input data, output indicator**. The output indicator is the one most often missing, and it causes most format failures.
- **Zero-shot** supplies no examples; **one-shot** supplies exactly one; **few-shot** supplies several. The count is of task examples, not instructions.
- Few-shot prompting is **in-context learning** — the examples ride in the context window on every call. Model weights are unchanged, nothing persists between calls, and you pay tokens for the examples every time.
- Structuring a prompt usually yields a **larger** quality gain than adding examples. Examples then buy format consistency and predictable handling of edge cases.
- More examples are not monotonically better. Past the point where format and edge cases are stable, extra examples add cost, latency and possible label bias.
- Prompt engineering is the **lowest rung** on the customisation ladder: prompt engineering → RAG → fine-tuning → continued pre-training. Exam questions asking for the lowest-cost sufficient approach usually want the lowest rung that solves the stated problem.
- Bedrock on-demand inference is **serverless** — no standing resource, billed on tokens processed.

**Next:** Lab 13 — Advanced Prompting and Prompt Templates
