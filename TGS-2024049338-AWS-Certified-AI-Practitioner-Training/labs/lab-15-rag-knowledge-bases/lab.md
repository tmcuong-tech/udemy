# Lab 15 — RAG with Knowledge Bases for Amazon Bedrock

Build a retrieval augmented generation pipeline over your own documents with Knowledge Bases for Amazon Bedrock, read the citations, and prove the difference against an ungrounded model.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 3 — Applications of Foundation Models (28%)
**Task statement:** 3.1 Describe design considerations for applications that use foundation models
**WSQ mapping:** LU4 · Topic 8 Developing GenAI Solutions · K5 · A4 · LO4
**Slide reference:** v11 deck slides 184–209
**Estimated time:** 45 minutes

> ## ⚠️ COST WARNING — READ BEFORE STARTING
>
> This lab provisions a **vector store**, normally an **Amazon OpenSearch Serverless collection**. It bills continuously by the hour from the moment it is created until you delete it — **whether or not you ever query it**. Deleting the knowledge base does **not** reliably delete the collection underneath.
>
> **Complete this lab in one sitting and do Step 7 in full.** Set an AWS Budgets alert before you begin, and check current rates on the official Amazon OpenSearch Serverless and Amazon Bedrock pricing pages. In a shared classroom account, confirm with your trainer first.

**Learning objectives:**

- Describe the RAG ingestion pipeline — chunk, embed, index — and the query pipeline — embed, retrieve top-K, generate.
- Explain that RAG changes the prompt, not the model's weights.
- Create a knowledge base over an S3 data source, choose an embedding model, and sync it.
- Inspect raw retrieval separately from generation as a diagnostic habit.
- Use retrieve-and-generate and verify every claim in an answer against its citation.
- Compare a grounded answer against an ungrounded one and explain why confident fabrication is more dangerous than refusal.
- Delete a knowledge base **and** its underlying vector store, and verify the deletion.

---

## Step 1 — Cost warning, and prepare the S3 data source

## ⚠️ Read this before you create anything

**This is the most expensive lab in the course, and the only one that leaves behind a resource billing continuously by the hour.**

A knowledge base needs a **vector store**. If you let Bedrock create one for you, it will typically provision an **Amazon OpenSearch Serverless collection**. That collection bills on provisioned capacity units **from the moment it is created until you delete it** — continuously, around the clock, **whether or not you ever run a single query**. Deleting the knowledge base does **not** always delete the collection underneath it.

Four rules for this lab:

1. **Complete the lab in one sitting.** Do not create the knowledge base at the start of the day and clean up tomorrow.
2. **Do Step 7 — Clean up.** It is not optional here. It deletes the knowledge base **and** the vector store, and it verifies the deletion.
3. **Set a billing alert before you begin** if you have not already. AWS Budgets can notify you on a threshold. Do this now.
4. **Check current pricing yourself** on the official Amazon OpenSearch Serverless and Amazon Bedrock pricing pages before creating anything. Do not rely on any figure quoted from memory or from older course material.

If you are working in a shared classroom account, confirm with your trainer before creating a knowledge base. If time is short, read this lab through and run the walkthrough steps without provisioning — Steps 2, 6 and 7 still teach most of the content.

Lab 16 extends this same knowledge base. If you intend to do Lab 16 immediately afterwards, you may keep the knowledge base between the two labs — but **only** if you will finish both today.

---

## Create the data source

RAG needs documents. You will create three small text files describing a fictional company so that the model cannot possibly answer from its training data — which is exactly what makes the demonstration honest.

### Create the S3 bucket

Bucket names are globally unique, so substitute your own suffix.

```bash
aws s3 mb s3://northwind-kb-docs-<your-unique-suffix> --region us-east-1
```

Or in the console: open <https://console.aws.amazon.com/s3/>, choose **Create bucket**, name it, and keep **Block all public access** enabled. There is no reason for these documents to be public, and a knowledge base reads them through an IAM role, not through public access.

### Create three documents

Create these locally, then upload them. The content is deliberately fictional.

**`shipping-policy.txt`**

