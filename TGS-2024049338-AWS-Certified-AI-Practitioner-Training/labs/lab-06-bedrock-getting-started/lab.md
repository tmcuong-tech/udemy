# Lab 06 — Amazon Bedrock Getting Started

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

## Step 1 — Open Amazon Bedrock and choose a Region

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

## Step 2 — Request access to foundation models

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

## Step 3 — Explore the model catalogue

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

## Step 4 — Run your first prompt in the playground

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

## Step 5 — See the same catalogue from the AWS CLI

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

## Step 6 — Clean up

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

## Verification

- [ ] You can name the Region you worked in and explain why Region matters for model availability
- [ ] The **Model access** page shows access granted for at least two models from two different providers
- [ ] You recorded provider, modality and stated use case for three catalogue models
- [ ] You can point to where a model ID is shown and explain that model IDs are versioned
- [ ] You ran at least two prompts in the playground and recorded observations for one
- [ ] You can state the difference between the `bedrock` and `bedrock-runtime` API namespaces
- [ ] `list-provisioned-model-throughputs` and `list-custom-models` return empty, and the playground tab is closed

## Discussion questions

1. Model access is granted per account, per Region, per model, and some providers require use case details first. What business and governance problem is this control solving, and who in an organisation should own the decision?
2. Bedrock gives you several providers behind one managed API with no servers to run. What does an organisation gain, and what does it give up, compared with hosting an open-weights model on its own infrastructure? Consider operational effort, scaling, data handling, and the ability to switch models later.
3. On-demand Bedrock inference leaves nothing running, yet Provisioned Throughput, custom models and Knowledge Bases all bill continuously. Why does that distinction matter more in a training account than the per-token cost of the prompts you ran today?

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.
