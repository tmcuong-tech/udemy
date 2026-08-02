# Domain 2 — Fundamentals of Generative AI (24%)

Part of the [AWS Certified AI Practitioner Training (AIF-C01) Learner Guide](../LEARNER%20GUIDE.md) · course code TGS-2024049338

---

## Lab 06 — Amazon Bedrock Getting Started

Enable foundation model access in Amazon Bedrock, explore the model catalogue, and run your first prompt in the playground.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 2 — Fundamentals of Generative AI (24%)
**Task statement:** 2.1 Explain the basic concepts of generative AI
**WSQ mapping:** LU2 · Topic 3 Amazon Bedrock Getting Started · K6 · A2 · LO2
**Slide reference:** v11 deck slides 137–164
**Estimated time:** 30 minutes

**Learning objectives:**
- Enable access to foundation models in the Amazon Bedrock console for a chosen Region
- Explain why model availability is specific to an AWS account and Region
- Navigate the model catalogue and identify a model's provider, modality and model ID
- Run a prompt in the Bedrock playground without writing code
- Distinguish the Bedrock control plane (`bedrock`) from the data plane (`bedrock-runtime`)
- Identify which Bedrock resources are serverless and which bill continuously

**Prerequisites:**
- An AWS account you can sign in to with console access
- IAM permissions for Amazon Bedrock — at minimum the actions behind `bedrock:ListFoundationModels`, `bedrock:GetFoundationModel` and `bedrock:InvokeModel`, plus the ability to view and manage model access
- Awareness that invoking a model incurs charges based on tokens processed. Keep prompts short.

Console entry point: <https://console.aws.amazon.com/bedrock/>

---

### Step 1 — Open Amazon Bedrock and choose a Region

Amazon Bedrock is a **fully managed service** that gives you a single API to foundation models (FMs) from several providers. There are no servers, clusters or endpoints for you to create — you call a model and you are billed for the tokens you process.

The first thing to understand is that **Bedrock is Region-specific**. The service itself is not offered in every AWS Region, and within a supported Region, the *set of models* offered differs. A model you have seen in a demo may simply not exist in the Region you are sitting in.

1. Sign in to the AWS Management Console.
2. Open the Amazon Bedrock console at <https://console.aws.amazon.com/bedrock/>.
3. Use the **Region selector** at the top right of the console to choose a Region in which Bedrock is offered. This lab assumes **US East (N. Virginia) `us-east-1`**.
4. Write down the Region you chose. Everything you do for the rest of this lab — model access, playground history, model IDs — belongs to that Region and nothing carries over to another one.
5. If a welcome or overview screen appears, choose the option to get started so that the full left navigation is displayed.

> **Console layouts drift.** AWS changes the Bedrock console regularly. Throughout this lab, follow the **named item** in the left navigation rather than a fixed screen position. If a label has been renamed, look for the item that does the job being described.

**Checkpoint:** The Bedrock console is open and you can state, out loud, which Region you are working in.

---

### Step 2 — Request access to foundation models

Having a Bedrock console does not mean you can call every model in it. Access is granted **per AWS account, per Region, per model**. Some models are available as soon as you ask; some providers require you to submit use case details first.

1. In the **left navigation**, find the configuration or settings area and choose **Model access**.
2. Read the page before clicking anything. It lists the foundation models offered in *this* Region and shows a status for each one — typically indicating whether access is already available, has been granted, or must still be requested.

   > This page — not your memory, not this handout, not a blog post — is the source of truth for which models you can use. Check the **Model access** page for the models available in your Region.

3. Choose the button that lets you **modify** or **manage** model access. Depending on the console version the label may read *Enable specific models*, *Modify model access*, or similar.
4. Select at least **two models from two different providers**. For example, one Amazon Titan text model and one Anthropic Claude model, or a Meta Llama model. Choosing two *different providers* matters, because Lab 07 asks you to compare them.
5. Also select one **embeddings** model if the Region offers one — Lab 08 needs it. Embedding models are usually listed with the others but produce vectors, not text.
6. If a provider asks for **use case details**, complete the short form honestly. Describe the use case as internal training and evaluation of foundation models.
7. Review your selections and **submit** the request.
8. Return to the **Model access** page and refresh until your chosen models show as granted. Some are granted almost immediately; others take longer. If one is still pending after a few minutes, carry on with any model that *has* been granted.

**Why this exists (exam relevance):** model access is an explicit, auditable opt-in. It is the account owner deciding which third-party models their organisation is permitted to send data to. Enabling access by itself does **not** generate charges — only invocations do.

**Checkpoint:** At least two models, from two different providers, show access granted in your chosen Region.

---

### Step 3 — Explore the model catalogue

Bedrock's value proposition is **choice through one API**. The catalogue is where you see that choice.

1. In the **left navigation**, open the model catalogue area. Labels vary by console version — look for *Model catalog*, *Foundation models*, or *Base models*.
2. Browse the list. Notice that models are grouped or filterable by **provider** and by **modality**.
3. Pick **three** different models and record the following for each:

| # | Model name | Provider | Modality (text / image / embeddings / multimodal) | Stated use cases (from the console) |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

4. Open the **detail page** for one model. Observe two things:
   - The model is identified by a **model ID** — a string your code passes to the API.
   - Providers publish **multiple versions** of a model over time, and the version is part of that ID.

> **Do not memorise version strings for the exam.** Model IDs change as providers ship new versions. What the exam expects you to know is that models are *selected by ID*, that IDs are *versioned*, and that availability is *per Region*.

**Providers and modalities — the mental model**

- **Provider** answers "who built and trained this model". Bedrock's role is to host several providers behind one consistent interface so you are not locked into one vendor.
- **Modality** answers "what goes in and what comes out". A text model takes text and returns text. An image model returns an image. An **embeddings** model returns a list of numbers (a vector) — you will use one of these in Lab 08. A **multimodal** model accepts more than one input type, such as text plus an image.

**Checkpoint:** You have recorded provider, modality and stated use case for three models, and you can point to where a model ID is displayed.

---

### Step 4 — Run your first prompt in the playground

The playground lets you send a prompt to a model without writing any code. It is the fastest way to build intuition.

1. In the **left navigation**, open the **playground** area and choose the **Chat** or **Text** playground.
2. Choose **Select model**, pick a **provider**, then pick one of the models you enabled in Step 2. Apply the selection.
3. Enter this **exact prompt**:

   ```
   Explain what a foundation model is to a small business owner who has
   never used AI. Use no more than 80 words and avoid technical jargon.
   ```

4. Run it and read the answer carefully. Record four things:
   - roughly **how long** the answer is,
   - the **tone** — formal, conversational, marketing-like,
   - whether it **respected the 80-word limit**,
   - whether it used **jargon** despite being told not to.

| Model used | Length | Tone | Respected 80 words? | Jargon slipped in? |
|---|---|---|---|---|
| | | | | |

5. Now run a second, deliberately different prompt on the same model:

   ```
   List three tasks a small retail business could automate with AI,
   and for each one say what could go wrong.
   ```

6. Notice that you did not configure a server, choose an instance type, or wait for anything to start. That is the whole point of a **managed FM API**: the infrastructure is not yours. Compare this with Lab 04, where deploying a SageMaker model required you to pick an instance and wait for an endpoint.

> **Keep prompts short.** On-demand Bedrock inference is billed on **tokens processed**, both input and output. Long prompts and long answers cost more. There is no charge for simply having the playground open.

**Checkpoint:** You have run at least two prompts and recorded observations for the first one.

---

### Step 5 — See the same catalogue from the AWS CLI

Everything you just clicked through is available through the API. Seeing it as data makes the Region-specific, ID-based nature of the catalogue concrete.

If you have the AWS CLI configured with credentials that allow Bedrock read actions, run:

```bash
# Which models exist in this Region?
aws bedrock list-foundation-models --region us-east-1

# Narrow it down to text models
aws bedrock list-foundation-models \
  --region us-east-1 \
  --by-output-modality TEXT

# Just the IDs, so the list is readable
aws bedrock list-foundation-models \
  --region us-east-1 \
  --query 'modelSummaries[].modelId' \
  --output table

# Everything one provider offers here
aws bedrock list-foundation-models \
  --region us-east-1 \
  --by-provider amazon
```

Then look at a single model in detail. Copy one model ID from the output above:

```bash
aws bedrock get-foundation-model \
  --region us-east-1 \
  --model-identifier <paste-a-model-id-here>
```

Read the response and find:

- `modelId` — the string your application passes when it invokes the model
- `providerName` — who built it
- `inputModalities` / `outputModalities` — what goes in and what comes out
- `responseStreamingSupported` — whether the model can stream tokens back as they are produced, rather than making the user wait for the whole answer

Now change the Region and run the first command again:

```bash
aws bedrock list-foundation-models \
  --region us-west-2 \
  --query 'modelSummaries[].modelId' \
  --output table
```

Compare the two lists. If they differ, you have just demonstrated to yourself why "is this model available?" is always a Region-specific question.

> **Note the two different API namespaces.** `aws bedrock ...` is the **control plane** — listing models, managing access, custom models. `aws bedrock-runtime ...` is the **data plane** — actually invoking a model to get an answer. You will use `bedrock-runtime` in Lab 08.

If you do not have CLI access in your training account, read this step for the concepts and move on. The console work in Steps 2–4 is sufficient to complete the lab.

**Checkpoint:** You can explain the difference between `bedrock` and `bedrock-runtime`, and you have seen that the model list is a per-Region result.

---

### Step 6 — Clean up

**Good news: on-demand Bedrock inference is serverless.** Running this lab does not leave behind an instance, an endpoint or a cluster that bills you by the hour. There is nothing you must delete to stop a meter.