```
Northwind Logistics Shipping Policy, revision 4.

Standard delivery within Singapore is 2 working days. Standard delivery to
Malaysia and Indonesia is 5 working days.

Express delivery is available in Singapore only and is next working day for
orders placed before 1400 hours.

Temperature-controlled shipping is available for perishable goods. It is
offered on the Singapore domestic network only and requires 24 hours notice.

Northwind does not ship lithium batteries, aerosols, or live animals.

Deliveries are not made on Sundays or public holidays.
```

**`claims-policy.txt`**

```
Northwind Logistics Claims Policy, revision 2.

A damage claim must be filed within 7 calendar days of delivery. A claim for
a parcel that never arrived must be filed within 21 calendar days of the
despatch date.

Claims above 500 Singapore dollars require review by an operations manager
and photographic evidence.

Temperature excursion claims on perishable goods are treated as priority and
must be acknowledged within 4 working hours.

Northwind's maximum liability for a standard parcel without declared value
is 100 Singapore dollars.
```

**`service-tiers.txt`**

```
Northwind Logistics Service Tiers.

Tier Bronze: standard delivery, email support, no service credit.
Tier Silver: standard delivery, email and phone support, 5 percent service
credit for a delivery more than 2 days late.
Tier Gold: express delivery included, dedicated account manager, 10 percent
service credit for any late delivery, and priority claims handling.

Tier is assigned annually based on shipment volume in the previous calendar
year. Gold requires more than 5000 shipments.
```

Upload them:

```bash
aws s3 cp shipping-policy.txt s3://northwind-kb-docs-<your-unique-suffix>/
aws s3 cp claims-policy.txt   s3://northwind-kb-docs-<your-unique-suffix>/
aws s3 cp service-tiers.txt   s3://northwind-kb-docs-<your-unique-suffix>/
```

Confirm all three are present:

```bash
aws s3 ls s3://northwind-kb-docs-<your-unique-suffix>/
```

### Establish the baseline now

Before building anything, open the Bedrock **Chat** playground, select a text model, and ask:

```
What is Northwind Logistics' maximum liability for a standard parcel with
no declared value?
```

Record the answer verbatim. The model has never seen these documents. It will either decline to answer or **produce a confident, plausible, entirely invented figure** — which is the more instructive outcome. Keep this answer; Step 6 compares against it.

**Checkpoint:** Billing alert set, three documents in an S3 bucket, and a recorded baseline answer from a model with no access to them.

---

## Step 2 — How RAG works

**Retrieval Augmented Generation** solves one specific problem: the model does not know your data. Its training data has a cutoff and never included your internal documents.

RAG does **not** teach the model anything. It **finds relevant text at query time and puts it in the prompt**. The model is unchanged. That single sentence answers a large share of exam questions on this topic.

### The two pipelines

RAG has an offline pipeline that runs when documents change, and an online pipeline that runs on every query. Confusing the two is a common error.

**Ingestion — offline, runs on sync:**

```
Documents in S3
      ↓  chunk
Text chunks
      ↓  embedding model
Vectors  (a list of numbers per chunk)
      ↓  index
Vector store
```

**Retrieval and generation — online, runs per query:**

```
User query
      ↓  same embedding model
Query vector
      ↓  similarity search against the vector store
Top-K most similar chunks
      ↓  inserted into the prompt as context
Foundation model
      ↓
Answer, with citations back to the source chunks
```

### The four moving parts

**1. Chunking.** Documents are split into pieces. Whole documents are not used because the context window is finite, retrieval precision is better on smaller units, and you pay tokens for everything you insert.

The tension: chunks too **small** lose the context that makes them meaningful; chunks too **large** dilute the match and waste tokens on irrelevant text. **Overlap** — repeating some text between adjacent chunks — stops a fact being sliced in half at a boundary. Bedrock knowledge bases offer strategies including fixed-size chunking with configurable size and overlap, and options for hierarchical and semantic chunking. Check the console for the strategies available in your Region. Lab 16 tests these directly.

**2. Embeddings.** An embedding model converts text into a vector — a list of numbers positioning that text in a high-dimensional space where semantically similar text sits close together. This is why RAG finds a chunk about "maximum liability" when you asked about "how much you cover" with no shared keywords. Contrast with keyword search, which would miss it.

