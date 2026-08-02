# Step 1 — Set up and measure a baseline

> ## ⚠️ Cost warning — the same one as Lab 15
>
> This lab uses a knowledge base backed by a **vector store**, normally an **Amazon OpenSearch Serverless collection**, which bills continuously by the hour from creation until deletion regardless of query volume. **Complete this lab in one sitting and do Step 6 in full.** Set an AWS Budgets alert before you begin, and check current rates on the official pricing pages.

### Get a knowledge base

**If you still have the Lab 15 knowledge base**, use it — that is the intended path and it saves both time and money.

**If you deleted it**, rebuild it now by following Lab 15 Steps 1, 3 and 4: create the S3 bucket, upload `shipping-policy.txt`, `claims-policy.txt` and `service-tiers.txt`, create a knowledge base with the **default** chunking strategy, and sync. Note the time you created the vector store.

Either way, re-fill the resource table from Lab 15 Step 3 — knowledge base ID, collection name, Region, bucket. It is your cleanup checklist and you will need it again.

### The premise of this lab

Lab 15 built a working RAG pipeline. This lab confronts the fact that **a working RAG pipeline can still give bad answers**, and that when it does, the model is usually not at fault.

Here is the causal chain, and each link can break independently:

```
Document  →  Chunk  →  Vector  →  Retrieved?  →  In context  →  Answer
```

If the correct chunk was never retrieved, **no amount of prompt engineering will produce a correct answer**. The model cannot use text it was never given. Diagnosing RAG failures therefore starts at retrieval, not at generation — and that is the single most useful habit this lab teaches.

### Build a test set

You cannot detect improvement without a fixed test set. Use these five questions, which probe different failure modes:

```
Q1. How long do I have to file a damage claim?
Q2. What is the maximum liability for a standard parcel with no declared value?
Q3. Can I get express delivery to Malaysia?
Q4. What happens if a Gold tier customer's perishable shipment arrives late?
Q5. How many shipments do I need for Gold tier, and what does Gold include?
```

| Question | Probes | Facts needed from |
|---|---|---|
| Q1 | Single clear fact | claims-policy |
| Q2 | Single fact, no keyword overlap with the query | claims-policy |
| Q3 | A negative fact — the answer is "no", stated indirectly | shipping-policy |
| Q4 | Multi-document synthesis | all three |
| Q5 | Two facts in one document, possibly split across chunks | service-tiers |

### Measure the baseline

For each question, run **retrieval only** — not retrieve-and-generate. Looking at raw chunks is the whole point.

```bash
aws bedrock-agent-runtime retrieve \
  --knowledge-base-id <YOUR_KB_ID> \
  --retrieval-query '{"text":"How long do I have to file a damage claim?"}' \
  --region us-east-1
```

For each question record:

- **Was the chunk containing the answer retrieved at all?** Yes or no. This is the only question that really matters.
- **At what rank?** First result, or fourth?
- **Was the chunk complete?** Did it contain the whole fact, or was the fact cut across a chunk boundary?
- **How much irrelevant text came back?**

| Q | Answer chunk retrieved? | Rank | Chunk complete? | Noise |
|---|---|---|---|---|
| Q1 | | | | |
| Q2 | | | | |
| Q3 | | | | |
| Q4 | | | | |
| Q5 | | | | |

Then run each question through retrieve-and-generate and note whether the final answer was correct.

**The key comparison:** for any question where the answer was wrong, check whether the right chunk was retrieved. If it was retrieved and the answer was still wrong, that is a **generation** problem. If it was not retrieved, that is a **retrieval** problem — and it is fixed by chunking, top-K or filtering, never by rewording the prompt.

**Checkpoint:** A knowledge base with default chunking, and a baseline table covering retrieval quality and answer correctness for all five questions.
