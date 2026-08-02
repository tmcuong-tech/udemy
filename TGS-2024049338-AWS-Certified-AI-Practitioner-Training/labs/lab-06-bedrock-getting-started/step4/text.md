# Step 4 — Run your first prompt in the playground

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
