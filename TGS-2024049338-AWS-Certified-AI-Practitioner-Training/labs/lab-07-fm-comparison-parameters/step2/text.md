# Step 2 — Run the identical prompt on a second model

1. **Clear the conversation**, or start a new playground session. This matters: in a chat playground the previous exchange stays in context and will influence the next answer. You want a clean comparison, not a continuation.
2. Choose **Select model** again and switch to a model from a **different provider**.
3. Paste the **same prompt, completely unchanged**, and run it.
4. Record the same four observations as the second row of your comparison table.
5. *(Optional, if a third model is available to you)* Repeat with a third model and fill the third row.

Now compare your rows and answer these in writing:

- Which answer would you actually put in front of a paying customer, and **why**?
- Did the models disagree about *what a foundation model is*, or only about *how to say it*? A difference in style is a preference. A difference in substance is a correctness problem.
- Did any model ignore an explicit instruction in the prompt (the word limit, the no-jargon rule)? **Instruction-following is itself a model capability that varies between models** — it is not guaranteed just because you asked clearly.

> **The exam point:** model choice is a real engineering decision with trade-offs across quality, instruction-following, latency and cost per token. Bedrock's single API is what makes switching models cheap — your application code changes a model ID, not an integration.

**A fair comparison requires:**

| Hold constant | Vary |
|---|---|
| The prompt text, word for word | The model |
| The inference parameters | |
| An empty conversation history | |

If you change two things at once, you learn nothing from the result. This is the same discipline you will apply in Steps 3–5, where the model is held constant and the parameters vary.

**Checkpoint:** At least two rows in the comparison table, from two different providers, for one identical prompt, with a written difference noted between them.