That said, do the following:

1. **Close the playground tab.** A stray keystroke in an open playground submits another billable request.

2. **Decide what to do about model access.** Access granted in Step 2 is a **persistent account setting** — it stays granted in that Region until you change it. In a shared or corporate account, follow your organisation's policy on which models may remain enabled. Leave your models enabled if you are continuing to Labs 07 and 08, which need them.

   > Enabled access by itself does **not** generate charges. **Invocations** do.

3. **Check that you did not create anything billable while exploring.** If, while looking around the console, you created any of the following, delete it now — these are **not** serverless and continue to incur charges until removed:
   - **Provisioned Throughput** for a model (billed for a committed term — this is the most expensive accidental click in the Bedrock console)
   - A **custom model** / fine-tuning job
   - A **Knowledge Base**, and any vector store it created for you, such as an **OpenSearch Serverless collection**
   - A **model evaluation job**

   To check from the CLI:

   ```bash
   aws bedrock list-provisioned-model-throughputs --region us-east-1
   aws bedrock list-custom-models --region us-east-1
   ```

   Both should return an empty list after this lab.

4. **Turn on cost visibility.** If this is your own account, set up an **AWS Budget** or a billing alert so that unexpected usage surfaces early rather than at the end of the month.

5. **Do not quote pricing from memory.** Consult the official Amazon Bedrock pricing page for current rates before doing any cost estimation for a real project.

**Checkpoint:** The playground is closed, no provisioned throughput or custom models exist, and you have made a conscious decision about which models stay enabled.

---

### Verification

- [ ] You can name the Region you worked in and explain why Region matters for model availability
- [ ] The **Model access** page shows access granted for at least two models from two different providers
- [ ] You recorded provider, modality and stated use case for three catalogue models
- [ ] You can point to where a model ID is shown and explain that model IDs are versioned
- [ ] You ran at least two prompts in the playground and recorded observations for one
- [ ] You can state the difference between the `bedrock` and `bedrock-runtime` API namespaces
- [ ] `list-provisioned-model-throughputs` and `list-custom-models` return empty, and the playground tab is closed

### Discussion questions

1. Model access is granted per account, per Region, per model, and some providers require use case details first. What business and governance problem is this control solving, and who in an organisation should own the decision?
2. Bedrock gives you several providers behind one managed API with no servers to run. What does an organisation gain, and what does it give up, compared with hosting an open-weights model on its own infrastructure? Consider operational effort, scaling, data handling, and the ability to switch models later.
3. On-demand Bedrock inference leaves nothing running, yet Provisioned Throughput, custom models and Knowledge Bases all bill continuously. Why does that distinction matter more in a training account than the per-token cost of the prompts you ran today?

---

---

## Lab 07 — Comparing Foundation Models and Inference Parameters

Run one identical prompt across two or more foundation models, then hold the model constant and vary temperature, top-P and max tokens.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 2 — Fundamentals of Generative AI (24%)
**Task statement:** 2.1 Explain the basic concepts of generative AI
**WSQ mapping:** LU2 · Topic 3 Amazon Bedrock Getting Started · K6 · A2 · LO2
**Slide reference:** v11 deck slides 137–164
**Estimated time:** 35 minutes

**Learning objectives:**
- Compare the output of two or more foundation models given one identical prompt
- Explain why a fair comparison holds the prompt, the parameters and the conversation history constant
- Describe what temperature does to the model's next-token probability distribution
- Distinguish temperature from top-P (and top-K) in mechanism and in effect
- Demonstrate that max tokens truncates output rather than instructing the model to be brief
- Choose appropriate parameter settings for factual versus creative tasks

**Prerequisites:**
- Lab 06 completed
- Access granted to at least **two foundation models from two different providers** in your Region
- Awareness that each playground run is billed on tokens processed. Prompts in this lab are deliberately short.

Console entry point: <https://console.aws.amazon.com/bedrock/>

---

### Step 1 — Set up the comparison and run the first model

Different foundation models, given exactly the same prompt, produce noticeably different answers. Those differences are not random noise — they come from differences in training data, model size and instruction tuning. The only way to see this is to hold the prompt constant and change the model.

**Before you start,** confirm from Lab 06 that you have access granted to at least **two models from two different providers** in your Region. If not, return to the **Model access** page and request them now.

1. Open the Amazon Bedrock console at <https://console.aws.amazon.com/bedrock/> and confirm your Region.
2. In the **left navigation**, open the **playground** area and choose the **Chat** or **Text** playground.
3. Choose **Select model**, pick a provider, then pick your first model. Apply the selection.
4. Leave the inference parameters at their defaults for now. You will change them in Steps 3–5.
5. Enter this **exact prompt** — you must not change a single word of it between models:

   ```
   Explain what a foundation model is to a small business owner who has
   never used AI. Use no more than 80 words and avoid technical jargon.
   ```

6. Run it, then record four observations in the **Model comparison table** below:
   - **Length** — roughly how many words came back
   - **Tone** — formal, conversational, marketing-like, teacherly
   - **Followed the 80-word limit?** — yes or no
   - **Jargon?** — did it use technical terms despite being told not to

## Model comparison table

Fill this in as you go. You will add the second row in Step 2.

| Model | Provider | Length | Tone | Followed 80-word limit? | Jargon? |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |

**Checkpoint:** One row of the comparison table is complete.

---

### Step 2 — Run the identical prompt on a second model

1. **Clear the conversation**, or start a new playground session. This matters: in a chat playground the previous exchange stays in context and will influence the next answer. You want a clean comparison, not a continuation.
2. Choose **Select model** again and switch to a model from a **different provider**.
3. Paste the **same prompt, completely unchanged**, and run it.
4. Record the same four observations as the second row of your comparison table.
5. *(Optional, if a third model is available to you)* Repeat with a third model and fill the third row.

Now compare your rows and answer these in writing:

- Which answer would you actually put in front of a paying customer, and **why**?
- Did the models disagree about *what a foundation model is*, or only about *how to say it*? A difference in style is a preference. A difference in substance is a correctness problem.
- Did any model ignore an explicit instruction in the prompt (the word limit, the no-jargon rule)? **Instruction-following is itself a model capability that varies between models** — it is not guaranteed just because you asked clearly.

> **The exam point:** model choice is a real engineering decision with trade-offs across quality, instruction-following, latency and cost per token. Bedrock's single API is what makes switching models cheap — your application code changes a model ID, not an integration.

**A fair comparison requires:**

| Hold constant | Vary |
|---|---|
| The prompt text, word for word | The model |
| The inference parameters | |
| An empty conversation history | |

If you change two things at once, you learn nothing from the result. This is the same discipline you will apply in Steps 3–5, where the model is held constant and the parameters vary.

**Checkpoint:** At least two rows in the comparison table, from two different providers, for one identical prompt, with a written difference noted between them.

---

### Step 3 — Baseline at low temperature: seeing non-determinism

Now reverse the experiment. **Hold the model constant** and change the knobs. Pick **one** model from Step 2 and stay on it for the rest of the lab.

1. In the playground, open the **inference configuration** panel — look for *Configurations*, *Inference parameters*, or a settings control beside the model name.
2. Find the controls for **Temperature**, **Top P**, and the maximum response length (labelled **Maximum length**, **Max tokens**, or similar). The exact set of parameters offered **depends on the model you selected** — some models expose more controls than others.
3. Set **temperature to a low value, near 0**. Leave top-P as provided.
4. Use this prompt:

   ```
   Give me a name for a new coffee shop in Singapore and one sentence
   explaining the name.
   ```

5. Run it **three times**, clearing the conversation between runs, and record each answer in the **Parameter observation table** below.
6. Look at your three answers. At low temperature they should be **similar or identical** to each other.

## What temperature actually does

A text model does not "know" the next word. At each position it computes a **probability distribution** over possible next tokens, then **samples** one from that distribution. Temperature reshapes that distribution before sampling:

- **Low temperature** sharpens the distribution towards the most probable tokens. Output becomes closer to **deterministic**, more predictable, more repetitive.
- **High temperature** flattens the distribution, giving lower-probability tokens a real chance. Output becomes more varied and more "creative" — and more likely to go off-brief.

> **Important nuance for the exam:** even at temperature 0, foundation models are **not guaranteed to be perfectly reproducible**. Low temperature makes output *closer to* deterministic; it does not turn the model into a lookup table. If your application genuinely requires the identical answer every time, a generative model is the wrong tool — use a template, a database query, or a rule.

## Parameter observation table

| Run | Temperature | Top-P | Max tokens | Answer (summarise) | What you noticed |
|---|---|---|---|---|---|
| Low temp — run 1 | | | | | |
| Low temp — run 2 | | | | | |
| Low temp — run 3 | | | | | |
| High temp — run 1 | | | | | |
| High temp — run 2 | | | | | |
| High temp — run 3 | | | | | |
| Low top-P | | | | | |
| Small max tokens | | | | | |

**Checkpoint:** Three low-temperature rows recorded, and you can describe how similar they were.

---

### Step 4 — Raise temperature, then narrow top-P

## High temperature

1. Stay on the same model and the same coffee shop prompt.
2. Raise **temperature** towards its maximum for this model.
3. Run the prompt **three times**, clearing between runs, and record all three answers in the parameter observation table.
4. Compare the spread. The three high-temperature answers should differ from each other **noticeably more** than the three low-temperature answers did. You may also see an answer that is odd, strains for cleverness, or drifts off the brief entirely.

Write one sentence in your table describing the difference in *variety* between the low and high temperature runs. That sentence is the whole lesson.

## Top-P

