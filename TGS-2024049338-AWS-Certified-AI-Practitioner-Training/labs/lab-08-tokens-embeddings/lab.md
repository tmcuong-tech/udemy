# Lab 08 — Tokens, Embeddings and Vector Representations

Explore how text becomes tokens and why token counts drive cost and context limits, then generate embeddings with a Bedrock embedding model and measure semantic similarity.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 2 — Fundamentals of Generative AI (24%)
**Task statement:** 2.1 Explain the basic concepts of generative AI
**WSQ mapping:** LU2 · Topic 3 Amazon Bedrock Getting Started · K6 · A2 · LO2
**Slide reference:** v11 deck slides 137–164
**Estimated time:** 35 minutes

**Learning objectives:**
- Explain the difference between words and tokens, and why the two counts diverge
- Describe how token counts drive both cost and the context window, and keep the two distinct
- Generate an embedding vector from a Bedrock embedding model
- Compute cosine similarity between embeddings and interpret the result
- Explain how embeddings enable semantic search and underpin the retrieval half of RAG
- Identify which resources in an embeddings workflow bill continuously

**Prerequisites:**
- Labs 06 and 07 completed
- Access granted to an **embeddings** model in your Region (see the Bedrock **Model access** page)
- AWS CLI configured with credentials permitting `bedrock:ListFoundationModels` and `bedrock:InvokeModel`, and `python3` available. If you have no CLI access, Steps 3 and 4 can be read for the concepts and the console alternative followed instead.

Console entry point: <https://console.aws.amazon.com/bedrock/>

---

## Step 1 — Tokens are not words

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

---

## Step 2 — Tokens drive cost and the context window

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

---

## Step 3 — Generate an embedding

An **embedding** is a text turned into a list of numbers — a **vector**. An embedding model does not generate text; it converts text into coordinates in a high-dimensional space, arranged so that **texts with similar meaning land close together**.

That single property is what makes semantic search, recommendation and RAG possible.

## Find an embedding model in your Region

Do not assume a model ID. Ask the API which embedding models exist where you are:

```bash
aws bedrock list-foundation-models \
  --region us-east-1 \
  --by-output-modality EMBEDDING \
  --query 'modelSummaries[].[modelId,providerName]' \
  --output table
```

Pick one you have access to — an Amazon Titan Text Embeddings model is the usual choice — and store its exact ID in a shell variable so the rest of the lab does not depend on a version string printed in a handout:

```bash
MODEL_ID="<paste-the-exact-model-id-from-the-table-above>"
REGION="us-east-1"
```

> If the table is empty or your model shows no access, return to the **Model access** page in the Bedrock console and request an embeddings model. Check that page for the models available in your Region.

## Invoke it

```bash
aws bedrock-runtime invoke-model \
  --region "$REGION" \
  --model-id "$MODEL_ID" \
  --content-type application/json \
  --accept application/json \
  --cli-binary-format raw-in-base64-out \
  --body '{"inputText":"The cat sat on the mat."}' \
  embed-cat.json

cat embed-cat.json
```

Note the two flags people forget:

- `--cli-binary-format raw-in-base64-out` lets you pass the request body as plain JSON text rather than base64
- the trailing `embed-cat.json` is the **output file** — `invoke-model` writes the response to a file, it does not print it

## Read the response

```bash
# How many numbers are in the vector? (its dimensionality)
python3 -c "import json;d=json.load(open('embed-cat.json'));print('dimensions:',len(d['embedding']))"

# The first few coordinates
python3 -c "import json;d=json.load(open('embed-cat.json'));print(d['embedding'][:8])"
```

Observe:

- The output is a **fixed-length list of floating point numbers**. That length — the **dimensionality** — is a property of the model, not of your input.
- A six-word sentence and a whole paragraph produce vectors of the **same length**. Embedding compresses any input into the same fixed shape.
- The individual numbers mean nothing on their own. **No single coordinate is "the sentiment" or "the topic."** Meaning lives in the *direction* of the whole vector, and only becomes useful when you compare one vector with another.
- The response also reports how many input tokens were consumed — embedding calls are billed on tokens too, though typically far more cheaply than text generation.

## Console alternative

If you do not have CLI access, the Bedrock playground may offer an embeddings or text playground where an embeddings model can be selected. Submit the same sentence and observe the array of numbers returned. The concepts are identical; only the interface differs.