**Critical:** the **same** embedding model must embed the documents and the queries. Vectors from different models are not comparable. Changing the embedding model means **re-embedding everything**.

**3. Vector store.** A database that indexes vectors and answers "which stored vectors are nearest to this one" quickly. Bedrock knowledge bases can create an OpenSearch Serverless collection for you, or use a vector store you already run — options typically include Amazon Aurora PostgreSQL with pgvector, Amazon OpenSearch Service, Pinecone and Redis Enterprise Cloud. Check the console for what is offered in your Region.

**This component is the cost.** The embedding and generation calls are per-token; the vector store is provisioned infrastructure billing by the hour.

**4. Retrieval and generation.** At query time the top-K chunks are retrieved and inserted into a prompt template alongside the question. The model answers **from that context**. Because you know which chunks were inserted, you can attach **citations** — the property that makes RAG auditable and distinguishes it sharply from fine-tuning.

### RAG versus fine-tuning

The most reliably examined comparison in Domain 3:

| | RAG | Fine-tuning |
|---|---|---|
| Changes model weights | No | Yes |
| Adds new facts | Yes | Poorly — it teaches form more than fact |
| Update a fact | Re-sync the document, seconds | Retrain, hours to days |
| Citations | Yes, natural | No |
| Cost profile | Vector store hourly + tokens per query | Training cost + hosting cost |
| Access control | Can filter by user permissions at retrieval | No — knowledge is baked in for everyone |
| Best at | Current, private, frequently changing facts | Style, tone, format, domain vocabulary, task shape |

The heuristic: **RAG for what the model should know; fine-tuning for how the model should behave.** Lab 17 works through this decision in full.

**Checkpoint:** You can draw both pipelines, explain why one embedding model must serve both sides, and state which component is the hourly cost.

---

## Step 3 — Create the knowledge base

> **This is the step that starts the meter.** Creating a knowledge base with a Bedrock-managed vector store provisions an OpenSearch Serverless collection that bills continuously from creation until deletion. Note the time you create it. Do not leave this lab unfinished.

### Enable an embedding model

Before creating anything, confirm you have access to an embedding model:

1. Open the Bedrock console at <https://console.aws.amazon.com/bedrock/> and check your Region.
2. In the left navigation choose **Model access**.
3. Confirm access is granted to at least one **embeddings** model and at least one **text** model. Embedding models are listed separately from text models and are easy to overlook — a knowledge base cannot be created without one.

### Create the knowledge base

1. In the left navigation, choose the **Knowledge bases** area and start creating a knowledge base.
2. **Name and description.** Name it something you will recognise when cleaning up — `northwind-kb` is fine.
3. **IAM permissions.** Let the console **create and use a new service role** unless your organisation requires otherwise. This role needs to read your S3 bucket, call the embedding model, and write to the vector store. If you supply your own role and the sync fails later, missing permissions on one of those three is the usual cause.
4. **Data source.** Choose **Amazon S3** and browse to the bucket you created in Step 1. Point at the bucket, or at a prefix within it. Note that other data source types may be offered — check the console for what is available in your Region.
5. **Chunking strategy.** You are asked how to split the documents. For this first pass choose the **default** strategy. Do not tune it yet — Lab 16 changes this deliberately and compares results, and you need an untuned baseline for that comparison to mean anything.

   Note what the console tells you here, particularly: **chunking configuration cannot be changed on an existing data source.** To change it you delete and recreate the data source, then re-sync. This is a real operational constraint worth remembering.

6. **Embeddings model.** Select the embedding model you enabled. Note its name — this choice is locked in for the life of the knowledge base, because changing it would invalidate every stored vector.
7. **Vector store.** You will be offered a choice between letting Bedrock create one for you and connecting one you already run.

   > **Pause here.** Selecting the quick-create option provisions an **Amazon OpenSearch Serverless collection**. Read whatever the console tells you about this on screen. This collection bills by the hour from creation, independently of the knowledge base, and it is the resource people forget in cleanup. Note down the collection name shown, if one is displayed — you will need it in Step 7.

8. **Review and create.** Creation takes several minutes while the vector store is provisioned and the index is set up.

### Record what was created

Before moving on, write down:

| Item | Value |
|---|---|
| Knowledge base name | |
| Knowledge base ID | |
| Region | |
| S3 bucket name | |
| Vector store type | |
| OpenSearch Serverless collection name | |
| Embedding model | |
| Time created | |

This table **is** your cleanup checklist. Filling it in now is the difference between a clean teardown and an unexplained bill.

You can confirm the knowledge base exists from the CLI:

```bash
aws bedrock-agent list-knowledge-bases --region us-east-1
```

And, if a collection was created for you:

```bash
aws opensearchserverless list-collections --region us-east-1
```

Run both now, so you know what "present" looks like. In Step 7 you will run the same two commands and expect them to come back empty.

**Checkpoint:** Knowledge base created, and every row of the resource table filled in.

---

## Step 4 — Sync the data source

Creating a knowledge base does not ingest anything. Documents are only chunked, embedded and indexed when you **sync** the data source. This trips people up constantly: the knowledge base exists, queries return nothing, and the sync was never run.

### Run the sync

1. Open your knowledge base in the console.
2. In the **data source** section, select your S3 data source and choose **Sync**.
3. Wait for it to complete. Three small text files take a short time; a large corpus can take considerably longer.
4. When it finishes, read the sync result. It reports how many documents were scanned, ingested and failed. **Confirm three documents were ingested and zero failed.**

If any document failed, the usual causes are an unsupported file type, an empty file, or the service role lacking `s3:GetObject` on the bucket.

### What just happened

For each document, in order:

1. It was **read** from S3.
2. It was **split into chunks** by your chosen strategy.
3. Each chunk was sent to the **embedding model** and converted to a vector.
4. Each vector was **written to the vector store** along with the chunk text and metadata identifying its source document.

Step 4 is why citations are possible. The source location travels with the vector, so a retrieved chunk can always be traced back to the file it came from.

You were billed for embedding tokens during this sync. That is a one-off per-sync cost, quite separate from the hourly vector store cost that has been accruing since Step 3.

### Inspect the retrieval directly

Before generating any answer, look at raw retrieval on its own. Separating retrieval from generation is the most valuable diagnostic habit in RAG work, and Lab 16 depends on it.

Use the CLI:

```bash
aws bedrock-agent-runtime retrieve \
  --knowledge-base-id <YOUR_KB_ID> \
  --retrieval-query '{"text":"How long do I have to file a damage claim?"}' \
  --region us-east-1
```

Or use the console's test window, which offers an option to show the retrieved source chunks alongside the generated response.

Examine the result carefully:

- **How many chunks came back?** That is your top-K, at its default.
- **What is in each chunk?** Read the actual text. Does the chunk containing the 7-day claim window also carry enough surrounding context to be understandable alone?
- **Is there a relevance score?** Higher means the chunk's vector was closer to the query's vector. Scores are comparable within one knowledge base and one embedding model; they are not an absolute measure of correctness.
- **Which source document is cited?** The location metadata should point at `claims-policy.txt`.

### Try a query that spans documents

```bash
aws bedrock-agent-runtime retrieve \
  --knowledge-base-id <YOUR_KB_ID> \
  --retrieval-query '{"text":"What happens if a Gold tier perishable shipment is late?"}' \
  --region us-east-1
```

This question requires facts from **three** documents: the Gold tier service credit, the temperature-controlled shipping rules, and the priority claims handling for temperature excursions.

Look at what came back. Did retrieval pull chunks from all three files, or did it return three chunks from whichever document matched most strongly overall? **Multi-document questions are where naive RAG most often falls short** — not because the model reasoned badly, but because the right chunks were never retrieved. Note what you observe; you will address it with top-K in Lab 16.

**Checkpoint:** Sync completed with three documents ingested and zero failures, and you have inspected raw retrieval output including chunk text, scores and source attribution.

---

## Step 5 — Retrieve and generate, and read the citations

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

---

## Step 6 — Compare against the no-context baseline

This step turns the lab into evidence. Put the RAG answer beside the plain-model answer from Step 1.

### The comparison

Open the plain **Chat** playground — no knowledge base — and re-ask all four questions from Step 5. Then place the two sets side by side.

| Question | Plain model answer | RAG answer | Which is correct? |
|---|---|---|---|
| Max liability | | | |
| Express to Malaysia | | | |
| Gold tier perishable late | | | |
| Lithium batteries by air | | | |