1. Return temperature to a **middle** value so it is not dominating the result.
2. Lower **top P** substantially — to a small fraction of its range.
3. Run the prompt again and record the answer.

**What top-P does.** Top-P (also called *nucleus sampling*) restricts sampling to the **smallest set of candidate tokens whose probabilities add up to P**. Everything outside that set is discarded before sampling happens.

- A **low top-P** (say 0.1) means the model only ever draws from the very few most likely tokens. Narrow vocabulary, safe and conventional output.
- A **high top-P** (near 1.0) leaves almost the entire vocabulary in play.

## Temperature versus top-P

Both increase or decrease variety, which is why they are easy to confuse. The distinction the exam cares about:

| Parameter | Mechanism | Plain-English effect |
|---|---|---|
| **Temperature** | Reshapes the probability distribution — flattens it or sharpens it | How *adventurous* the model is allowed to be |
| **Top-P** | Truncates the candidate list to the top tokens summing to P | How *many candidates* the model is allowed to consider at all |
| **Top-K** (offered by some models) | Truncates to the K most probable tokens, a fixed count | Same idea as top-P but a fixed number rather than a probability mass |

**In practice you tune one, not all of them.** Changing temperature and top-P at the same time makes the result impossible to attribute — the same discipline as Step 2.

**Rules of thumb:**
- Factual extraction, classification, structured output → **low** temperature and top-P
- Brainstorming, marketing copy, creative naming → **higher** temperature and top-P

**Checkpoint:** Three high-temperature rows and one low-top-P row recorded, and you can state the difference between the two parameters in your own words.

---

### Step 5 — Max tokens: truncation is not brevity

This step exists because it is one of the most commonly misunderstood parameters, and it appears on the exam.

1. Stay on the same model. Set **temperature** back to a middle value.
2. Set the **maximum response length** (*Max tokens* / *Maximum length*) to a **small** value — small enough that a normal answer could not possibly fit.
3. Run a prompt that would naturally produce a long answer:

   ```
   Describe in detail how a small retail business in Singapore could use
   generative AI across marketing, customer service and inventory.
   ```

4. Read what comes back. **The response stops mid-sentence.** It is not a shorter, well-formed answer — it is a full answer with the end cut off.
5. Record this in the parameter observation table.

## Why this matters

**Max tokens is a hard stop applied to generation. It is not an instruction to the model.**

The model does not see the max tokens value and decide to be concise. It begins writing the answer it was always going to write, and generation is halted the moment the limit is reached. The result is truncated, not summarised.

| If you want... | Do this | Not this |
|---|---|---|
| A genuinely shorter, complete answer | Say so **in the prompt** — "in no more than 50 words", "answer in one sentence" | Lower max tokens |
| A hard ceiling on cost and latency per call | Set **max tokens** | Rely on the prompt alone |

In production you usually do both: the prompt asks for brevity, and max tokens is a **safety ceiling** so a misbehaving generation cannot run away with your token bill or block your request timeout.

6. **Prove it to yourself.** Reset max tokens to a generous value, then run this instead:

   ```
   Describe in detail how a small retail business in Singapore could use
   generative AI across marketing, customer service and inventory.
   Answer in no more than 40 words.
   ```

   This time the answer is **short and complete** — it has an ending. That is the difference between instructing the model and cutting it off.

7. Reset the maximum length to a reasonable value before finishing.

## Where the parameters live in a real call

These are not console-only settings. When an application invokes a model, the same values are sent in the request body — the exact field names vary by model provider, which is one more reason Bedrock's unified API is useful.

**Checkpoint:** You have seen a response truncated mid-sentence, and you can explain why that is not the same as asking the model to be concise.

---

### Step 6 — Clean up

As in Lab 06, on-demand Bedrock inference is **serverless** — this lab leaves behind no instance, endpoint or cluster to delete.

1. **Reset your inference parameters** to their defaults before leaving the playground, so a later lab does not inherit an extreme temperature or a tiny max tokens value and confuse you.
2. **Clear the conversation and close the playground tab.** An open playground is one stray keystroke away from another billable request.
3. **Leave model access enabled** if you are continuing to Lab 08, which needs an embeddings model. Otherwise follow your organisation's policy on which models may remain enabled. Enabled access costs nothing; **invocations** are billed on tokens processed.
4. **Keep your tables.** The model comparison table and the parameter observation table are the deliverables of this lab and are referenced in the verification checklist.
5. **Confirm nothing billable was created while exploring.** If you clicked into Provisioned Throughput, custom models, model evaluation or Knowledge Bases, delete what you created — these bill continuously, unlike on-demand inference:

   ```bash
   aws bedrock list-provisioned-model-throughputs --region us-east-1
   aws bedrock list-custom-models --region us-east-1
   ```

   Both should return an empty list.

   > **Provisioned Throughput is the expensive mistake here.** It reserves model capacity for a committed term and bills for that term whether you send requests or not. On-demand inference is the correct choice for all of this course's labs.

6. **Do not estimate costs from memory.** Token pricing differs by model and by provider — a model that looked best in your comparison table may be several times the price of the runner-up. Consult the official Amazon Bedrock pricing page when the trade-off matters.

**Checkpoint:** Parameters reset, playground closed, no provisioned throughput or custom models exist, and both tables are filled in.

---

### Verification

- [ ] The model comparison table has at least two rows, from two different providers, for one identical prompt
- [ ] You wrote down which answer you would put in front of a customer, and why
- [ ] The parameter observation table has three low-temperature rows and three high-temperature rows for the same model and prompt
- [ ] You observed that repeated runs at low temperature are more similar than repeated runs at high temperature
- [ ] You can state the difference between temperature and top-P in your own words
- [ ] You observed a response truncated mid-sentence by a small max tokens value
- [ ] You produced a short *and complete* answer by asking for brevity in the prompt instead
- [ ] Parameters reset, playground closed, no provisioned throughput or custom models exist

### Discussion questions

1. Two models gave different answers to your identical prompt. How would you decide which one to ship, and what would you need to measure beyond "which one reads better"? Consider instruction-following, latency, cost per token and consistency across many inputs.
2. A colleague sets max tokens to a small value and reports that "the model gives short answers now". What is actually happening, what will the user see, and how would you fix it properly?
3. A compliance team asks you to guarantee that a customer-facing assistant returns the identical answer to the identical question every time. Can temperature 0 deliver that guarantee? What would you propose instead, and what does this tell you about where generative models belong in a solution?

---

---

## Lab 08 — Tokens, Embeddings and Vector Representations

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

### Step 1 — Tokens are not words

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

### Step 2 — Tokens drive cost and the context window

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

### Step 3 — Generate an embedding

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

### Step 4 — Semantic similarity: compare the vectors

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

### Step 5 — Where this leads: vector stores and RAG

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

### Step 6 — Clean up

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

### Verification

- [ ] You can explain why one long or rare word becomes several tokens
- [ ] You can state why a timestamp or a block of JSON costs more tokens than plain prose of the same length
- [ ] You can distinguish cost per token from the context window, and say which one you cannot change
- [ ] You completed the token arithmetic exercise and named the change that saves the most tokens
- [ ] You produced an embedding vector and can state its dimensionality
- [ ] Your cosine similarity table is filled in, and the semantically similar pair scored higher than the lexically similar pair
- [ ] You can describe the RAG indexing and query pipeline and explain why changing embedding model forces a full re-index
- [ ] Local files removed, and no vector store, Knowledge Base or search index exists in your account

### Discussion questions

1. A team reports that their chat assistant "gets more expensive the longer people talk to it". Explain the mechanism, and propose two ways to control it without degrading the experience.
2. Keyword search would rank "how do I reset my washing machine" above "I forgot my login credentials" for the query "how do I reset my password". Your embeddings ranked them the other way round. Where would keyword search still be the better choice, and why might a production system use both?
3. An organisation has indexed 2 million document chunks and a newer embedding model becomes available that scores better on benchmarks. What does adopting it actually require, what would it cost, and how would you decide whether it is worth doing?

---

---

## Lab 09 — Generative AI Capabilities and Limitations

Exercise what generative AI does well, then deliberately produce a hallucination, document it, and apply grounding and human review as mitigations.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 2 — Fundamentals of Generative AI (24%)
**Task statement:** 2.2 Understand the capabilities and limitations of generative AI for solving business problems
**WSQ mapping:** LU3 · Topic 5 Exploring AI Use Cases · K7 · A3 · LO3
**Slide reference:** v11 deck slides 165–172
**Estimated time:** 30 minutes

**Learning objectives:**
- Demonstrate summarisation, generation, translation and code capabilities in the Bedrock playground
- Identify the common property that predicts whether a generative AI task will succeed
- Deliberately produce a hallucination and record it verbatim with evidence that it is false
- Observe non-determinism, knowledge cutoff, bias and cost/latency limitations first hand
- Apply grounding to convert a hallucinated answer into a correct or declined one
- Match human review models to the risk level of a use case, and state what each mitigation does not fix

**Prerequisites:**
- Labs 06 and 07 completed
- Access granted to at least one text foundation model in your Region
- Use one model for the whole lab so your observations are comparable

Console entry point: <https://console.aws.amazon.com/bedrock/>

---

### Step 1 — Capabilities: summarisation and generation

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

---

### Step 2 — Capabilities: translation and code

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

---

### Step 3 — Produce a hallucination yourself and record it

This is the most important step in the lab. **You are not finished until you have made the model state something false with complete confidence, and written it down.**

Reading that models hallucinate changes nobody's behaviour. Watching a fluent, well-formatted, entirely fabricated answer appear on your own screen does.

## Why hallucination happens