**Checkpoint:** You have a JSON file containing an embedding vector and you can state its dimensionality.

---

## Step 4 — Semantic similarity: compare the vectors

A single embedding is useless. Embeddings only earn their keep when you **compare** them.

## Embed four sentences

Two of these mean nearly the same thing but share almost no words. Two share words but mean different things. That contrast is the whole point.

```bash
embed () {
  aws bedrock-runtime invoke-model \
    --region "$REGION" \
    --model-id "$MODEL_ID" \
    --content-type application/json \
    --accept application/json \
    --cli-binary-format raw-in-base64-out \
    --body "{\"inputText\":\"$1\"}" \
    "$2" > /dev/null
  echo "embedded -> $2"
}

embed "How do I reset my password?"            a.json
embed "I forgot my login credentials."          b.json
embed "What are your office opening hours?"     c.json
embed "How do I reset my washing machine?"      d.json
```

Sentences **a** and **b** mean the same thing and share only the word "my". Sentences **a** and **d** share four words but mean completely different things.

## Measure the distance between them

The standard measure is **cosine similarity** — the cosine of the angle between two vectors. It ranges from **1.0** (pointing the same way, semantically very close) through **0** (unrelated) to **-1.0** (opposite).

```bash
cat > cosine.py <<'PY'
import json, math, itertools

def vec(path):
    return json.load(open(path))["embedding"]

def cosine(u, v):
    dot = sum(a*b for a, b in zip(u, v))
    nu  = math.sqrt(sum(a*a for a in u))
    nv  = math.sqrt(sum(b*b for b in v))
    return dot / (nu * nv)

labels = {
    "a.json": "reset my password",
    "b.json": "forgot my login credentials",
    "c.json": "office opening hours",
    "d.json": "reset my washing machine",
}
vs = {f: vec(f) for f in labels}

for x, y in itertools.combinations(labels, 2):
    print(f"{cosine(vs[x], vs[y]):+.4f}   {labels[x]:<30} vs  {labels[y]}")
PY

python3 cosine.py
```

## Record and interpret

| Pair | Cosine similarity | Shared words? | Same meaning? |
|---|---|---|---|
| a vs b — password reset / forgot credentials | | almost none | yes |
| a vs d — reset password / reset washing machine | | many | no |
| a vs c — password reset / opening hours | | none | no |
| b vs c | | | |
| c vs d | | | |

Now answer:

1. Which pair scored **highest**? Was it the pair sharing the most words, or the pair sharing the most meaning?
2. Compare **a vs b** with **a vs d**. If you had built search by keyword matching, which pair would keyword matching have ranked higher? What would that have done to the user asking about their password?
3. All four sentences are short. Would you expect **c vs d** — two unrelated sentences — to score near zero, or somewhere above it? In practice, embeddings of same-language, same-domain text often score moderately similar even when unrelated. **What matters is the ranking of scores relative to each other, not the absolute number.**

> **This is the mechanism behind semantic search.** Embed every document once and store the vectors. At query time, embed the question and find the stored vectors closest to it. The system retrieves on **meaning**, so a user who asks "I can't get into my account" finds the password reset article that never uses those words.

**Checkpoint:** Your similarity table is filled in, and the semantically similar pair scores higher than the lexically similar pair.

---

## Step 5 — Where this leads: vector stores and RAG

You have now built, by hand, the core of a semantic search engine. Scale it up and it becomes the retrieval half of a **RAG** (Retrieval Augmented Generation) system — the subject of Labs 15 and 16.

## The pipeline

**Indexing — done once, ahead of time:**

1. **Chunk** the documents. A 40-page policy PDF is split into passages, because you want to retrieve the relevant paragraph, not the whole file.
2. **Embed** each chunk with an embedding model — exactly the call you made in Step 3.
3. **Store** each vector, alongside its source text and metadata, in a **vector store** — a database that can search by vector proximity. On AWS this might be an OpenSearch Serverless collection, Aurora with pgvector, or another supported store.

**Query time — done on every user question:**

4. **Embed the question** with the **same** embedding model.
5. **Search** the store for the nearest vectors — this is your cosine calculation from Step 4, done efficiently over millions of vectors.
6. **Assemble a prompt** containing the retrieved chunks plus the question, and send it to a **text generation** model.
7. The model answers **grounded in the retrieved text**, and can cite where the answer came from.

