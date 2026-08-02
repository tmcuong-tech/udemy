# Lab 16 — Vector Stores and Retrieval Quality

Tune the retrieval half of a RAG pipeline — chunk size, overlap, top-K and metadata filtering — and learn to tell a retrieval failure from a generation failure.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 3 — Applications of Foundation Models (28%)
**Task statement:** 3.1 Describe design considerations for applications that use foundation models
**WSQ mapping:** LU4 · Topic 8 Developing GenAI Solutions · K5 · A4 · LO4
**Slide reference:** v11 deck slides 184–209
**Estimated time:** 40 minutes

> ## ⚠️ COST WARNING
>
> This lab uses the knowledge base from Lab 15, backed by a **vector store** — normally an **Amazon OpenSearch Serverless collection** — which bills continuously by the hour from creation until deletion, whether or not you query it. **Complete this lab in one sitting and do Step 6 in full.** Deleting the knowledge base does **not** reliably delete the collection underneath. Set an AWS Budgets alert before you begin.

**Prerequisite:** Lab 15. This lab extends the same knowledge base; rebuild it from Lab 15 Steps 1, 3 and 4 if you deleted it.

**Learning objectives:**

- Measure retrieval quality separately from answer correctness, and use that split to locate a fault.
- Explain the chunk size trade-off and what overlap fixes, with concrete examples.
- Compare fixed-size, hierarchical and semantic chunking, and say why hierarchical resolves the trade-off rather than compromising.
- Tune top-K and explain the recall–precision trade-off and why the asymmetry favours recall.
- Apply metadata filtering, and argue why access control in a RAG system belongs at retrieval.
- Follow a diagnostic procedure for a wrong RAG answer, in cost order, ending rather than starting at the prompt.
- Delete a knowledge base **and** every vector store collection it created, and verify it.

---

## Step 1 — Set up and measure a baseline

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

---

## Step 2 — Chunk size and overlap

Chunking is the highest-leverage decision in a RAG system and the one most often left at its default. A bad chunking strategy produces bad answers that look like model failures.

### The trade-off

Every chunk is embedded into a **single vector**. That vector must represent everything in the chunk. This creates a direct tension:

**Chunks too small:**
- A vector represents one narrow idea — precise matching.
- But **context is lost**. A chunk reading "This requires 24 hours notice" is nearly useless: which service? Retrieved alone, the model cannot use it.
- Facts get **split across boundaries**. "Claims above 500 Singapore dollars require review by an operations manager" landing in one chunk and "and photographic evidence" in the next means neither chunk answers the question completely.
- More chunks means more vectors, a larger index, and more retrieval calls to cover the same material.

**Chunks too large:**
- Each chunk is self-contained and readable.
- But the vector is a **blurred average** of several topics. A chunk covering claims deadlines, monetary thresholds and temperature excursions has a vector that is not strongly close to any of those queries. Retrieval precision drops.
- You pay input tokens for the **entire** chunk on every retrieval, most of it irrelevant.
- Fewer, larger chunks fill the context window faster, so effective top-K falls.

### Overlap

**Overlap** repeats a slice of text between adjacent chunks. Its single job is to stop a fact being severed at a boundary — with overlap, a sentence spanning the split appears complete in at least one chunk.

Overlap costs storage and duplicates text across retrieved results. A common starting point is a modest overlap, on the order of ten to twenty percent of chunk size. **Treat that as a starting point to be tested, not a rule.** The right number depends on how your documents are written.

### Chunking strategies

Bedrock knowledge bases offer several. Check the console for what is available in your Region:

| Strategy | How it splits | Best for |
|---|---|---|
| **Fixed-size** | A configured number of tokens, with configured overlap | General text; predictable and easy to reason about |
| **No chunking** | One chunk per document | Documents already short and single-topic |
| **Hierarchical** | Parent and child chunks — retrieve on small children, return larger parents | Getting precision *and* context together |
| **Semantic** | Splits at points where meaning shifts rather than at a fixed length | Documents with uneven section lengths |

**Hierarchical chunking is worth understanding well**, because it directly resolves the trade-off above rather than compromising on it: you match against small, precise chunks but hand the model the larger parent that surrounds the match.

### Run the experiment

Chunking configuration **cannot be changed on an existing data source**. To test a different strategy you must create a new data source or a new knowledge base and re-sync.

**If your budget and time allow**, create a second data source over the same S3 bucket with a **noticeably smaller** fixed chunk size and **zero overlap**, sync it, and re-run the five test questions from Step 1.

**If not, reason it through** — this is the exam-relevant part and requires no provisioning. Take `claims-policy.txt` and mark by hand where a small, zero-overlap chunker would split it. Then answer:

1. Does any single chunk still contain the complete answer to **Q2** (maximum liability)?
2. **Q5** needs the Gold shipment threshold *and* what Gold includes. In `service-tiers.txt` those sit in different paragraphs. With small chunks, would one retrieved chunk carry both? What does that imply for top-K?
3. Which chunk boundary would **overlap** have rescued, and which would it not?

### What you should conclude

- **Retrieval failures caused by chunking are invisible in the generated answer.** The model gives a confident partial answer from an incomplete chunk. Nothing signals that the other half of the fact existed and was not retrieved.
- **The right chunk size depends on your documents**, not on a universal best practice. Dense reference material with one fact per line wants different chunking from flowing narrative prose.
- **Chunking is set at ingestion.** Changing it means re-ingesting everything, which is why it is worth testing on a small corpus before committing to a large one.

**Checkpoint:** You can explain both failure modes with a concrete example from these documents, describe what overlap fixes, and say why hierarchical chunking resolves the trade-off rather than compromising on it.

---

## Step 3 — Top-K

**Top-K** is how many chunks retrieval returns for insertion into the prompt. Unlike chunking, it is set **per query** — so you can experiment freely without re-ingesting anything.

### Run the experiment

Take **Q4**, the multi-document question, which needs facts from all three files:

```
What happens if a Gold tier customer's perishable shipment arrives late?
```

Run it at several values of K. Specify K through the retrieval configuration:

```bash
aws bedrock-agent-runtime retrieve \
  --knowledge-base-id <YOUR_KB_ID> \
  --retrieval-query '{"text":"What happens if a Gold tier customer perishable shipment arrives late?"}' \
  --retrieval-configuration '{"vectorSearchConfiguration":{"numberOfResults":1}}' \
  --region us-east-1
```

Repeat with `numberOfResults` set to 3, then 5, then a higher value. The console test panel also exposes the number of retrieved results in its configuration options.

Record for each:

| K | Distinct source documents retrieved | All three facts present? | Total retrieved text | Answer correct? |
|---|---|---|---|---|
| 1 | | | | |
| 3 | | | | |
| 5 | | | | |
| higher | | | | |

Then run the full retrieve-and-generate at each K and check the answer.

### What you should see

**At K=1** the answer is almost certainly incomplete. Only one chunk was available, so at most one of the three needed facts was present. Critically, **the model does not announce the gap** — it answers confidently from what it has. This is the clearest demonstration in the whole domain that a RAG failure looks exactly like a model failure.

**Raising K improves recall.** More chunks means a higher chance the needed facts are all present. Q4 typically becomes answerable somewhere in the middle of the range.

**Raising K further stops helping, then hurts:**
- **Cost.** Every retrieved chunk is input tokens on every query. Doubling K roughly doubles the retrieval share of your input cost.
- **Latency.** More text to process before generation.
- **Context window pressure.** Chunks compete with the system prompt and conversation history for a finite budget.
- **Dilution.** With many marginally-relevant chunks present, the model may latch onto a low-relevance chunk that happens to be phrased confidently. Adding noise can make a previously correct answer wrong.

### Precision and recall

The standard framing, and it is examinable:

- **Recall** — of all the chunks that *should* have been retrieved, how many were? Raising K raises recall.
- **Precision** — of the chunks that *were* retrieved, how many were actually relevant? Raising K lowers precision.

Tuning K is choosing a point on that trade-off. There is no universally correct value.

**The asymmetry that decides it:** a fact that was never retrieved is **unrecoverable** — the model has no path to the right answer. A fact that was retrieved alongside irrelevant material is merely **more expensive**, and the model will usually still find it. So the sensible default is to **bias toward recall**, then reduce K if cost, latency or dilution become real problems.

### Beyond top-K

Two techniques you should be able to name:

- **Re-ranking.** Retrieve a generous K by vector similarity, then use a second, more accurate model to re-score those candidates and keep only the best few. This gets high recall from the first stage and high precision from the second — at the cost of an extra model call.
- **Hybrid search.** Combine vector similarity with keyword search. Pure vector search can miss exact identifiers — a part number, an error code, a policy revision number — because such strings carry little semantic meaning. Hybrid search covers that gap. Check the console for the search type options available on your knowledge base.

**Checkpoint:** You have run Q4 at several values of K, seen K=1 give a confidently incomplete answer, and can explain why the asymmetry between recall and precision favours biasing toward recall.

---

## Step 4 — Metadata filtering