A text model predicts likely next tokens. It has **no separate store of facts** and **no mechanism to check whether what it is saying is true**. Fluency and accuracy are produced by the same process, so a false answer looks exactly as confident as a true one. There is no internal signal you can read off the output that says "I am guessing here."

## Techniques that reliably provoke one

Try these in order and stop when you have a clear, checkable falsehood. Prompts that ask for **specific, verifiable, obscure facts** work best.

1. **The plausible non-existent thing.** Ask for details about something that sounds real but is not — a book, a paper, a standard, a product feature. For example, ask for a summary of a specific-sounding but invented technical paper, including its authors and its main finding.

2. **Ask for citations.** Ask the model to recommend published sources on a narrow topic and to give author, title and year for each. Then check whether they exist. Fabricated references are one of the most consistently reproducible failure modes.

3. **Very obscure specifics.** Ask for a precise number, date or name in a niche area — the population of a small town in a specific year, the exact clause number of a regulation, a minor historical figure's dates.

4. **The false premise.** Ask a question that assumes something untrue and see whether the model challenges the premise or plays along. Models often play along.

5. **A question about the near past.** Ask about something recent (see Step 4 on knowledge cutoff) and watch it answer confidently anyway rather than saying it does not know.

## Record it — this is a required deliverable

| Field | Your record |
|---|---|
| Model used | |
| Exact prompt | |
| The false claim, quoted verbatim | |
| How you verified it was false | |
| Did the model hedge at all, or state it flatly? | |
| Would a non-expert reader have spotted it? | |

**The last row is the one that matters.** A hallucination that an expert catches is a nuisance. One that a customer, a patient, a junior employee or a court filing does not catch is a business, legal or safety incident.

## Then try to fix it

Re-run your prompt with this added:

```
If you do not know the answer or are not confident it is factually
correct, say "I don't know" rather than guessing. Do not invent
sources, names, dates or figures.
```

Record whether the model now declines. Then note carefully what this **does not** give you:

> **Prompting for honesty reduces hallucination. It does not eliminate it, and it gives you no guarantee.** The model has no reliable way to know that it does not know. You cannot make a factual guarantee out of a prompt instruction — which is exactly why Step 5's mitigations are architectural rather than verbal.

**Checkpoint:** You have a verbatim false claim written down, along with how you verified it and whether a non-expert would have caught it.

---

### Step 4 — The other four limitations

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

---

### Step 5 — Mitigations: grounding, review and scoping

None of the limitations in Steps 3 and 4 can be removed. They are properties of how the technology works. What a competent solution does is **manage** them.

## Mitigation 1 — Grounding with RAG

**This is the primary defence against hallucination**, and it follows directly from the pattern you spotted in Step 1: the model performed well when the source material was **in the prompt**.

RAG (Retrieval Augmented Generation) makes that the architecture rather than the accident. Retrieve the relevant documents from a trusted source, put them in the prompt, and instruct the model to answer **only** from them.

**Prove it to yourself now.** Take the topic where you produced a hallucination in Step 3 and re-run it grounded:

```
Answer the question using ONLY the reference text below. If the answer
is not contained in the reference text, reply exactly "Not found in the
provided documents." Do not use any other knowledge.

REFERENCE TEXT:
<paste two or three true sentences on the topic, from a source you trust>

QUESTION:
<your Step 3 question>
```

Record what changed. You should see the model either answer correctly from your text or decline. **You have narrowed the model's job from "recall a fact" to "read this passage"** — and reading a supplied passage is a task it is genuinely good at.

Then note what grounding does **not** fix:

- If the retrieved documents are wrong or out of date, the answer is confidently wrong — grounded on bad ground
- If retrieval misses the relevant document, the model may fall back on training knowledge unless firmly instructed not to
- Grounding does nothing for bias, cost or latency, and it *increases* token usage and latency

Labs 15 and 16 build a real RAG system with Knowledge Bases for Amazon Bedrock.

## Mitigation 2 — Human review, scaled to the stakes

Not everything needs the same scrutiny. Match the review model to the consequence of being wrong:

| Risk level | Example | Review model |
|---|---|---|
| Low | Internal brainstorming, first drafts | None — the human is already the reader |
| Medium | Customer email drafts, summaries | **Human in the loop** — a person approves before it is sent |
| High | Medical, legal, financial, safety advice | Human in the loop, by a **qualified** reviewer, with the source cited |
| Unacceptable | Fully autonomous decisions affecting a person's rights, money or health | Do not automate the decision — use AI only to assist the decision-maker |

The pattern that works: **AI drafts, a human approves.** It captures most of the productivity gain while keeping accountability with a person who can be held responsible.

## Mitigations 3-6

- **Cite sources.** Require the model to quote the passage it used. This does not make it correct, but it makes checking *cheap* — and a mitigation nobody can afford to apply is not a mitigation.
- **Constrain the scope.** A narrowly scoped assistant over a known document set fails far less than a general-purpose one. Refusing out-of-scope questions is a feature.
- **Apply guardrails.** Amazon Bedrock Guardrails can filter topics, block harmful content and detect gaps in grounding, independently of the prompt. Because they sit outside the prompt, they cannot be talked out of by a user. Lab 19 covers these.
- **Set expectations with users.** Tell people they are talking to an AI, that it can be wrong, and how to escalate to a human. Undisclosed AI is a trust and, increasingly, a regulatory problem.

## Complete your record

| Limitation | Primary mitigation | What the mitigation does NOT fix |
|---|---|---|
| Hallucination | | |
| Non-determinism | | |
| Knowledge cutoff | | |
| Bias | | |
| Cost and latency | | |

**Checkpoint:** You have re-run your Step 3 hallucination with grounding, recorded what changed, and completed the mitigations table.

---

### Step 6 — Clean up

This lab used the **serverless** Bedrock playground only. No endpoint, index or instance was created, so nothing is billing by the hour.

1. **Clear the conversation and close the playground tab.** You ran a lot of prompts in this lab, and an open playground is one keystroke away from another billable request.

2. **Reset any inference parameters** you changed while testing non-determinism, so a later lab does not inherit them.

3. **Keep your written records.** The hallucination record from Step 3 and the limitations and mitigations tables from Steps 4 and 5 are the deliverables of this lab and appear in the verification checklist. They are also the most directly exam-relevant notes you will produce in Domain 2.

4. **Handle the outputs responsibly.** If you generated bias examples in Step 4, do not circulate them out of context — they are teaching artefacts produced from a handful of runs, not a measurement of any model's fairness. Any real claim about bias requires a defined metric and many samples (Lab 20).

5. **Confirm nothing billable was created.** If you explored beyond the playground into Knowledge Bases, Guardrails evaluation, model evaluation jobs, provisioned throughput or custom models, remove what you created:

   ```bash
   aws bedrock list-provisioned-model-throughputs --region us-east-1
   aws bedrock list-custom-models --region us-east-1
   ```

   Both should return an empty list.

   > If you created a **Knowledge Base** while exploring the grounding section, delete it — and check separately for an **OpenSearch Serverless collection**, which may have been created alongside it and which bills continuously whether you query it or not.

6. **Leave model access enabled** if you are continuing to Lab 10. Enabled access costs nothing; invocations are billed on tokens processed.

**Checkpoint:** Playground closed, parameters reset, your written records kept, and no Knowledge Base, vector store, provisioned throughput or custom model exists in your account.

---

### Verification

- [ ] The capability table has four rows — summarisation, generation, translation, code — each noting something the model did imperfectly
- [ ] You can state the property shared by the tasks that succeeded (the source material was in the prompt)
- [ ] **You produced a hallucination and recorded the false claim verbatim**, with how you verified it and whether a non-expert would have caught it
- [ ] You re-ran the prompt asking the model to admit ignorance, and can explain why that is not a guarantee
- [ ] The limitations table is complete for non-determinism, knowledge cutoff, bias, and cost/latency with your own observations
- [ ] You re-ran your hallucination prompt with grounding and recorded what changed
- [ ] The mitigations table names what each mitigation does **not** fix
- [ ] Playground closed, and no Knowledge Base, vector store, provisioned throughput or custom model exists

### Discussion questions

1. Based only on what you observed, name two things the model did genuinely well and two it did poorly. A customer asks you to guarantee the answers are factually correct every time. What do you tell them, and what does that imply for how the solution must be designed?
2. Describe a business task where a generative foundation model would be a worse choice than a rule, a database query or a classical ML model. Weigh cost per request, latency, auditability, consistency, and whether the task actually requires generating new language at all.
3. Grounding with RAG is the primary defence against hallucination, but a grounded system can still be confidently wrong. Give two ways that happens, and say what else must be in place before such a system faces customers.

---

---

## Lab 10 — Choosing Bedrock, SageMaker JumpStart or a Managed Service

Compare the three layers of AWS AI capability on the same task, build a decision table, and classify ten business scenarios against it.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 2 — Fundamentals of Generative AI (24%)
**Task statement:** 2.3 Describe AWS infrastructure and technologies for building generative AI applications
**WSQ mapping:** LU2 · Topic 3 Amazon Bedrock Getting Started · K6 · A2 · LO2
**Slide reference:** v11 deck slides 173–182
**Estimated time:** 35 minutes

**Learning objectives:**
- Distinguish managed AI services, Amazon Bedrock and Amazon SageMaker by what you manage and what you control
- Run the same task through a managed AI service and a foundation model and compare the outputs
- Identify a task only a foundation model can perform, and one only SageMaker can host
- Build a decision table across infrastructure, customisation, output shape, cost model and idle billing
- Classify business scenarios to the correct layer and justify each choice
- Identify which resources in each layer bill continuously and how to delete them

