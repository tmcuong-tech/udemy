# Lab 07 — Comparing Foundation Models and Inference Parameters

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

## Step 1 — Set up the comparison and run the first model

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

## Step 2 — Run the identical prompt on a second model

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

## Step 3 — Baseline at low temperature: seeing non-determinism

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

## Step 4 — Raise temperature, then narrow top-P

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

## Step 5 — Max tokens: truncation is not brevity

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

## Step 6 — Clean up

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

## Verification

- [ ] The model comparison table has at least two rows, from two different providers, for one identical prompt
- [ ] You wrote down which answer you would put in front of a customer, and why
- [ ] The parameter observation table has three low-temperature rows and three high-temperature rows for the same model and prompt
- [ ] You observed that repeated runs at low temperature are more similar than repeated runs at high temperature
- [ ] You can state the difference between temperature and top-P in your own words
- [ ] You observed a response truncated mid-sentence by a small max tokens value
- [ ] You produced a short *and complete* answer by asking for brevity in the prompt instead
- [ ] Parameters reset, playground closed, no provisioned throughput or custom models exist

## Discussion questions

1. Two models gave different answers to your identical prompt. How would you decide which one to ship, and what would you need to measure beyond "which one reads better"? Consider instruction-following, latency, cost per token and consistency across many inputs.
2. A colleague sets max tokens to a small value and reports that "the model gives short answers now". What is actually happening, what will the user see, and how would you fix it properly?
3. A compliance team asks you to guarantee that a customer-facing assistant returns the identical answer to the identical question every time. Can temperature 0 deliver that guarantee? What would you propose instead, and what does this tell you about where generative models belong in a solution?

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.