Vector similarity finds semantically similar text. It has no idea whether a chunk is current, whether it applies to the right region, or whether **this particular user is allowed to see it**. Metadata filtering supplies that.

### How metadata works

Each document can carry structured attributes. For a Bedrock knowledge base with an S3 data source, you supply these in a companion metadata file alongside each document in the bucket, using the naming convention shown in the console for your Region.

The content is a small JSON object of attributes you define:

```json
{
  "metadataAttributes": {
    "doc_type": "claims",
    "audience": "internal",
    "revision": 2,
    "effective_year": 2026
  }
}
```

Attribute names and values are yours to choose. Design them deliberately — you are defining the filter dimensions your application will have forever, and adding a new one later means re-ingesting.

At query time, a filter is applied **during** the vector search, so non-matching chunks are never candidates:

```bash
aws bedrock-agent-runtime retrieve \
  --knowledge-base-id <YOUR_KB_ID> \
  --retrieval-query '{"text":"What are the claim deadlines?"}' \
  --retrieval-configuration '{
      "vectorSearchConfiguration": {
        "numberOfResults": 5,
        "filter": { "equals": { "key": "audience", "value": "internal" } }
      }
  }' \
  --region us-east-1
```

Check the console or the service documentation for the full set of filter operators available in your Region — typically equality, inequality, comparison operators for numbers, list membership, and boolean combinations.

### Try it

If you want to see it working end to end, add a metadata file for each of your three documents with a `doc_type` attribute (`shipping`, `claims`, `tiers`), re-sync, and then run **Q1** with a filter restricting to `doc_type = shipping`. Retrieval should fail to find the claims deadline, because the only chunk containing it has been excluded from the candidate set.

That failure is the point. **The filter is applied before similarity ranking, not after.** An excluded chunk is not a low-scoring result — it does not exist as far as this query is concerned.

### The three things filtering is for

**1. Access control — the important one.**

Consider a chat interface used by both customers and operations staff over one knowledge base. The claims policy is internal.

The wrong design: instruct the model in the system prompt not to reveal internal policies to customers. Lab 14 explains exactly why this fails — the instruction is steering, not enforcement, the content is already in the context window, and prompt injection or plain misunderstanding will eventually surface it.

The right design: **the customer's session applies a filter of `audience = public`, so internal chunks are never retrieved.** The model cannot leak what it was never given. The control is deterministic and it sits outside the probabilistic component.

This is the single most important architectural point in the lab. **Access control in RAG belongs at retrieval.** Your application derives the filter from the authenticated user's identity — never from anything the user typed, which would let them ask for the filter to be widened.

**2. Freshness and versioning.** Filter to the current revision so superseded policy text is never retrieved, while remaining in the store for audit. Without this, a query can retrieve both revision 2 and revision 4 of the same clause, and the model has no reliable way to know which governs.

**3. Precision on large corpora.** With three documents everything is close. With fifty thousand, a query about claims will surface superficially similar text from unrelated departments. Narrowing the candidate set by department, product line or geography raises precision far more cheaply than tuning K.

### Design guidance

- **Filter first, then tune K.** Filtering shrinks the haystack; K decides how much of it you take. Doing them the other way round wastes effort.
- **Metadata is set at ingestion.** A dimension you did not think of means re-ingesting. Think about audience, effective date, version, language and owning team up front.
- **Never let user input construct the filter.** Derive it from the authenticated session. A filter built from user-supplied text is an authorisation bypass waiting to happen.
- **Filtering does not replace bucket-level security.** If a document must not be retrievable by a class of user, also consider whether it should be in that knowledge base at all. Separate knowledge bases for separate trust domains is a legitimate and often safer design.

**Checkpoint:** You can write a metadata attributes object, explain why a filter is applied before ranking rather than after, and argue why access control belongs at retrieval rather than in the system prompt.

---

## Step 5 — Diagnose a bad answer

You now have every tool. This step assembles them into a procedure you can apply to any RAG system that is giving wrong answers.

### The diagnostic procedure

When a RAG answer is wrong, resist the urge to edit the prompt. Work through this in order.

**Question 1 — Was the answer in the corpus at all?**

Search the source documents directly. If the fact is not there, this is not a retrieval or generation problem; it is a **data coverage** problem, and the fix is to add the document. Surprisingly often, this is the answer.

**Question 2 — Was the correct chunk retrieved?**

Run retrieval alone and read the chunks. This is the fork in the road:

- **Chunk not retrieved** → retrieval problem. Go to question 3.
- **Chunk retrieved** → generation problem. Go to question 5.

Do not skip this. It determines which half of the system you work on, and getting it wrong means hours spent tuning a prompt that was never the issue.