**Prerequisites:**
- Labs 06 to 09 completed
- Access granted to at least one text foundation model in your Region
- Console access to Amazon Comprehend and Amazon SageMaker (read-only is sufficient)

> **Cost warning:** you will **browse** the SageMaker JumpStart catalogue in this lab. **Do not deploy a model.** A JumpStart deployment creates a real-time inference endpoint that bills per instance-hour continuously until deleted, whether or not it receives any requests.

Console entry points: <https://console.aws.amazon.com/bedrock/> · <https://console.aws.amazon.com/comprehend/> · <https://console.aws.amazon.com/sagemaker/>

---

### Step 1 — The three options, and the question that separates them

AWS offers AI capability at three levels of abstraction. Choosing between them is one of the most frequently examined judgements in Domain 2, and one of the most consequential real decisions an architect makes.

| Layer | What you get | What you manage | Typical example |
|---|---|---|---|
| **Managed AI services** | A trained model behind a task-specific API | Nothing — you call an API | Amazon Comprehend, Rekognition, Transcribe, Translate, Textract |
| **Amazon Bedrock** | Foundation models from several providers behind one API | Prompts and data; no infrastructure | Bedrock on-demand inference |
| **Amazon SageMaker (incl. JumpStart)** | The tools to train, tune, host and operate models yourself | The model, the instances, the endpoints, the scaling | SageMaker JumpStart, training jobs, inference endpoints |

Read down the "What you manage" column. **The layers differ by how much you are responsible for**, and responsibility trades off directly against control.

## The question that separates them

> **Does a service already exist that does exactly this task?**
>
> - **Yes** → use the **managed AI service**. It is cheaper, faster to build, needs no ML expertise, and someone else keeps the model current.
> - **No, but a general-purpose foundation model can do it with a good prompt** → use **Bedrock**.
> - **No, and I need a specific model, my own weights, custom training, or control over hosting** → use **SageMaker**.

Most teams get this wrong in one direction: they reach for a foundation model because it is the interesting technology, when a managed service would have solved the problem for less money, with lower latency and with a consistent, testable output.

**The rule to carry into the exam:** *the most specific service that solves the problem is usually the right answer.*

## Cost warning for this lab

You will **browse** these consoles. You will **not deploy** anything.

> **Deploying a model from SageMaker JumpStart creates a real-time inference endpoint that bills per instance-hour continuously — whether or not you send it a single request.** It does not stop when you close the browser tab. The same is true of a SageMaker Studio application or notebook instance. Step 3 and Step 6 return to this.

**Checkpoint:** You can state the one question that separates the three layers, and you know not to deploy anything in this lab.

---

### Step 2 — Option A: a managed AI service (Amazon Comprehend)

Managed AI services are pre-trained models exposed through a task-specific API. You bring data, you get a result. There is no model to choose, no infrastructure, and no ML expertise required.

1. Open the Amazon Comprehend console at <https://console.aws.amazon.com/comprehend/>.
2. Find the real-time analysis area, keep the built-in model selected, and paste this text:

   ```
   The delivery was three days late and nobody answered the phone, but
   the replacement chair arrived quickly and the quality is excellent.
   Order 44192 was placed by Siti Rahman in Singapore on 3 April.
   ```

3. Run the analysis and look at each tab of results:
   - **Sentiment** — a label with confidence scores, not a paragraph of prose
   - **Entities** — people, places, dates, quantities extracted with types and confidence
   - **Key phrases**, **Language**, and **PII** if offered

4. Note what you did **not** do: you did not write a prompt, choose a model, set a temperature, or handle a context window. And note what you **got**: a **structured, typed result with a confidence score**.

## What this layer gives you that a foundation model does not

| Property | Managed AI service | Foundation model |
|---|---|---|
| Output shape | Structured and typed, always | Text you must parse and validate |
| Confidence score | Provided | Not provided — fluent output looks equally confident whether right or wrong |
| Determinism | Same input gives the same output | Varies between runs (Lab 09) |
| Latency | Typically milliseconds | Typically seconds |
| Cost per request | Typically lower | Per token, input and output |
| ML expertise needed | None | Prompt engineering |
| Auditability | Easy — a label and a score | Hard — free text |

> **That confidence score is the sleeper advantage.** It lets you route low-confidence cases to a human automatically. A foundation model gives you no equivalent signal — as Lab 09 demonstrated, a hallucination arrives with exactly the same confident tone as a correct answer.

## Other services in this layer

Recognise these by their task, since the exam tests exactly that mapping:

| Service | Task |
|---|---|
| **Amazon Comprehend** | NLP on text — sentiment, entities, key phrases, language, PII |
| **Amazon Rekognition** | Image and video analysis — objects, faces, moderation, text in images |
| **Amazon Transcribe** | Speech to text |
| **Amazon Polly** | Text to speech |
| **Amazon Translate** | Language translation |
| **Amazon Textract** | Extract text, forms and tables from scanned documents |
| **Amazon Personalize** | Recommendations |
| **Amazon Forecast** | Time-series forecasting |
| **Amazon Fraud Detector** | Fraud detection on transactions |

**The limitation of this layer:** you get exactly the task on offer and nothing else. If you need sentiment classified into your own eleven custom categories, or a summary written in your brand voice, no amount of configuration will produce it. That is when you move up to Bedrock.

**Checkpoint:** You have run text through Comprehend and can state two things its output gives you that a foundation model's does not.

---

### Step 3 — Option B: Bedrock, and Option C: SageMaker JumpStart

## Option B — the same task on Bedrock

1. Open the Bedrock playground at <https://console.aws.amazon.com/bedrock/> and select a text model.
2. Run the **same text** through a foundation model:

   ```
   Analyse the sentiment of this text and extract every person, place,
   date and order number. Return your answer as JSON.

   "The delivery was three days late and nobody answered the phone, but
   the replacement chair arrived quickly and the quality is excellent.
   Order 44192 was placed by Siti Rahman in Singapore on 3 April."
   ```

3. Compare the result with Step 2's:
   - Did you get **valid JSON**, every time? Run it twice and check.
   - Is there a **confidence score**?
   - Was it **faster or slower** than Comprehend?
   - Did it catch the **mixed** sentiment more subtly than a single label?

4. Now run something Comprehend **cannot** do at all:

   ```
   Write a two-sentence apology to this customer in a warm, informal
   tone, referencing their specific complaint. Then classify the
   complaint into exactly one of: DELIVERY_DELAY, PRODUCT_QUALITY,
   SUPPORT_UNREACHABLE, BILLING.
   ```

   **This is the boundary.** Free-form generation, custom categories defined at request time, and reasoning across a task no fixed API was built for. That is Bedrock's territory.

## Option C — SageMaker JumpStart

SageMaker JumpStart is a catalogue of pre-built models — open-weights foundation models, vision models, and classical ML models — that you can deploy **into your own account, on instances you choose and pay for**.

> ### Cost warning — read before clicking
>
> **Browse only. Do not deploy.**
>
> Deploying a JumpStart model creates a **real-time inference endpoint** that bills **per instance-hour, continuously, from creation until you delete it** — regardless of whether you send it any requests. Large model instance types are among the more expensive resources on AWS. An endpoint left running over a weekend is the classic training-course bill.
>
> Opening **SageMaker Studio** may also start an application that bills while it runs. If you open Studio, Step 6 tells you how to shut it down.

1. Open the SageMaker console at <https://console.aws.amazon.com/sagemaker/> and find **JumpStart** in the left navigation.
2. Browse the catalogue **without deploying**. Note that models are grouped by provider and by task.
3. Open the detail page for one model and observe what a deployment would ask you for. This is the important part:
   - **an instance type** — you choose the hardware, and you pay for it by the hour
   - **an instance count** — you choose the scale
   - **an endpoint name** — a persistent resource you own and must delete

   Compare this with Bedrock in Step 3, where you chose a model ID and nothing else.

4. Close the page **without deploying**.

## What you would gain by deploying it

Real reasons organisations choose SageMaker over Bedrock:

- **A specific model** Bedrock does not offer — an open-weights model, a domain-specific model, or one from a research group
- **Your own model** — trained in house, or fine-tuned on proprietary data, with full control of the weights
- **Full control of hosting** — instance type, scaling policy, VPC placement, latency profile
- **Deep customisation** — modifying the model itself, not just prompting it
- **Predictable high-volume economics** — at very high sustained throughput, a reserved instance can beat per-token pricing

And what you take on: instance selection, capacity planning, scaling, patching, monitoring, and an hourly bill that runs whether anyone uses the endpoint or not.

**Checkpoint:** You ran the same task on Comprehend and Bedrock, saw a task only Bedrock can do, and browsed JumpStart **without deploying anything**.

---

### Step 4 — Build the decision table

Fill this in from what you observed in Steps 2 and 3. Complete it yourself **before** reading the model answer below it — the value of this step is in the recall.

| Dimension | Managed AI service | Amazon Bedrock | SageMaker / JumpStart |
|---|---|---|---|
| Infrastructure you manage | | | |
| Model choice | | | |
| Can you use your own model? | | | |
| Customisation available | | | |
| Output shape | | | |
| Confidence score provided? | | | |
| Typical latency | | | |
| Cost model | | | |
| Billing when idle | | | |
| ML expertise required | | | |
| Time to first working result | | | |

---

## Model answer

Check yours against this once you have finished.

