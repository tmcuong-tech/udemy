# Step 5 — Retrieve and generate, and read the citations

Step 4 returned raw chunks. Now add the generation half: retrieve the chunks **and** have a model answer from them.

### Use the console test window

1. Open your knowledge base and use the test or chat panel.
2. Select a **text generation model** — this is a different model from the embedding model, and it is chosen per query, not baked into the knowledge base.
3. Turn on the option to **show source details** or **show citations** if it is not on by default.

Ask the question you asked in Step 1:

```
What is Northwind Logistics' maximum liability for a standard parcel with
no declared value?
```

You should now get the correct figure from `claims-policy.txt`, with a citation.

### Or use the CLI

```bash
aws bedrock-agent-runtime retrieve-and-generate \
  --input '{"text":"What is the maximum liability for a standard parcel with no declared value?"}' \
  --retrieve-and-generate-configuration '{
      "type": "KNOWLEDGE_BASE",
      "knowledgeBaseConfiguration": {
        "knowledgeBaseId": "<YOUR_KB_ID>",
        "modelArn": "arn:aws:bedrock:us-east-1::foundation-model/<MODEL_ID>"
      }
  }' \
  --region us-east-1
```

Substitute the model ID of a text model you have access to. Get exact IDs from the console model catalogue or from:

```bash
aws bedrock list-foundation-models --region us-east-1
```

Do not type a model version string from memory — providers publish multiple versions and they change.

### Read the citations properly

The response has two parts, and the second is the one people skip.

- **`output.text`** — the generated answer.
- **`citations`** — for each span of the answer, the retrieved references that support it, each with its chunk text and its S3 source location.

Do all three of these:

1. **Find the exact sentence** in the retrieved chunk that supports the answer. Confirm the answer is not adding anything the chunk does not say.
2. **Confirm the source document** is the one you expected.
3. **Check whether every claim in the answer is cited.** If the answer contains a statement no citation supports, the model has blended retrieved context with its own training knowledge — which is precisely the failure mode citations exist to expose.

> **Why citations matter for the exam.** They give **traceability**: a human can verify an answer against a source. This addresses transparency and explainability requirements (Domain 4) and it is a concrete, structural advantage of RAG over fine-tuning, where no equivalent trace exists.

### Ask three more questions

Run these and record the answer plus whether it was correctly cited:

```
1. Can I get express delivery to Malaysia?
2. My frozen shipment arrived warm and I am a Gold tier customer.
   What service credit and claims handling applies?
3. What is Northwind's policy on shipping lithium batteries by air freight?
```

**Question 1** is a negative fact. `shipping-policy.txt` says express is Singapore-only, so the correct answer is no. Watch for the model hedging or inventing a Malaysian express option. Retrieving a document that *implies* a negative is harder than retrieving one that states a positive.

**Question 2** spans three documents, as in Step 4. Check the citations: are all three files cited, or did the model answer partially from a subset and fill the rest in on its own?

**Question 3** is the important one. The documents say Northwind does not ship lithium batteries, but say **nothing about air freight specifically**. The correct behaviour is to state what the policy says and be explicit that air freight is not addressed. Watch for the model quietly extending the source into territory the source does not cover.

> **RAG reduces hallucination. It does not eliminate it.** The model can still misread a chunk, blend context with training data, or over-extend a partial match. This is exactly what **contextual grounding checks** in Amazon Bedrock Guardrails are designed to catch — see Lab 14 Step 5 and Lab 19.

### Record your results

| Question | Answer correct? | Cited? | Source document(s) | Notes |
|---|---|---|---|---|
| Max liability | | | | |
| 1 Express to Malaysia | | | | |
| 2 Gold tier perishable late | | | | |
| 3 Lithium batteries by air | | | | |

**Checkpoint:** Four questions answered with citations inspected, and you have identified at least one place where the answer went beyond what the retrieved chunks actually support — or verified that it did not.
