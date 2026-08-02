# Step 4 — Build the decision table

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
