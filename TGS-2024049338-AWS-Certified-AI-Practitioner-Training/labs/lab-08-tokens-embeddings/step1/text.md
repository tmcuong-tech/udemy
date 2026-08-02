# Step 1 — Tokens are not words

A foundation model does not read words. It reads **tokens** — the units its tokeniser splits text into. A token is roughly a common word or a fragment of one. Punctuation and spaces count too.

A widely used rule of thumb for English is that **one token is about four characters, or roughly ¾ of a word** — so 100 tokens is very approximately 75 English words. Treat this as an estimate only: the true count depends on the model's tokeniser, and it is different for every model family.

## Predict, then check

1. Open the Bedrock playground at <https://console.aws.amazon.com/bedrock/> and select a text model you enabled in Lab 06.
2. For each string below, **write down your guess** for the token count *before* you do anything else.

| # | Text | Words | Your guess (tokens) | Notes |
|---|---|---|---|---|
| 1 | `The cat sat on the mat.` | 6 | | short common words |
| 2 | `Amazon Bedrock` | 2 | | product name |
| 3 | `antidisestablishmentarianism` | 1 | | long rare word |
| 4 | `2024-04-17T09:30:00Z` | 1 | | timestamp |
| 5 | `你好世界` | — | | non-Latin script |
| 6 | `def f(x): return x**2 + 3*x - 7` | — | | code |

3. Now check. Many Bedrock playgrounds display token counts for the request and the response after a run — look for a token or usage indicator near the output. If your playground shows this, send each string as a prompt and read the count.

4. If no token count is displayed, reason it through instead. The pattern you should be able to predict:

   - **Common short words** are usually one token each. Row 1 is close to its word count.
   - **Rare or long words** are split into several fragments. Row 3 is one word but several tokens.
   - **Structured strings** — timestamps, IDs, URLs — fragment badly. Row 4 is one "word" but many tokens.
   - **Non-Latin scripts** typically consume **more tokens per character** than English, because the tokeniser was trained mostly on English text. Row 5 is short but not cheap.
   - **Code** fragments heavily on symbols and indentation.

## Why the mismatch matters

> **Two texts of the same word count can cost very different amounts.** A page of plain English prose and a page of JSON with long identifiers may differ by a factor of two or more in tokens — and therefore in price and in how much of the context window they consume.

This is why "tokens", not "words" or "characters", is the unit that appears on every foundation model pricing page.

**Checkpoint:** You can explain why one long word can be several tokens, and why a timestamp is more expensive than a short sentence.
