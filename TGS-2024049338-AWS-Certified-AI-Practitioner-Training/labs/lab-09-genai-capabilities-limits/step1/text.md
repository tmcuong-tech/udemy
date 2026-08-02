# Step 1 — Capabilities: summarisation and generation

This lab is deliberately balanced. The first two steps show you what generative AI does genuinely well. The next two make you find its failure modes yourself. You cannot advise a business on where to apply this technology if you have only seen one half.

Open the Bedrock playground at <https://console.aws.amazon.com/bedrock/> and select a text model you enabled in Lab 06. Keep the same model for the whole lab so your observations are comparable.

## Capability 1 — Summarisation

Summarisation is the most reliable and most commercially valuable capability, because the source material is supplied in the prompt. The model is condensing text you gave it, not recalling facts from training.

Paste this and run it:

```
Summarise the following customer email in two sentences, then state
the customer's requested action on a separate line.

"Hi, I ordered two office chairs on the 3rd and the confirmation said
delivery within five working days. It is now the 14th and nothing has
arrived. I called on Tuesday and was told the order was 'in the
warehouse' but nobody could tell me when it would ship. I have a new
staff member starting Monday with nowhere to sit. If they cannot arrive
before Monday I would rather cancel and buy elsewhere, but I would
prefer to keep the order if you can commit to a date."
```

Record: did it capture the deadline (Monday), the conditional nature of the request (keep **if** a date is committed, otherwise cancel), and did it invent any detail that was not in the email?

## Capability 2 — Generation

Now generate new text from a brief:

```
Write a reply to that customer. Apologise, commit to investigating,
and ask for their order number. Do not promise a delivery date.
Keep it under 100 words and use a professional but warm tone.
```

Record: did it follow **all four** constraints, including the negative one (do not promise a date)? Negative instructions are followed less reliably than positive ones — a genuinely useful thing to know before you put a model in front of customers.

## Record your results

| Capability | Task | Did it work? | What was imperfect? |
|---|---|---|---|
| Summarisation | Customer email | | |
| Generation | Reply drafting | | |
| Translation | *(Step 2)* | | |
| Code | *(Step 2)* | | |

> **The pattern to notice:** both tasks worked well because **the source material was in the prompt**. This is the single strongest predictor of whether a generative AI task will succeed. Hold on to it — it explains Step 3 and it explains why RAG exists.

**Checkpoint:** Two capability rows recorded, including at least one thing each task did imperfectly.
