# Well done!

You have completed Lab 07 — Comparing Foundation Models and Inference Parameters:

✅ Set up the comparison and run the first model
✅ Run the identical prompt on a second model
✅ Baseline at low temperature
✅ Raise temperature, then narrow top-P
✅ Max tokens truncates, it does not shorten
✅ Clean up

**Key takeaways:**

- Different foundation models answer the same prompt differently because of training data, model size and instruction tuning. Model choice is an engineering decision, not a preference.
- A fair comparison changes **one thing at a time** — hold the prompt, the parameters and the conversation history constant.
- **Temperature** reshapes the next-token probability distribution: low is closer to deterministic, high is more varied. Even at temperature 0, output is not guaranteed to be perfectly reproducible.
- **Top-P** truncates the candidate tokens to the smallest set whose probabilities sum to P; **top-K** does the same with a fixed count. Tune one control, not all of them.
- **Max tokens truncates generation — it does not instruct the model to be brief.** For a genuinely shorter, complete answer, ask for brevity **in the prompt**; use max tokens as a cost and latency ceiling.
- Low temperature and top-P suit factual and structured tasks; higher values suit brainstorming and creative work.

**Next:** Lab 08 — Tokens, Embeddings and Vector Representations