**Question 3 — Why was the chunk not retrieved?**

- **Was it excluded by a filter?** Re-run without the filter. If it appears, your metadata or filter logic is wrong.
- **Was it ranked below K?** Re-run with a much higher K. If it appears at rank 8, raise K or add re-ranking.
- **Did it not appear at any K?** The chunk's vector is genuinely far from the query's. Causes: the chunk is too large and its vector is a blurred average; the query uses vocabulary the document never uses; or the fact is an exact identifier that vector search handles poorly, which is the case for hybrid search.

**Question 4 — Was the chunk retrieved but incomplete?**

The fact was severed at a chunk boundary. This is a chunking problem: increase chunk size, add overlap, or move to hierarchical chunking. Symptom to recognise: a **confident half-answer** — the model states the part it received as if it were the whole rule.

**Question 5 — The right chunk was retrieved and the answer is still wrong.**

Now, and only now, it is a generation problem:

- **The model contradicted the chunk.** Strengthen the prompt: instruct it to answer only from the provided context. Consider contextual grounding checks in Guardrails.
- **The model blended context with training knowledge.** Same fix, plus check citations — an uncited claim in the answer is the tell.
- **Conflicting chunks were retrieved** — two revisions of the same clause. This is a *metadata* fix, not a prompt fix. Filter to the current version.
- **The model answered despite insufficient context.** Explicitly instruct it to say when the provided context does not answer the question, and treat "I cannot answer from the provided documents" as a **successful** outcome, not a failure. A system that never admits ignorance is a system whose ignorance you cannot see.

### Work an example

Recall **Q3**: *Can I get express delivery to Malaysia?*

The correct answer is no — `shipping-policy.txt` states express is available in Singapore only. The document never says "Malaysia" and "express" in the same sentence, because it is expressing the answer as a **limitation** rather than a denial.

Run Q3 and work the procedure:

1. Is the answer in the corpus? Yes, implicitly, in the express delivery paragraph.
2. Was the chunk retrieved? Check. Vector similarity to a query mentioning Malaysia may pull the *international delivery* paragraph instead, which mentions Malaysia and never mentions express.
3. If the express paragraph was not retrieved — is it below K, or genuinely distant? Try a higher K.
4. If both paragraphs came back, what did the model do? Did it correctly combine "express is Singapore only" with the question about Malaysia, or did it see "Malaysia: 5 working days" and answer with a delivery time?

**The lesson:** negative and constraint-based facts are harder for RAG than positive facts, because the query's vocabulary matches the wrong paragraph. The mitigation is partly retrieval — higher K, hybrid search — and partly **how the source documents are written**. A policy document that states limitations explicitly ("Express delivery is not available outside Singapore") retrieves far better than one that states them by omission.

> **Document authoring is part of RAG engineering.** A corpus written for human readers, who infer from context, often retrieves badly. Explicit, self-contained statements retrieve well. This is a genuine and underrated lever.

### The tuning order

When retrieval quality is poor, work in this order — cheapest and highest-leverage first:

1. **Check data coverage.** Is the fact even there?
2. **Fix the source documents.** Make implicit facts explicit. Free, and it helps every query.
3. **Add metadata and filter.** Shrinks the haystack. No re-chunking needed.
4. **Tune top-K.** Per query, no re-ingestion, immediate feedback.
5. **Add hybrid search or re-ranking.** More capability, more cost per query.
6. **Change the chunking strategy.** Requires full re-ingestion — do it last, and test on a sample first.
7. **Only then** touch the generation prompt.

Most teams do this list backwards, starting with the prompt because it is the most visible part. That is why so much time gets spent on prompts that were never the problem.

**Checkpoint:** You can state the procedure, know that retrieval-only inspection is the fork that decides everything, and can explain why negative facts retrieve poorly and what to do about it.

---

## Step 6 — Clean up

## ⚠️ Mandatory — the vector store is still billing

Your knowledge base is backed by a vector store that has been billing by the hour since it was created — in Lab 15 or at the start of this lab — and it will keep billing until deleted, whether or not you query it again.

**This is the last lab in the course that uses a knowledge base. There is no reason to keep it.** Delete everything.

Remember the trap from Lab 15: **deleting the knowledge base does not reliably delete the OpenSearch Serverless collection underneath.** They are separate resources. Check both.

### 1. Delete any extra data sources or knowledge bases

If you created a second data source or a second knowledge base in Step 2 to test chunking, delete those first. List everything so nothing is missed:

```bash
aws bedrock-agent list-knowledge-bases --region us-east-1
```

### 2. Delete the knowledge base

