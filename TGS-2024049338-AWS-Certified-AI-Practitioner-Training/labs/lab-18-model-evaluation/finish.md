# Well done!

You have completed Lab 18 — Evaluating Foundation Model Performance:

✅ Why evaluate, and build a test set
✅ The automatic metrics
✅ Run an automatic evaluation job
✅ Interpret the results
✅ Human evaluation, benchmarks, and business metrics
✅ Clean up

**Key takeaways:**

- Generative output has no single right answer, so classification accuracy does not apply. Three families fill the gap: **automatic metrics**, **human evaluation** and **benchmarks**.
- **ROUGE** — summarisation, **recall**-oriented, n-gram and longest-common-subsequence overlap with the reference. **BLEU** — translation, **precision**-oriented, with a brevity penalty. This pairing is heavily examined.
- **BERTScore** uses embeddings, so it rewards correct paraphrase where ROUGE and BLEU punish it — but semantic similarity is still not correctness.
- **Perplexity** measures fluency, not task quality. **F1, precision and recall** apply when there is one right answer — so reframing a generative task as classification makes evaluation far stronger.
- **No automatic metric detects a hallucination.** A fabricated fact phrased like the reference scores well. Metrics measure similarity to a reference, and similarity is not truth.
- **Your results are only as good as your reference answers.** The job measures similarity to text you wrote, not quality.
- **Read reports per record, not by aggregate.** Expect to find at least one low score that is the metric's fault and one high score that came from verbatim copying.
- **Deltas are trustworthy; absolute scores are not.** Fix the dataset, metric and references, change one thing, and read the change.
- **Human evaluation** captures what matters but is slow and subjective. **Comparison between two outputs is more reliable than absolute rating.** Blind the raters, use multiple raters, measure agreement, and sample rather than enumerate.
- **LLM as a judge** sits between the two — cheap and capable of assessing relevance and grounding, but it is a model judging a model and needs validating against human ratings.
- **Benchmarks** — GLUE, SuperGLUE, MMLU, BIG-bench, HELM — are for shortlisting, not for judging your task. **HELM** is distinctive for evaluating across accuracy, robustness, fairness, bias, toxicity and efficiency rather than one number. Watch for contamination.
- **Business metrics justify the project**: user satisfaction, task completion, escalation and deflection rate, conversion, retention, cost per interaction. A metric improvement that moves none of these has delivered no value.
- **Model selection is a trade-off across quality, cost and latency** — not a search for the highest score.

**Next:** Lab 19 — Amazon Bedrock Guardrails
