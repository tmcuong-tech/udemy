# Step 2 — Tokens drive cost and the context window

Tokens are the unit of account for two separate constraints. The exam expects you to keep them distinct.

## 1. Cost

On-demand foundation model usage is billed **per token processed**, and **input tokens and output tokens are priced separately** — output is typically the more expensive of the two.

So the cost of a single call is driven by:

- the length of your **prompt** (input tokens), including any system instructions, examples and retrieved documents you attached
- the length of the **answer** (output tokens)

Two consequences that catch teams out in production:

- A long system prompt or a big few-shot example block is paid for on **every single call**, forever.
- In a **chat** application, the whole conversation history is usually resent with each turn. Token cost per turn therefore **grows as the conversation gets longer** — a fifteenth message is far more expensive than the first.

> Do not quote per-token prices from memory or from older course material. Consult the official Amazon Bedrock pricing page for current rates, and note that they differ by model and by provider.

## 2. The context window

The **context window** is the maximum number of tokens a model can handle in one request — and it covers the **input and the output together**. It is a hard architectural limit of the model, not a setting you can raise.

This produces the classic failure: you paste a long document, the model has almost no room left to answer, and the response is cut off or the request is rejected outright.

| | Cost | Context window |
|---|---|---|
| What it is | Money per token processed | Hard token ceiling per request |
| Can you change it? | Only by using fewer tokens or a cheaper model | No — it is a property of the model |
| Symptom when ignored | A surprising bill | Truncated or rejected requests |

## Do the arithmetic

An internal assistant answers **20,000 questions per month**. Each call sends a 600-token system prompt, about 400 tokens of retrieved context, a 100-token user question, and produces a 300-token answer.

1. Input tokens per call: 600 + 400 + 100 = **1,100**
2. Output tokens per call: **300**
3. Input tokens per month: 1,100 × 20,000 = **22,000,000**
4. Output tokens per month: 300 × 20,000 = **6,000,000**

*(These figures are teaching data, not a measurement or a quote.)*

Now answer, without looking anything up:

- Which single change would cut the most tokens — shortening the system prompt, retrieving less context, or capping the answer length? Why?
- The team wants to add three few-shot examples to the system prompt, adding 500 tokens. What does that cost per month in input tokens?
- What does this tell you about why RAG systems are careful about **how many** chunks they retrieve, not just which ones?

## Strategies to control tokens

- Trim system prompts; every word is billed on every call
- Retrieve fewer, better-targeted chunks rather than more
- Truncate or summarise old conversation turns instead of resending everything
- Set **max tokens** as a ceiling on runaway output (Lab 07)
- Match the model to the task — a smaller, cheaper model is often sufficient for classification or extraction

**Checkpoint:** You can explain the difference between cost per token and the context window, and name two ways to reduce token usage.