Console: open the **Knowledge bases** list, select it, delete it.

CLI:

```bash
aws bedrock-agent delete-knowledge-base \
  --knowledge-base-id <YOUR_KB_ID> \
  --region us-east-1
```

Confirm with `list-knowledge-bases` that nothing of yours remains.

### 3. Delete the vector store — the expensive one

```bash
aws opensearchserverless list-collections --region us-east-1
```

Match each result against the collection name in your resource table, then delete it:

```bash
aws opensearchserverless delete-collection --id <COLLECTION_ID> --region us-east-1
```

Re-run `list-collections` and confirm the result no longer contains your collection.

**If you created a second knowledge base for the chunking experiment, it very likely created a second collection.** Delete that one too. `list-collections` returning empty is the only acceptable result.

**Check every Region you worked in.** Both lists are Region-scoped, and a collection in a Region you switched away from is invisible in the console and still billing.

### 4. Remove the remaining resources

- **S3 bucket**, including any metadata files added in Step 4:

  ```bash
  aws s3 rm s3://northwind-kb-docs-<your-unique-suffix>/ --recursive
  aws s3 rb s3://northwind-kb-docs-<your-unique-suffix>
  ```

- **IAM service roles** created by the console for the knowledge bases. They do not bill, but they carry S3 read and Bedrock invoke permissions with no remaining purpose. Remove them from <https://console.aws.amazon.com/iam/>.
- **OpenSearch Serverless policies** — security, network, encryption and data access policies left behind by the deleted collections. They do not bill; remove them for a clean account.

### 5. Final verification

- [ ] `aws bedrock-agent list-knowledge-bases` shows none of yours, in every Region used
- [ ] **`aws opensearchserverless list-collections` shows none of yours, in every Region used**
- [ ] Second knowledge base and second collection from the chunking experiment also deleted
- [ ] S3 bucket emptied and deleted
- [ ] IAM service roles deleted
- [ ] Leftover OpenSearch Serverless policies removed

### 6. Check tomorrow's bill

Open the Billing and Cost Management console **the following day** and look at yesterday's spend by service. An OpenSearch Serverless line item means a collection survived somewhere — go back to step 3 and check every Region.

You are now past the expensive part of this course. Labs 17 and 18 walk through configuration without provisioning, and the remaining labs use serverless or low-cost services.

**Checkpoint:** Every box ticked, both list commands return nothing of yours in every Region you used, and you have a reminder to check tomorrow's bill.

---

## Verification

- [ ] You recorded a baseline for all five questions covering both retrieval quality and answer correctness.
- [ ] You can state the fork in the diagnostic procedure: was the correct chunk retrieved, yes or no.
- [ ] You can give a concrete example from these documents of a fact severed by a chunk boundary, and say what overlap would have done.
- [ ] You can explain why a very large chunk retrieves less precisely than a well-sized one.
- [ ] You can describe hierarchical chunking and why it addresses the trade-off directly.
- [ ] You ran Q4 at several values of top-K and observed a confidently incomplete answer at K=1.
- [ ] You can define recall and precision in retrieval terms and say which way K moves each.
- [ ] You can explain why the recall–precision asymmetry favours biasing toward recall.
- [ ] You can name re-ranking and hybrid search and say what each is for.
- [ ] You can write a metadata attributes object and explain why filters are applied before ranking.
- [ ] You can argue why a system prompt instruction is the wrong control for withholding internal documents.
- [ ] You can put the seven tuning steps in cost order, with the generation prompt last.
- [ ] **Every knowledge base and every OpenSearch Serverless collection is deleted and verified, in every Region used.**

## Discussion questions

1. **Diagnosing in the right half (Task 3.1).** Your RAG assistant gives a confident but incomplete answer about a claims deadline. A colleague proposes rewriting the generation prompt to demand more thorough answers. What do you check first, and what specific evidence would tell you the prompt is not the problem? Describe two distinct root causes that would produce this exact symptom and require completely different fixes.

2. **Retrieval as an authorisation boundary (Tasks 3.1 and 3.2).** One knowledge base serves customers and internal staff. Design the control that stops customers retrieving internal policy. State where the filter value comes from, why it must never derive from user input, and what a successful prompt injection could achieve against your design. Then argue the case for using two separate knowledge bases instead, and say when you would choose that.

3. **Documents as an engineering artefact.** Q3 retrieves poorly because the source states a limitation by omission rather than explicitly. Rewrite the express delivery paragraph so it retrieves well for a query about Malaysia. Then generalise: what three properties make a document retrieve well, and what does that imply for how an organisation should write policy documents it intends to put in a knowledge base?

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.
