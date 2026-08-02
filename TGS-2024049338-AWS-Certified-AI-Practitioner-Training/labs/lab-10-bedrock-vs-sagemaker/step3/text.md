# Step 3 — Option B: Bedrock, and Option C: SageMaker JumpStart

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
