# Step 2 — Capabilities: translation and code

## Capability 3 — Translation

```
Translate the customer reply you just wrote into Simplified Chinese and
into Malay. Keep the professional tone. Do not translate the phrase
"order number" — leave it in English.
```

Record whether the exception instruction was honoured. If you or a colleague read either language, judge the quality — and notice how hard it is to evaluate an output you cannot read. **"I cannot check this output" is a limitation of the deployment, not of the model**, and it applies to far more than translation.

## Capability 4 — Code

```
Write a Python function that takes a list of order dictionaries, each
with keys 'order_id', 'ordered_date' and 'delivered_date' (delivered_date
may be None), and returns the order IDs that are more than 7 days late.
Include a docstring and handle the None case.
```

Record whether the code is syntactically valid, whether it handles `None`, and whether it would actually run. Do not assume it works because it looks confident and well formatted. If you have `python3` available, paste it into a file and run it against a small test case.

## The honest summary of capabilities

Generative AI is strong at:

| Task family | Examples | Why it works |
|---|---|---|
| **Summarisation** | Emails, transcripts, documents, tickets | Source material is supplied |
| **Generation** | Drafts, replies, marketing copy, descriptions | No single correct answer required |
| **Translation** | Between languages, and between registers | Strong pattern task with the source supplied |
| **Code** | Boilerplate, tests, explanation, conversion | Highly structured, and easy to verify by running it |
| **Extraction and classification** | Pull fields from unstructured text, route tickets | Source supplied, output constrained |
| **Conversation** | Assistants, guided help | Tolerant of variation in phrasing |

**The common thread across the strong cases:** either the source material is in the prompt, or there is no single correct answer, or the output is cheap to verify.

**The common thread across the weak cases** — which you will meet in Step 3 — is the opposite: the model is asked to recall specific facts from training, and the output is expensive to verify.

**Checkpoint:** Your capability table has four rows, each with something imperfect noted.