### What to notice

**The plain model was confident and wrong.** This is the observation that matters most. It did not say "I have no information about Northwind Logistics." It produced a fluent, specific, plausible answer — a liability figure, a delivery timeframe — with the same tone it uses when correct.

This is the practical definition of **hallucination**: not gibberish, but confident fabrication that is indistinguishable from a correct answer by fluency alone. A user cannot tell the difference. **That** is why grounding and citations are engineering requirements and not niceties.

**The RAG answer could be checked.** Every claim traced to a document you can open. Even where RAG was imperfect — question 3, or a partially-cited multi-document answer — you could *see* the imperfection. The plain model's errors were invisible.

**Freshness.** Change one fact in `claims-policy.txt`, upload the new version, and re-sync. The knowledge base reflects it within a sync. There is no equivalent for training data — a fine-tuned model with an outdated fact needs retraining.

### Design considerations this lab surfaces

These map directly to Task 3.1, "design considerations for applications that use foundation models":

- **Context window.** Retrieved chunks consume it. Higher top-K, larger chunks, or a long conversation history all compete for the same finite budget.
- **Cost per query.** You pay to embed the query, and you pay input tokens for every retrieved chunk on every call. Doubling top-K roughly doubles the retrieval portion of your input tokens.
- **Latency.** RAG adds an embedding call plus a vector search before generation begins.
- **Access control.** Retrieval is where per-user permissions belong. If a user must not see the claims policy, filter it out at retrieval — never rely on a prompt instruction to make the model decline. Metadata filtering, covered in Lab 16, is the mechanism.
- **Freshness versus consistency.** The vector store is only as current as the last sync. Decide your sync cadence and know your staleness window.
- **Retrieved content is untrusted.** Lab 14's indirect injection risk lands here concretely. Anyone who can write to that S3 bucket can influence what the model reads in **another user's** session. Lock down write access to the data source with the same rigour you apply to code.

### When RAG is the wrong answer

RAG is not universal. It is a poor fit when:

- the question needs **aggregation across the whole corpus** ("how many of our policies mention perishables?") — retrieval returns a handful of chunks, not a count, and a database query is the right tool;
- the corpus is **small enough to fit in the context window** — just include it and skip the vector store cost entirely;
- what you need is a **change of style, tone or output format** — that is prompt engineering or fine-tuning, not retrieval;
- the answer requires **reasoning over structured data** — SQL against a database beats similarity search over prose.

**Checkpoint:** All four questions compared side by side, and you can articulate why a confidently wrong answer is more dangerous than a refusal.

---

## Step 7 — Clean up

## ⚠️ This step is mandatory

**You created a vector store. It has been billing by the hour since Step 3, and it will keep billing until you delete it — whether or not you ever query it again.**

The critical point, and the one most often missed: **deleting the knowledge base does not reliably delete the OpenSearch Serverless collection underneath it.** They are separate resources with separate lifecycles. You must check for and delete both.

> **Going straight to Lab 16?** Lab 16 extends this knowledge base, so you may keep it — **but only if you are starting Lab 16 now and will finish today.** If there is any chance you will not, delete everything now and rebuild it in Lab 16. Rebuilding costs a few minutes; a forgotten collection costs money every hour indefinitely.

Work through this in order.

### 1. Delete the knowledge base

Console: open the **Knowledge bases** list, select `northwind-kb`, and delete it. Read the confirmation dialog carefully — it may tell you explicitly whether the vector store will also be removed. Whatever it says, verify in step 2 anyway.

CLI:

```bash
aws bedrock-agent delete-knowledge-base \
  --knowledge-base-id <YOUR_KB_ID> \
  --region us-east-1
```

Confirm it is gone:

```bash
aws bedrock-agent list-knowledge-bases --region us-east-1
```

### 2. Delete the vector store — do not skip this

**This is the expensive resource.**

1. Open the Amazon OpenSearch Service console at <https://console.aws.amazon.com/aos/> and find the **Serverless** area, or list collections from the CLI:

   ```bash
   aws opensearchserverless list-collections --region us-east-1
   ```

