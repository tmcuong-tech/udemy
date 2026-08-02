# Step 4 — The other four limitations

Hallucination gets the attention. These four cause just as much trouble in production.

## Non-determinism

You saw this in Lab 07. The same prompt can produce different answers on different runs.

**Test it:** run one factual question three times, clearing between runs.

```
In one sentence, what is the main risk of using generative AI for
regulatory compliance advice?
```

Record whether the three answers agree in **substance**, or only in **style**.

**Why it matters:** it breaks testing. You cannot assert an exact expected output, so quality assurance must check properties — did it stay on topic, did it avoid forbidden content, is the JSON valid — rather than exact strings. It also means a customer and your support agent can ask the identical question and get different answers.

## Knowledge cutoff

A model's training data ends at some point in time. It does not know about anything after that, and it has **no awareness that time has passed** since.

**Test it:** ask the model about a recent event you know about — something from the last few months.

```
What significant developments have there been in this field recently?
Be specific about dates.
```

Record: did it say it does not know, did it give stale information as though current, or did it confidently invent something recent? The last is the dangerous one — it is hallucination and knowledge cutoff compounding each other.

> Also note: the model does not know your **internal** information at all. Your prices, your policies, your customer records, yesterday's inventory — none of it is in the training data. This is a cutoff of a different kind, and it is the single most common reason a business assistant needs RAG.

## Bias

Training data reflects the world as it was written down, including its stereotypes and its gaps. Models reproduce these patterns.

**Test it:** run this and read the output critically.

```
Write three short profiles of a nurse, a construction worker and a
CEO. Include a name and one sentence about each person's background.
```

Record which genders, names and backgrounds the model chose, and what it assumed without being asked. Run it two or three times to see whether the pattern is consistent — a single run is an anecdote, a repeated pattern is a finding.

*(This is a teaching exercise, not a measurement of bias. A real assessment requires many samples and a defined metric — see Lab 20 on SageMaker Clarify.)*

**Why it matters:** if this shaped screening, lending, or pricing decisions, the pattern becomes a compliance and fairness problem at scale, and one that is hard to spot from any single output.

## Cost and latency

Generative AI is neither free nor fast, and both are easy to forget when the playground feels instantaneous.

- **Cost** is per token, input and output (Lab 08). At scale, per-request costs that look trivial become a material line item.
- **Latency** is measured in seconds, not milliseconds, and generally grows with output length. Streaming improves the *perceived* wait but not the total.

**The question this forces:** if a rule, a database lookup or a small classical model can do the job, it will usually be cheaper, faster, more consistent and easier to audit. **A foundation model is the right tool when the input is unstructured language and the output requires generation — not simply because it is available.**

## Limitations summary

| Limitation | What you observed | Business consequence |
|---|---|---|
| Hallucination | *(Step 3)* | |
| Non-determinism | | |
| Knowledge cutoff | | |
| Bias | | |
| Cost and latency | | |

**Checkpoint:** All five rows of the limitations table are filled in with your own observations.