| Dimension | Managed AI service | Amazon Bedrock | SageMaker / JumpStart |
|---|---|---|---|
| Infrastructure you manage | None | None | Instances, endpoints, scaling |
| Model choice | None — one model per task | Several providers, one API | Any model, including your own |
| Can you use your own model? | No | Only via supported customisation | Yes — full control of weights |
| Customisation available | Some services support custom classifiers/entities | Prompting, RAG, fine-tuning within the service | Unlimited — train or modify the model |
| Output shape | Structured and typed | Free text you must parse and validate | Whatever your model returns |
| Confidence score provided? | Yes | No | Depends on the model |
| Typical latency | Milliseconds | Seconds | Depends on your instance |
| Cost model | Per request or per unit processed | Per token, in and out | Per instance-hour |
| Billing when idle | Nothing | Nothing (on-demand) | **Bills continuously** |
| ML expertise required | None | Prompt engineering | Substantial |
| Time to first working result | Minutes | Minutes | Hours to weeks |

## The three rows that decide most real arguments

1. **"Billing when idle."** Bedrock on-demand and managed services cost nothing when nobody is using them. A SageMaker endpoint bills all night and all weekend. For anything spiky, low-volume, or in development, this dominates every other consideration.
2. **"Can you use your own model?"** This is usually the *only* thing that forces SageMaker. If the answer is no, you probably do not need SageMaker.
3. **"Confidence score provided?"** If your workflow needs to route uncertain cases to a human automatically, a managed service gives you the signal to do it and a foundation model does not.

## Two nuances worth knowing

- **These layers combine.** A real system might use Textract to read a scanned invoice, Comprehend to detect PII, and Bedrock to summarise the result. The question is rarely "which one" for the whole application — it is "which one for this step".
- **Bedrock is not always the middle option on cost.** At very high sustained volume, per-token pricing can exceed the cost of a permanently busy endpoint. At low or spiky volume, on-demand wins easily. Volume shape, not just volume, decides.

**Checkpoint:** Your decision table is complete and you have compared it against the model answer.

---

### Step 5 — Classify ten scenarios

For each scenario choose **one** primary answer — **Managed service**, **Bedrock**, or **SageMaker** — and write **one sentence** justifying it. The justification matters more than the label; exam questions turn on the reason.

| # | Scenario | Your choice | Why (one sentence) |
|---|---|---|---|
| 1 | A retailer wants sentiment scores on 50,000 product reviews per day, as a number they can chart. | | |
| 2 | A law firm wants to summarise 80-page contracts in the firm's own house style. | | |
| 3 | A hospital has trained its own diagnostic model on proprietary imaging data and must host it inside its own VPC. | | |
| 4 | An insurer needs to read text out of scanned claim forms, including tables. | | |
| 5 | A startup wants a customer support chatbot answering from its own help centre articles. | | |
| 6 | A media company needs to detect inappropriate images uploaded by users. | | |
| 7 | A bank needs a research team to fine-tune an open-weights model on its own data and control the weights entirely. | | |
| 8 | A logistics firm wants to convert recorded driver voice notes into text. | | |
| 9 | An HR team wants to draft job descriptions from a few bullet points, in the company's tone of voice. | | |
| 10 | An e-commerce site wants product recommendations based on user browsing history. | | |

---

## Answers and reasoning

Check yours only after you have committed to all ten.

1. **Managed service** (Comprehend). Sentiment is exactly what it does, it returns a number with a confidence score, and at 50,000 a day the cost and latency advantage over per-token inference is decisive.
2. **Bedrock**. Summarisation in a specific house style is generation with a custom brief — no fixed API offers "summarise like this firm writes".
3. **SageMaker**. Their own model, their own weights, their own VPC. This is the case that forces SageMaker; nothing else can host it.
4. **Managed service** (Textract). Purpose-built for extracting text, forms and tables from scanned documents, and it returns structure rather than prose.
5. **Bedrock**. A chatbot grounded in their own documents is RAG — Knowledge Bases for Amazon Bedrock (Lab 15). Note the retrieval layer may add its own continuously billed vector store.
6. **Managed service** (Rekognition). Content moderation on images is a built-in capability with confidence scores you can threshold.
7. **SageMaker**. "Fine-tune an open-weights model and control the weights entirely" is the definition of the SageMaker case.
8. **Managed service** (Transcribe). Speech to text, purpose-built.
9. **Bedrock**. Open-ended generation from a short brief, in a specified tone. No fixed API does this.
10. **Managed service** (Personalize). Purpose-built recommendations. Note it is the one managed service that trains on *your* data — managed does not always mean one-size-fits-all.

## If you scored badly

The most common error is choosing **Bedrock** for scenarios 1, 4, 6, 8 and 10. A foundation model *could* attempt all of them — and would be slower, more expensive, less consistent, harder to audit, and would give you no confidence score.

> **Re-read the rule from Step 1: the most specific service that solves the problem is usually the right answer.** "It can do it" is not the same as "it should do it".

The second most common error is choosing **SageMaker** whenever the scenario mentions custom data. Custom *data* does not force SageMaker — RAG on Bedrock handles proprietary documents without any hosting. It is custom *model weights* and control over hosting that force SageMaker.

**Checkpoint:** All ten scenarios classified with a written justification, and you can explain any you got wrong.

---

### Step 6 — Clean up

This lab was deliberately designed so that **browsing is all that was required**. If you followed it as written, nothing billable was created. Verify that rather than assuming it.

## 1. SageMaker — the expensive one

If you deployed a JumpStart model despite the warnings, **delete the endpoint now**. It bills per instance-hour continuously, whether or not it receives a single request.

```bash
# Endpoints — these bill per instance-hour until deleted
aws sagemaker list-endpoints --region us-east-1

# Delete any endpoint from this lab
aws sagemaker delete-endpoint --region us-east-1 --endpoint-name <name>

# The endpoint config and model are free to keep, but tidy them anyway
aws sagemaker list-endpoint-configs --region us-east-1
aws sagemaker delete-endpoint-config --region us-east-1 --endpoint-config-name <name>
```

> **Deleting the model or the endpoint config does not stop the charge. Only deleting the *endpoint* does.** This is the single most common and most expensive cleanup mistake in AWS AI training.

Also check for anything that bills by the hour whether idle or not:

```bash
# Notebook instances — bill while "InService", even with no notebook open
aws sagemaker list-notebook-instances --region us-east-1
```

If you opened **SageMaker Studio**, shut down the running applications from within Studio (**File → Shut Down**, or the running terminals and kernels panel). A Studio application keeps billing after you close the browser tab — closing the tab is not shutting it down.

## 2. Bedrock

On-demand inference is serverless — nothing to delete. Confirm you created nothing that is not:

```bash
aws bedrock list-provisioned-model-throughputs --region us-east-1
aws bedrock list-custom-models --region us-east-1
```

Both should be empty. Close the playground tab.

## 3. Comprehend

Real-time analysis in the console creates no persistent resource. If you went further and started a **custom classifier**, a **custom entity recogniser**, an **endpoint**, or an **analysis job**, delete them — custom Comprehend endpoints bill continuously in the same way SageMaker endpoints do.

## 4. Keep your work

The **decision table** from Step 4 and the **ten classified scenarios** from Step 5 are the deliverables of this lab and are among the most exam-relevant notes in Domain 2. Keep them.

## 5. Set a budget

If this is your own account and you have not already, create an **AWS Budget** or billing alert. This lab's cleanup list is exactly the category of resource that surfaces as a surprise at month end rather than at the moment you create it.

**Checkpoint:** `list-endpoints` and `list-notebook-instances` return nothing from this lab, no Studio application is running, Bedrock shows no provisioned throughput or custom models, and your tables are saved.

---

### Verification

- [ ] You can state the one question that separates the three layers
- [ ] You ran the same text through Comprehend and a Bedrock model and compared the outputs
- [ ] You can name two things a managed service's output gives you that a foundation model's does not
- [ ] You ran a task that only a foundation model could do, and can say why Comprehend could not
- [ ] You browsed JumpStart and can list the three things a deployment would ask you for that Bedrock does not
- [ ] The decision table is complete and checked against the model answer
- [ ] All ten scenarios are classified with a one-sentence justification each
- [ ] `list-endpoints` and `list-notebook-instances` show nothing from this lab, no Studio application is running, and Bedrock shows no provisioned throughput or custom models

### Discussion questions

1. A team proposes using a foundation model to classify 50,000 support tickets a day into eight fixed categories. Comprehend custom classification could also do it. Argue both sides on cost, latency, consistency, auditability and effort — then say which you would choose and what would change your mind.
2. Bedrock gives you several providers through one managed API with no servers to run. What does an organisation give up compared with hosting an open-weights model on SageMaker? Consider provider choice, data handling, control of weights, scaling, and how easily they could switch models later.
3. On-demand Bedrock costs nothing when idle; a SageMaker endpoint bills all weekend. Yet some organisations still choose the endpoint. Under what volume and latency conditions does that become the correct decision?

---

---

## Lab 11 — Amazon Q Business Getting Started

Create an Amazon Q Business application, connect it to documents in Amazon S3, and ask questions answered from those documents with citations.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 2 — Fundamentals of Generative AI (24%)
**Task statement:** 2.3 Describe AWS infrastructure and technologies for building generative AI applications
**WSQ mapping:** LU1 · Topic 2 Amazon Q Business Getting Started · K2 · A1 · LO1
**Slide reference:** v11 deck slides 173–182
**Estimated time:** 40 minutes

**Learning objectives:**
- Explain what Amazon Q Business is and how it differs from Amazon Bedrock
- Create a Q Business application and connect an Amazon S3 data source
- Run a sync and interpret the sync history
- Ask questions answered from your own documents, and verify the citations
- Test the boundaries of grounding — out-of-scope questions, false premises, stale documents, per-user permissions
- Explain why permission-aware retrieval is the main reason to buy rather than build an enterprise assistant
- Delete the application and confirm from the API that billing has stopped

