# Well done!

You have completed Lab 09 — Generative AI Capabilities and Limitations:

✅ Capabilities — summarisation and generation
✅ Capabilities — translation and code
✅ Produce a hallucination yourself and record it
✅ The other four limitations
✅ Mitigations — grounding, review and scoping
✅ Clean up

**Key takeaways:**

- Generative AI is strong at **summarisation, generation, translation, code, extraction and conversation**. The common thread: the source material is in the prompt, or there is no single correct answer, or the output is cheap to verify.
- **Hallucination** happens because fluency and accuracy come from the same next-token prediction process. A false answer looks exactly as confident as a true one, and the model has no internal signal that it is guessing.
- Prompting a model to admit ignorance reduces hallucination but **provides no guarantee** — you cannot build a factual guarantee out of a prompt instruction.
- **Non-determinism** breaks exact-match testing; **knowledge cutoff** means no recent events and no internal company data; **bias** reproduces patterns in training data; **cost and latency** rule out FMs where a rule or a query would do.
- **Grounding with RAG is the primary defence** against hallucination — it narrows the model's job from recalling a fact to reading a supplied passage. It does not fix bias, cost or latency, and it fails if retrieval fails.
- Match review to stakes: **AI drafts, a human approves**. Some decisions should not be automated at all.
- Guardrails sit outside the prompt, so unlike prompt instructions they cannot be talked out of by a user.

**Next:** Lab 10 — Choosing Bedrock, SageMaker JumpStart or a Managed Service
