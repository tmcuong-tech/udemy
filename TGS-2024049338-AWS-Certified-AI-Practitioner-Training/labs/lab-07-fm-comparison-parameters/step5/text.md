# Step 5 — Max tokens: truncation is not brevity

This step exists because it is one of the most commonly misunderstood parameters, and it appears on the exam.

1. Stay on the same model. Set **temperature** back to a middle value.
2. Set the **maximum response length** (*Max tokens* / *Maximum length*) to a **small** value — small enough that a normal answer could not possibly fit.
3. Run a prompt that would naturally produce a long answer:

   ```
   Describe in detail how a small retail business in Singapore could use
   generative AI across marketing, customer service and inventory.
   ```

4. Read what comes back. **The response stops mid-sentence.** It is not a shorter, well-formed answer — it is a full answer with the end cut off.
5. Record this in the parameter observation table.

## Why this matters

**Max tokens is a hard stop applied to generation. It is not an instruction to the model.**

The model does not see the max tokens value and decide to be concise. It begins writing the answer it was always going to write, and generation is halted the moment the limit is reached. The result is truncated, not summarised.

| If you want... | Do this | Not this |
|---|---|---|
| A genuinely shorter, complete answer | Say so **in the prompt** — "in no more than 50 words", "answer in one sentence" | Lower max tokens |
| A hard ceiling on cost and latency per call | Set **max tokens** | Rely on the prompt alone |

In production you usually do both: the prompt asks for brevity, and max tokens is a **safety ceiling** so a misbehaving generation cannot run away with your token bill or block your request timeout.

6. **Prove it to yourself.** Reset max tokens to a generous value, then run this instead:

   ```
   Describe in detail how a small retail business in Singapore could use
   generative AI across marketing, customer service and inventory.
   Answer in no more than 40 words.
   ```

   This time the answer is **short and complete** — it has an ending. That is the difference between instructing the model and cutting it off.

7. Reset the maximum length to a reasonable value before finishing.

## Where the parameters live in a real call

These are not console-only settings. When an application invokes a model, the same values are sent in the request body — the exact field names vary by model provider, which is one more reason Bedrock's unified API is useful.

**Checkpoint:** You have seen a response truncated mid-sentence, and you can explain why that is not the same as asking the model to be concise.