**Prerequisites:**
- Labs 06 to 10 completed
- AWS CLI configured, with permissions for Amazon S3 and Amazon Q Business
- Amazon Q Business available in your chosen Region — check the console

> ## Cost warning — read before starting
>
> **Amazon Q Business is not free tier and bills continuously for as long as the application exists**, on a per-user subscription and index capacity basis — not per question asked. Closing the browser does **not** stop the charge; only deleting the application does.
>
> Check the current Amazon Q Business pricing page and accept the charge before you begin, **complete this lab in one sitting**, and delete the application in Step 7 the same day. If you would rather not incur the cost, read Steps 2 to 6 for the concepts — the exam tests what Q Business is and when to use it, not your ability to click through the wizard.

Console entry point: <https://console.aws.amazon.com/amazonq/>

---

### Step 1 — What Amazon Q Business is, and what it will cost you

Amazon Q Business is a **managed generative AI assistant for enterprise data**. You point it at your organisation's content, it indexes that content, and employees ask questions in natural language and get answers **with citations back to the source documents**.

Everything you built by hand in Lab 08 and argued for in Lab 09 — retrieval, grounding, citations — Q Business provides as a managed service. You supply documents and permissions; you do not supply prompts, an embedding model, a vector store or any code.

## Where it sits in Lab 10's framework

| Layer | Example |
|---|---|
| Managed AI service | Comprehend, Rekognition |
| **Managed generative AI application** | **Amazon Q Business** |
| Foundation model API | Amazon Bedrock |
| Build and host it yourself | SageMaker |

Q Business sits **above** Bedrock. Where Bedrock gives you a model and you build the RAG pipeline, Q Business gives you the finished application. You trade control for speed: you cannot choose the model or write the prompt, but you get a working, permission-aware, cited assistant in an afternoon.

## Cost warning — read this before Step 3

> ### Amazon Q Business is not free tier, and it bills continuously.
>
> - A Q Business application is charged on a **per-user subscription** basis, and index capacity is charged for **as long as the application exists** — not per question asked.
> - **Closing the browser does not stop the charge. Only deleting the application does.**
> - This is fundamentally unlike the Bedrock labs, where on-demand inference cost nothing when idle.
>
> **Before you begin, decide which applies to you:**
>
> 1. **You are in a managed classroom account** — your trainer will confirm whether you should create an application or follow along on a shared one.
> 2. **You are using your own account** — check the current Amazon Q Business pricing page and confirm you accept the charge. Then complete the lab **in one sitting** and delete the application in Step 7 the same day.
> 3. **You do not want to incur the cost** — read Steps 2 to 6 for the concepts and skip the creation. The exam tests what Q Business *is* and *when to use it*, not your ability to click through the wizard.
>
> Do not create the application and come back to it tomorrow. That is the decision that produces a bill.

## What Q Business does that a raw model cannot

