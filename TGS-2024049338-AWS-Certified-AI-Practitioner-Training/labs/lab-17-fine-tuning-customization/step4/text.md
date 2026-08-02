# Step 4 — Provisioned throughput, and why you stop here

> ## ⚠️ DO NOT PURCHASE PROVISIONED THROUGHPUT IN THIS LAB
>
> You may open the configuration screen to see the fields. **Do not choose Purchase, Confirm or Create.** This is the single most expensive action available anywhere in this course, and unlike most AWS resources it may involve a **term commitment you cannot simply delete your way out of**.
>
> If you are in a shared classroom account, do not open the purchase flow at all without your trainer present.

### The constraint that shapes everything

On-demand inference against a base model is **serverless and per-token**. No commitment, no idle cost. That is what every earlier lab in this course used.

**A custom model does not work that way.** Once you fine-tune, you own a model artefact that no shared serving fleet hosts. To invoke it, capacity must be dedicated to you — and you pay for that capacity **whether or not you send it a single request**.

This is purchased as **provisioned throughput**, in **model units**. A model unit represents a quantum of dedicated capacity with an associated throughput ceiling.

### The three things to understand

**1. You pay for time, not for use.** Provisioned throughput bills for the duration it exists. A model unit sitting idle overnight costs the same as one running at capacity. This inverts the economics you have internalised from every other Bedrock lab.

**2. Commitment terms.** Provisioned throughput can be purchased with no commitment or with a longer commitment term at a lower rate. **A term commitment cannot generally be cancelled early.** Choosing a one-month or six-month term to save money is a decision you live with for that period. Read the terms shown on screen carefully.

**3. It is the dominant cost of fine-tuning.** Teams routinely budget for the training job — a one-off — and are surprised by serving. **Serving is the recurring cost, and it is usually much larger over any realistic time horizon.**

### Do the arithmetic yourself

Rather than quote figures that would be out of date, look them up:

1. Open the official Amazon Bedrock pricing page and find the provisioned throughput rates for a model in your Region.
2. Compute the cost of **one model unit for one month with no commitment**.
3. Find the on-demand price per thousand input and output tokens for the same model family.
4. Work out **how many on-demand requests you could make for the same money**, using your own estimate of tokens per request.

Almost everyone is surprised by the answer. Write your number down; it is the most useful thing you will take from this step.

### The break-even question

Provisioned throughput becomes rational at **sustained high volume**. The reasoning:

- On-demand cost scales **linearly** with requests. Ten times the traffic, ten times the bill.
- Provisioned cost is **flat**. Ten times the traffic on the same units costs the same, until you hit the throughput ceiling.

So there is a crossover. **Below it, on-demand wins. Above it, provisioned wins.** And an intermittent workload — busy for two hours, idle for twenty-two — sits badly on provisioned throughput, because you pay for the idle twenty-two.

Note that provisioned throughput is also available for **base** models, where it buys predictable latency and guaranteed capacity rather than being a precondition for using the model at all. For a custom model it is not a choice — it is the only path to inference.

### What this means for the customisation decision

Now revisit Step 1 with this knowledge. The full cost of fine-tuning is:

```
data curation and labelling   (weeks of human effort — usually the largest hidden cost)
+ training job                (one-off compute)
+ provisioned throughput      (RECURRING, and it dominates)
+ retraining                  (when the base model version moves on)
+ evaluation                  (Lab 18 — you must prove it improved anything)
```

Against prompt engineering, whose cost is an afternoon of an engineer's time and some extra tokens per call.

> **The exam-relevant conclusion.** When a question describes a team wanting to customise a model and asks for the most cost-effective approach, the presence of provisioned throughput in the fine-tuning path is usually what decides it. Fine-tuning is justified by **sustained high volume** plus a behavioural requirement that prompting genuinely cannot meet — not by a preference for having a custom model.

### Verify you purchased nothing

```bash
aws bedrock list-provisioned-model-throughputs --region us-east-1
```

**This must return empty.** If it does not, go to Step 6 immediately.

**Checkpoint:** You can explain why a custom model cannot be served on demand, you have calculated the on-demand equivalent of one model unit for one month, and `list-provisioned-model-throughputs` returns empty.
