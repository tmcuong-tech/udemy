# Step 1 — Create the guardrail and set blocked messages

Amazon Bedrock Guardrails let you apply safety and privacy policies **on top of** a
foundation model, independently of the model itself. That separation is the whole point:
the safety policy is named, versioned, auditable and reusable across models, so swapping
the underlying model does not silently discard your controls.

In responsible-AI terms this step is about **controllability** and **governance** — the
ability to constrain what a deployed system may do, and to prove later what constraints
were in force.

### 1.1 Open the Guardrails console

1. Sign in to the [AWS Management Console](https://console.aws.amazon.com/).
2. Go to the [Amazon Bedrock console](https://console.aws.amazon.com/bedrock/).
3. Confirm the Region selector (top right) is set to a Region where you have Bedrock
   model access. This lab assumes `us-east-1`.
4. In the left navigation, find the safeguards section and choose **Guardrails**.
5. Choose **Create guardrail**.

> **Note:** Creating a guardrail does **not** require model access to be approved. If your
> account is still waiting on model access, you can complete Steps 1–5 in full and return
> for the testing in Step 6 later.

### 1.2 Name the guardrail

1. **Name:** `aif-lab19-guardrail`
2. **Description:** `Lab 19 responsible AI guardrail - TGS-2024049338`
3. Leave optional encryption (KMS) and tagging settings at their defaults unless your
   trainer instructs otherwise.

### 1.3 Write the blocked messages

Two separate messages are configured, and the distinction matters.

| Setting | When it is returned |
|---|---|
| **Blocked message for prompts** | The user's *input* violated a policy — the model was never called. |
| **Blocked message for responses** | The model's *output* violated a policy — the model ran, but its answer was withheld. |

Enter:

- Blocked message for prompts:
  `Your request was blocked by our responsible AI policy. Please rephrase and try again.`
- Blocked message for responses:
  `The response was withheld by our responsible AI policy.`

Choose **Next**.

> **Teaching point:** Guardrails evaluate **both directions**. A learner who only tests
> prompts has exercised half the control surface. You will deliberately test the response
> direction in Step 6.

> **Transparency check:** Notice that the blocked message is *your* wording, not AWS's.
> A vague message ("Error") tells the user nothing; a message that names the policy area
> and offers a route to rephrase or appeal is the more transparent design. Decide what
> your application should say before an incident forces the decision.
