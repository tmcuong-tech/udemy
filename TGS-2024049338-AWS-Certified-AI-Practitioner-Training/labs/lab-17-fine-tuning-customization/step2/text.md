# Step 2 — Prepare a fine-tuning dataset

Most of the effort and most of the risk in fine-tuning lives here, not in the training job. A team that budgets for compute and not for data preparation has mis-planned the project.

### The format

Bedrock fine-tuning datasets are **JSONL** — JSON Lines. One complete JSON object per line, no commas between lines, no wrapping array. A single stray blank line or trailing comma fails validation.

For text-to-text fine-tuning each record pairs an input with the desired output. The exact key names depend on the model you are customising — **the console shows the required schema for your selected model, and that is the authoritative source.** A common shape is:

```json
{"prompt": "Classify: My card was charged twice.", "completion": "BILLING"}
{"prompt": "Classify: The app crashes on the reports tab.", "completion": "TECHNICAL"}
{"prompt": "Classify: Please change my profile email.", "completion": "ACCOUNT"}
```

Do not type key names from memory in an exam or in production — read the schema the console shows for the model you picked.

### Build a small dataset

Create `northwind-train.jsonl`. Use the Lab 13 triage task, with the completion being the structured record you want the model to learn to produce.

```json
{"prompt": "Assess this delivery complaint: My frozen seafood arrived at room temperature. Order value 180 dollars.", "completion": "{\"category\":\"DAMAGE\",\"severity\":\"HIGH\",\"refund_warranted\":\"YES\",\"summary\":\"Perishable shipment arrived at ambient temperature; temperature excursion.\"}"}
{"prompt": "Assess this delivery complaint: The box was dented but the contents seem fine.", "completion": "{\"category\":\"DAMAGE\",\"severity\":\"LOW\",\"refund_warranted\":\"NO\",\"summary\":\"Cosmetic packaging damage; contents undamaged.\"}"}
{"prompt": "Assess this delivery complaint: I ordered a laptop stand and received a keyboard. Value 620 dollars.", "completion": "{\"category\":\"WRONG_ITEM\",\"severity\":\"MEDIUM\",\"refund_warranted\":\"NEEDS_REVIEW\",\"summary\":\"Incorrect item despatched; value above review threshold.\"}"}
```

Note that the JSON in `completion` is escaped, because it is a string value inside the outer JSON object. Getting this wrong is one of the most common validation failures.

Also create a small `northwind-validation.jsonl` in the same format with **different** examples. Validation data must never overlap with training data — if it does, your reported validation loss is measuring memorisation, and it will look excellent while telling you nothing.

Upload both:

```bash
aws s3 cp northwind-train.jsonl      s3://<your-bucket>/finetune/
aws s3 cp northwind-validation.jsonl s3://<your-bucket>/finetune/
```

Three records will not train anything useful. This is a format exercise — the volume discussion follows.

### How much data do you actually need?

There is no universal number, and any specific figure you have memorised is probably wrong for your model. What you can rely on:

- Fine-tuning needs **substantially more** than few-shot prompting — hundreds to thousands of examples rather than three to five.
- Bedrock enforces **minimum and maximum record counts that vary by model**. The console states the limits for your selected model; read them there.
- **Quality dominates quantity.** A few hundred consistent, correct examples beat several thousand noisy ones. Inconsistent labelling is worse than less data, because you are actively teaching the model to be inconsistent.

### Data quality rules that decide success or failure

1. **Be consistent.** If two near-identical complaints carry different labels, you are teaching contradiction. Have a second person re-label a sample and measure agreement before training.
2. **Represent your real distribution.** Training only on clear-cut cases produces a model that fails on exactly the ambiguous ones you needed help with.
3. **Cover every output class.** An absent class will effectively never be produced.
4. **Match the format exactly.** Every completion must have identical structure. Fine-tuning is highly sensitive to formatting inconsistency — this is what it learns most readily.
5. **Split train and validation properly.** No overlap, and validation should reflect the same distribution.
6. **Remove PII and sensitive data.** This is a governance requirement, and it is more serious than for RAG: RAG context is transient, but **fine-tuning data is absorbed into the weights**. You cannot delete a record from a trained model — you retrain. Amazon Macie can help identify sensitive data in S3 before training; see Lab 24.
7. **Check for bias.** Historical labelling reflects historical decisions, including biased ones. Fine-tuning bakes them in and makes them harder to detect. SageMaker Clarify addresses this; see Lab 20.
8. **Know your data provenance and licensing.** Confirm you have the right to train on it.

> **This is the honest cost of fine-tuning.** Curating, labelling, checking and de-biasing a dataset takes a team weeks. It is usually the largest line item, and it is almost always underestimated in project plans.

**Checkpoint:** Valid JSONL training and validation files created and uploaded, with no overlap between them, and you can list at least five data quality rules.