- **Connects to enterprise data sources** through built-in connectors, rather than you writing ingestion code
- **Respects existing permissions** — a user should only get answers from documents they are already allowed to read. This is the hardest part of enterprise RAG and the main reason to buy rather than build.
- **Cites its sources**, so an answer can be checked (Lab 09's mitigation, built in)
- **Provides a ready-made web experience** with user authentication
- **Declines when the answer is not in the documents** — the grounding behaviour you had to prompt for by hand in Lab 09

**Checkpoint:** You can explain how Q Business differs from Bedrock, and you have made an explicit decision about whether to incur the cost.

---

### Step 2 — Prepare documents in Amazon S3

Q Business needs something to be grounded in. You will create a small set of fictional company documents — deliberately containing facts that **no foundation model could possibly know**, so that when you get a correct answer in Step 5 you know for certain it came from retrieval and not from training data.

## Create a bucket

```bash
REGION=us-east-1
BUCKET=q-business-lab-$(date +%s)

aws s3 mb "s3://$BUCKET" --region "$REGION"
echo "Bucket: $BUCKET"
```

Write the bucket name down. You will need it in Step 4 and again in Step 7.

## Create the documents

```bash
mkdir -p qdocs

cat > qdocs/leave-policy.txt <<'EOF'
NORTHWIND LOGISTICS PTE LTD - ANNUAL LEAVE POLICY (2026)

Full-time employees are entitled to 21 days of paid annual leave per
calendar year. Employees who have completed five years of continuous
service are entitled to 26 days.

Leave requests must be submitted through the Meridian portal at least
14 calendar days before the intended start date. Requests of more than
10 consecutive working days require approval from a department head.

A maximum of 7 unused days may be carried forward into the following
year. Carried-forward days expire on 31 March. Unused days beyond the
carry-forward limit are forfeited and are not paid out.

The leave year runs from 1 January to 31 December.
EOF

cat > qdocs/expense-policy.txt <<'EOF'
NORTHWIND LOGISTICS PTE LTD - EXPENSE REIMBURSEMENT POLICY (2026)

Claims must be submitted within 30 days of the expense being incurred.
Claims submitted after 60 days will not be reimbursed.

Meal allowance while travelling domestically is SGD 45 per day.
International travel meal allowance is SGD 80 per day.

Air travel in economy class is approved by default. Business class
requires prior written approval from a director and is permitted only
for flights exceeding 7 hours.

Taxi and ride-hailing fares are reimbursable. Private vehicle mileage
is reimbursed at SGD 0.62 per kilometre.

All claims over SGD 500 require an itemised receipt.
EOF

cat > qdocs/it-support.txt <<'EOF'
NORTHWIND LOGISTICS PTE LTD - IT SUPPORT GUIDE (2026)

The service desk operates Monday to Friday, 08:30 to 18:30 Singapore
time. Outside these hours, only Priority 1 incidents are handled, via
the on-call number listed in the Meridian portal.

Password resets are self-service through the Meridian portal. Accounts
lock after five failed attempts and unlock automatically after 30
minutes.

Laptop replacement is on a four-year cycle. Requests for early
replacement require a documented hardware fault.

Software installation requires a ticket. Employees do not have local
administrator rights.
EOF
```

Notice what these contain: **21 days of leave, SGD 45 meal allowance, a four-year laptop cycle, five failed login attempts.** These numbers exist nowhere in any model's training data. They are the perfect test of grounding.

## Upload

```bash
aws s3 cp qdocs/ "s3://$BUCKET/docs/" --recursive
aws s3 ls "s3://$BUCKET/docs/"
```

You should see three objects.

> **S3 storage costs are negligible** for three small text files — a few cents a month at most. It is the Q Business application in Step 3, not this bucket, that carries the real cost. You will still delete the bucket in Step 7.

**Checkpoint:** Three text files are in S3 under `docs/`, and you have written down your bucket name.

---

### Step 3 — Create the Amazon Q Business application

> **This is the step that starts the meter.** Re-read the cost warning in Step 1 before continuing. If you decided not to incur the charge, read this step and Steps 4 to 6 for the concepts and go straight to Step 7.

1. Open the Amazon Q Business console at <https://console.aws.amazon.com/amazonq/> and confirm your Region in the selector. Q Business is not offered in every Region — if the console tells you the service is unavailable here, switch to a Region where it is offered.
2. Choose the option to **create an application**.
3. Give the application a name you will recognise later, such as `northwind-lab`.
4. Work through the creation flow. The console will ask you for the following, and the exact wording and ordering change between console versions — follow the **named** item rather than a fixed sequence:

   - **A service role.** Let the console **create a new service role** for you. Q Business needs permission to read from your data sources and write to its index. Note the role name — you may want to remove it in Step 7.

   - **User access and identity.** Q Business identifies users so it can apply document permissions. Depending on the console version this is configured through **AWS IAM Identity Center** or an equivalent identity provider setup. If you have no Identity Center instance, the console will offer to create one.

     > **This is the architecturally important part of the whole lab.** Q Business is user-aware by design. It filters retrieval by what *that user* is permitted to read, so two employees asking the same question can correctly receive different answers. A hand-built RAG system gets this wrong by default — the index does not know who is asking, and every user sees every document. Permission-aware retrieval is the main reason organisations buy this rather than build it.

   - **Index capacity or application tier.** This is the sizing choice that drives cost. Choose the **smallest option offered** — three text files need nothing more. Check the Amazon Q Business pricing page for what each option costs before selecting.

   - **Encryption.** The default AWS-managed key is fine for this lab.

5. Create the application and wait for it to reach an active state. This takes a few minutes.
6. **Write down the application name and its ID.** You need both for Step 7, and Step 7 is the step that stops the charge.

```bash
# Record your application ID now
aws qbusiness list-applications --region "$REGION"
```

**Checkpoint:** The application shows as active, and you have written down its ID.

---

### Step 4 — Connect the S3 data source and sync

An application with no data answers nothing. Now connect it to the documents you uploaded in Step 2.

1. Open your application in the Q Business console and find the **data sources** area.
2. Choose to **add a data source**. Browse the available connectors before picking one.

   Note how many there are. Connectors typically cover S3, web crawlers, document stores, wikis, ticketing systems, chat platforms, CRMs and file shares. **This connector catalogue is a large part of what you are buying** — each one is ingestion code, incremental sync logic and permission mapping that you would otherwise write and maintain yourself.

3. Choose the **Amazon S3** connector.
4. Configure it:
   - **Data source name** — something recognisable, such as `northwind-docs`
   - **IAM role** — let the console create one, so it has read access to your bucket
   - **Bucket and prefix** — your bucket from Step 2, with the prefix `docs/`
   - **Sync schedule** — choose **run on demand**. Do not schedule a recurring sync for a lab; a schedule keeps working on documents you no longer care about.
5. Add the data source, then **start a sync** manually.
6. Wait for the sync to complete. Watch the sync history and note what it reports: how many documents were **scanned**, **added**, **modified**, **deleted** and **failed**.

   > **If documents fail, the assistant will not know about them.** A common cause is the data source role lacking read access to the bucket. Check the sync history rather than assuming success — a Q Business application that answers "I don't know" is far more often a failed sync than a model limitation.

7. Confirm three documents were added successfully.

## What just happened

The sync did, as a managed service, exactly the indexing pipeline you built by hand in Lab 08:

| Lab 08, by hand | Q Business, managed |
|---|---|
| Chunk the documents | Done for you |
| Embed each chunk | Done for you — you do not choose the model |
| Store vectors in a vector store | The Q Business index |
| Track document permissions | Done for you, from the source system's ACLs |
| Re-sync when documents change | The connector's incremental sync |

You gave up all control over chunking strategy, embedding model and retrieval tuning. In exchange you wrote no code and manage no vector store. **That is the trade, and it is the right trade for a standard enterprise knowledge assistant** — Lab 15 shows the Bedrock Knowledge Bases route when you need the control back.

**Checkpoint:** The sync completed and the sync history shows three documents added and none failed.

---

### Step 5 — Ask questions grounded in your documents

1. From your application in the console, open the **web experience** — the console provides a deployed URL for it. You may be asked to sign in with the identity you configured in Step 3.
2. Ask each question below and record the answer **and its citation**.

## Questions with answers in the documents

| # | Question | Answer given | Cited source? | Correct? |
|---|---|---|---|---|
| 1 | How many days of annual leave do I get? | | | |
| 2 | What happens to unused leave at the end of the year? | | | |
| 3 | What is the meal allowance when I travel overseas? | | | |
| 4 | How long do I have to submit an expense claim? | | | |
| 5 | When can I fly business class? | | | |
| 6 | My account is locked. What do I do? | | | |
| 7 | Can I install software on my laptop myself? | | | |

Check each answer against the source text from Step 2. **Every one of these facts is invented and appears nowhere in any model's training data.** A correct answer therefore proves retrieval worked.

## Now test the harder behaviours

**8. A question requiring synthesis across one document:**

```
I have been here six years and want to take three weeks off. How many
days do I have, and what approval do I need?
```

This needs the model to combine the five-year service rule (26 days), the 10-consecutive-day threshold, and the 14-day notice rule. Did it get all three?

**9. A question spanning two documents:**

```
I am travelling overseas for work next month. What do I need to know
about booking and about claiming afterwards?
```

Does it draw on the expense policy for both the booking rules and the claim rules? Does it cite more than one source?

**10. A question phrased in words the documents never use:**

```
I can't get into my account.
```

The IT document says "accounts lock after five failed attempts". Your question says none of those words. If this works, you have watched the semantic retrieval from Lab 08 operating inside a managed service.

## What to look for in every answer

- **Is there a citation?** Q Business is designed to show where an answer came from. Click through and verify the cited passage actually says what the answer claims. This is Lab 09's "cite sources" mitigation, and it is what makes checking cheap enough to actually do.
- **Is the answer complete?** A partial answer that omits a condition — the approval requirement, the deadline — is a real risk in a policy assistant.
- **Is the tone appropriate for an employee-facing tool?**

**Checkpoint:** All ten questions asked, answers and citations recorded, and you have clicked through at least one citation to verify it.

---

### Step 6 — Test the boundaries of grounding

Step 5 showed the system working. This step is more useful: it shows you where it stops. **Knowing where an assistant fails is what qualifies you to deploy one.**

## Test 1 — A question the documents cannot answer

```
What is Northwind Logistics' parental leave entitlement?
```

Your leave policy says nothing about parental leave. Record exactly what happens:

- Did it say it **could not find** the answer? — correct behaviour, and the whole point of grounding
- Did it answer from **general knowledge** about typical parental leave? — this is the failure mode. Note it carefully.
- Did it give a **partial** answer, or bridge from annual leave to parental leave? — subtly the most dangerous outcome, because it looks authoritative

Compare this with Lab 09, where you had to write "if the answer is not in the reference text, say Not found" by hand. A managed assistant should do this by default.

## Test 2 — A question with a false premise

```
Why does the company only give 14 days of annual leave?
```

The policy says **21**. Does the assistant correct the premise, or accept it and explain a policy that does not exist? Accepting false premises is a well-documented failure mode (Lab 09, Step 3) and it appears in grounded systems too.

## Test 3 — A stale-document scenario

You do not need to run this one — reason it through and write your answer:

> Suppose HR updates the leave policy in S3 to 25 days, but nobody triggers a sync and no schedule is configured. What does the assistant tell employees tomorrow?

It confidently gives the **old** answer, with a citation, and the citation makes it *more* convincing. **Grounding guarantees the answer matches the indexed documents. It guarantees nothing about whether those documents are current.**

This is why Step 4 asked you to notice the sync schedule. Operationally: who owns the sync, how often does it run, and how would anyone find out it had been failing for three weeks?

## Test 4 — The permissions question

Also reason this one through:

> Two employees ask "what is the meal allowance?" One is in finance and can read a confidential document listing director-level allowances. One cannot.

In a hand-built RAG system the index typically has no idea who is asking — both users get the same retrieval, and the confidential figure leaks. Q Business filters retrieval by the user's permissions, inherited from the source system's access controls. **The two employees correctly get different answers.**

This is the single strongest technical argument for a managed enterprise assistant, and it is heavily weighted on the exam.

## Record your findings

| Test | What you expected | What actually happened | Implication for deployment |
|---|---|---|---|
| Out-of-scope question | | | |
| False premise | | | |
| Stale documents | *(reasoned)* | | |
| Per-user permissions | *(reasoned)* | | |

**Checkpoint:** All four boundary tests recorded, and you can state what grounding does and does not guarantee.

---

### Step 7 — Clean up

> ## This is the most important cleanup in the course. Do it now, not later.
>
> Unlike every Bedrock lab, **Amazon Q Business bills for as long as the application exists** — per-user subscriptions and index capacity accrue whether or not anyone asks a question. Closing the web experience, closing the browser and signing out of the console all do **nothing**. Only **deleting the application** stops the charge.

## 1. Delete the Q Business application

Deleting the application removes its index, its data source configurations and its web experience together.

**Console:** open the Amazon Q Business console at <https://console.aws.amazon.com/amazonq/>, select your application, and choose **Delete**. Confirm by typing the name if prompted.

**CLI:**

```bash
# Confirm the application ID
aws qbusiness list-applications --region "$REGION"

# Delete it
aws qbusiness delete-application \
  --region "$REGION" \
  --application-id <your-application-id>
```

Then **verify** — do not assume:

```bash
aws qbusiness list-applications --region "$REGION"
```

The output must no longer contain your application. Deletion may take a few minutes; if it still appears, wait and check again. **Do not close your laptop until this list is clear.**

## 2. Delete the S3 bucket

```bash
aws s3 rm "s3://$BUCKET" --recursive
aws s3 rb "s3://$BUCKET"
aws s3 ls | grep q-business-lab   # should return nothing
```

## 3. Remove local files

```bash
rm -rf qdocs
```

## 4. Identity Center and IAM roles

- If the console **created an AWS IAM Identity Center instance** for you in Step 3 and your account had none before, decide whether to keep it. Identity Center itself does not carry a charge in the way the Q Business application does, but an instance you did not intend to create is a governance concern in a shared account. If your organisation was already using Identity Center, **leave it alone** — deleting it affects far more than this lab.
- The **service roles** created in Steps 3 and 4 do not cost anything. Delete them for tidiness if this is your own account; leave them if you are unsure what else might use them. Deleting an IAM role that something else depends on is a worse outcome than leaving an unused role behind.

## 5. Set a budget

If you have not already, create an **AWS Budget** or billing alert on this account. Q Business is exactly the kind of resource that shows up as an unwelcome surprise at month end, because nothing about an idle application looks like it is running.

## Final verification

- [ ] `aws qbusiness list-applications` no longer lists your application
- [ ] The S3 bucket is deleted
- [ ] Local `qdocs` directory removed
- [ ] You have made a deliberate decision about the Identity Center instance and the service roles
- [ ] A budget or billing alert exists on the account

**Checkpoint:** The application is confirmed deleted from the API, not just closed in the browser.

---

### Verification

- [ ] You can explain how Amazon Q Business differs from Amazon Bedrock in what it provides and what it takes away
- [ ] Three documents were uploaded to S3 and the sync history shows three added and none failed
- [ ] You asked the seven document-grounded questions and recorded the answers and citations
- [ ] You clicked through at least one citation and verified the source says what the answer claimed
- [ ] You tested a question that spans two documents and one phrased in words the documents never use
- [ ] You recorded what happened on the out-of-scope question and the false-premise question
- [ ] You can explain what grounding guarantees and what it does not — specifically the stale-document case
- [ ] You can explain why permission-aware retrieval is hard to build and why it is the main reason to buy
- [ ] **`aws qbusiness list-applications` no longer lists your application**, the S3 bucket is deleted, and a budget or billing alert exists

### Discussion questions

1. Amazon Q Business gives you a finished, permission-aware, cited assistant but no control over the model, the prompt, the chunking or the embedding model. Describe a use case where that trade is clearly right, and one where you would build on Bedrock Knowledge Bases instead.
2. HR updates a policy document but the sync never runs. The assistant confidently gives the old answer, with a citation that makes it more convincing. Who owns this failure operationally, and what controls would you put in place to detect it?
3. Two employees ask the same question and correctly receive different answers because of document permissions. Why is this so difficult in a hand-built RAG system, and what could go wrong in a system that ignores it?

---

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.