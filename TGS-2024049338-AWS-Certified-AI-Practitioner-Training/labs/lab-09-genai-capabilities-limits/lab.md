# Lab 09 — Generative AI Capabilities and Limitations

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

## Step 1 — Capabilities: summarisation and generation

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

## Step 2 — Capabilities: translation and code

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

## Step 3 — Produce a hallucination yourself and record it

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

## Step 4 — The other four limitations

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

## Step 5 — Mitigations: grounding, review and scoping

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

## Step 6 — Clean up

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

## Verification

- [ ] The capability table has four rows — summarisation, generation, translation, code — each noting something the model did imperfectly
- [ ] You can state the property shared by the tasks that succeeded (the source material was in the prompt)
- [ ] **You produced a hallucination and recorded the false claim verbatim**, with how you verified it and whether a non-expert would have caught it
- [ ] You re-ran the prompt asking the model to admit ignorance, and can explain why that is not a guarantee
- [ ] The limitations table is complete for non-determinism, knowledge cutoff, bias, and cost/latency with your own observations
- [ ] You re-ran your hallucination prompt with grounding and recorded what changed
- [ ] The mitigations table names what each mitigation does **not** fix
- [ ] Playground closed, and no Knowledge Base, vector store, provisioned throughput or custom model exists

## Discussion questions

1. Based only on what you observed, name two things the model did genuinely well and two it did poorly. A customer asks you to guarantee the answers are factually correct every time. What do you tell them, and what does that imply for how the solution must be designed?
2. Describe a business task where a generative foundation model would be a worse choice than a rule, a database query or a classical ML model. Weigh cost per request, latency, auditability, consistency, and whether the task actually requires generating new language at all.
3. Grounding with RAG is the primary defence against hallucination, but a grounded system can still be confidently wrong. Give two ways that happens, and say what else must be in place before such a system faces customers.

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.