2. Locate the collection created for your knowledge base — match it against the collection name you recorded in the Step 3 resource table.
3. **Delete the collection.**

   ```bash
   aws opensearchserverless delete-collection --id <COLLECTION_ID> --region us-east-1
   ```

4. Re-run `list-collections` and confirm the result is empty, or no longer contains your collection.

Deleting the collection can leave behind its associated **security, network, encryption and data access policies**. These do not bill, but they are clutter — remove them from the OpenSearch Serverless console if you want a clean account.

**Check every Region you worked in.** Both the knowledge base list and the collection list are Region-scoped. A collection created in a Region you then switched away from is invisible in the console and still billing.

### 3. Delete the S3 bucket

S3 storage for three text files is negligible, but leave nothing behind:

```bash
aws s3 rm s3://northwind-kb-docs-<your-unique-suffix>/ --recursive
aws s3 rb s3://northwind-kb-docs-<your-unique-suffix>
```

### 4. Delete the IAM service role

If you let the console create a service role for the knowledge base, it now has no purpose. IAM roles do not bill, but an unused role with S3 read and Bedrock invoke permissions is unnecessary standing access. Find it in the IAM console at <https://console.aws.amazon.com/iam/> and delete it.

### 5. Verify against your resource table

Go back to the table you filled in at Step 3 and tick off every row:

- [ ] Knowledge base deleted, and `list-knowledge-bases` confirms it
- [ ] **OpenSearch Serverless collection deleted, and `list-collections` confirms it**
- [ ] Checked every Region you worked in
- [ ] S3 bucket emptied and deleted
- [ ] IAM service role deleted
- [ ] Associated OpenSearch Serverless policies removed

### 6. Check your bill tomorrow

Open the Billing and Cost Management console **the following day** and look at yesterday's spend by service. This is the only way to be certain nothing is still running, and it is a habit worth forming — an alert fires on a threshold, but a daily glance catches a slow leak below it.

If you find an unexpected OpenSearch Serverless charge, a collection survived somewhere. Check every Region.

**Checkpoint:** Every box above ticked, `list-collections` returns nothing of yours in every Region you used, and you have a reminder to check tomorrow's bill.

---

## Verification

- [ ] You set a billing alert before creating any resource.
- [ ] Three documents were uploaded to S3 and you recorded a plain-model baseline answer before building anything.
- [ ] You can draw the ingestion pipeline and the query pipeline and say which runs per query.
- [ ] You can explain why the same embedding model must serve both documents and queries.
- [ ] The knowledge base was created and every row of the Step 3 resource table was filled in.
- [ ] The sync completed with three documents ingested and zero failures.
- [ ] You inspected raw retrieval output and can describe the chunk text, the score and the source attribution.
- [ ] You ran retrieve-and-generate and traced at least one answer to the exact sentence in its cited chunk.
- [ ] You tested a question the documents do not answer and observed how the model handled the gap.
- [ ] You compared all four questions against the ungrounded model and can explain why the plain model's errors were invisible.
- [ ] **The knowledge base is deleted and `list-knowledge-bases` confirms it.**
- [ ] **The OpenSearch Serverless collection is deleted and `list-collections` confirms it, in every Region you used.**
- [ ] The S3 bucket and the IAM service role are deleted.

## Discussion questions

1. **RAG or fine-tuning (Tasks 3.1 and 3.3).** Northwind revises its claims policy roughly monthly, and the operations team must be able to show a customer exactly which clause a decision came from. A vendor proposes fine-tuning a model on the policy documents instead. Give three specific reasons that is the wrong choice here, and name the one circumstance in which fine-tuning would still be worth adding alongside RAG.

2. **The cost conversation.** Your knowledge base holds three text files and receives about twenty queries a day. Break the cost into its parts — vector store hourly, embedding per sync, generation per query — and identify which dominates at this volume. At what query volume would the balance shift, and what cheaper architecture would you propose for the low-volume case?

3. **Retrieval as a security boundary (Tasks 3.1 and 3.2).** The claims policy must be visible to operations staff but not to customers using the same chat interface. Explain why instructing the model not to reveal it is inadequate, and describe where in the pipeline the control actually belongs. Then consider the other direction: anyone who can write to the S3 bucket can influence answers given to other users — what do you do about that?

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.
