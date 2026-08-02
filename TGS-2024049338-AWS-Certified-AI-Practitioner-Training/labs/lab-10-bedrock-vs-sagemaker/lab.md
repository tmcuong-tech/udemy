# Lab 10 — Choosing Bedrock, SageMaker JumpStart or a Managed Service

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

## Step 1 — The three options, and the question that separates them

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

## Step 2 — Option A: a managed AI service (Amazon Comprehend)

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

## Step 3 — Option B: Bedrock, and Option C: SageMaker JumpStart

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

## Step 4 — Build the decision table

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

## Step 5 — Classify ten scenarios

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

## Step 6 — Clean up

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

## Verification

- [ ] You can state the one question that separates the three layers
- [ ] You ran the same text through Comprehend and a Bedrock model and compared the outputs
- [ ] You can name two things a managed service's output gives you that a foundation model's does not
- [ ] You ran a task that only a foundation model could do, and can say why Comprehend could not
- [ ] You browsed JumpStart and can list the three things a deployment would ask you for that Bedrock does not
- [ ] The decision table is complete and checked against the model answer
- [ ] All ten scenarios are classified with a one-sentence justification each
- [ ] `list-endpoints` and `list-notebook-instances` show nothing from this lab, no Studio application is running, and Bedrock shows no provisioned throughput or custom models

## Discussion questions

1. A team proposes using a foundation model to classify 50,000 support tickets a day into eight fixed categories. Comprehend custom classification could also do it. Argue both sides on cost, latency, consistency, auditability and effort — then say which you would choose and what would change your mind.
2. Bedrock gives you several providers through one managed API with no servers to run. What does an organisation give up compared with hosting an open-weights model on SageMaker? Consider provider choice, data handling, control of weights, scaling, and how easily they could switch models later.
3. On-demand Bedrock costs nothing when idle; a SageMaker endpoint bills all weekend. Yet some organisations still choose the endpoint. Under what volume and latency conditions does that become the correct decision?

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.