## Four things that follow directly from what you just did

**The same model must be used for both sides.** Vectors from two different embedding models are not comparable — they are coordinates in different spaces. If you change embedding model, you must **re-embed your entire corpus**. This is a real migration cost, and a common exam point.

**Embedding models and text models are different tools.** An embedding model cannot write you a paragraph. A text model cannot give you a vector to store. Both appear in the Bedrock catalogue; they have different output modalities, as you saw in Lab 06.

**Retrieved chunks are input tokens.** Everything you retrieve is pasted into the prompt and billed on every call, and it competes for the context window (Step 2). This is why RAG systems retrieve the top few chunks rather than everything that scored above a threshold — retrieval quality beats retrieval quantity.

**Chunk size is a trade-off.** Chunks that are too large dilute the meaning of the vector and waste tokens. Chunks that are too small lose the context needed to answer. Lab 16 makes you tune this.

## Beyond search

The same vectors support:

- **Recommendation** — "items similar to this one" is a nearest-neighbour query
- **Clustering and topic discovery** — group vectors that sit close together
- **Deduplication** — near-identical documents produce near-identical vectors
- **Classification** — embed the input, compare against labelled examples

**Checkpoint:** You can describe the seven-step RAG pipeline and explain why changing the embedding model forces a full re-index.

---

## Step 6 — Clean up

This lab used **on-demand, serverless** inference only. No endpoint, index, collection or instance was created, so there is nothing running up a bill.

1. **Delete the local files** you created:

   ```bash
   rm -f embed-cat.json a.json b.json c.json d.json cosine.py
   ```

   Embedding output files are large — a single vector is hundreds of floating point numbers — and they clutter a working directory quickly.

2. **Unset the shell variables** if you are handing the terminal to someone else:

   ```bash
   unset MODEL_ID REGION
   ```

3. **Confirm you did not create a vector store.** Step 5 described the RAG pipeline but you did **not** build one. If you went exploring in the console and created any of the following, delete them **now** — every one of them bills continuously, whether you query it or not:

   | Resource | Why it matters |
   |---|---|
   | **OpenSearch Serverless collection** | Bills for a minimum capacity allocation from the moment it exists, independent of usage. This is the most expensive accidental resource in the whole course. |
   | **Bedrock Knowledge Base** | Creating one may create a vector store for you as a side effect — deleting the Knowledge Base does not always delete that store. Check both. |
   | **Kendra index** | Bills continuously per index. |
   | **Aurora / RDS cluster used for pgvector** | Bills per instance-hour. |

   Check the OpenSearch Serverless and Bedrock consoles directly if you are unsure.

   > **Do not leave these for "later".** They are the resources most likely to produce an unwelcome bill after a training day, precisely because nothing about them looks like it is running.

4. **Leave model access enabled** if you are continuing to Lab 09. Enabled access costs nothing; **invocations** are billed on tokens processed.

5. **Close the playground tab** so a stray keystroke does not submit another request.

**Checkpoint:** Local files removed, and you have confirmed no vector store, Knowledge Base or search index exists in your account.

---

## Verification

- [ ] You can explain why one long or rare word becomes several tokens
- [ ] You can state why a timestamp or a block of JSON costs more tokens than plain prose of the same length
- [ ] You can distinguish cost per token from the context window, and say which one you cannot change
- [ ] You completed the token arithmetic exercise and named the change that saves the most tokens
- [ ] You produced an embedding vector and can state its dimensionality
- [ ] Your cosine similarity table is filled in, and the semantically similar pair scored higher than the lexically similar pair
- [ ] You can describe the RAG indexing and query pipeline and explain why changing embedding model forces a full re-index
- [ ] Local files removed, and no vector store, Knowledge Base or search index exists in your account

## Discussion questions

1. A team reports that their chat assistant "gets more expensive the longer people talk to it". Explain the mechanism, and propose two ways to control it without degrading the experience.
2. Keyword search would rank "how do I reset my washing machine" above "I forgot my login credentials" for the query "how do I reset my password". Your embeddings ranked them the other way round. Where would keyword search still be the better choice, and why might a production system use both?
3. An organisation has indexed 2 million document chunks and a newer embedding model becomes available that scores better on benchmarks. What does adopting it actually require, what would it cost, and how would you decide whether it is worth doing?

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.
