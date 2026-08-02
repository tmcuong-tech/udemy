# Lab 17 — Fine-Tuning and Model Customisation

Prepare a fine-tuning dataset and walk through a Bedrock custom model job configuration without submitting it, then decide between prompt engineering, RAG, fine-tuning and continued pre-training on cost, effort and data.

> ## ⚠️ DO NOT SUBMIT THE JOB AND DO NOT PURCHASE PROVISIONED THROUGHPUT
>
> A Bedrock custom model cannot be invoked on demand — serving it requires **provisioned throughput**, which is far more expensive than anything else in this course, bills whether or not you use it, and may commit you for a term you cannot cancel.
>
> **Fill in every configuration screen and stop at the final button.** Everything examinable here lives in the configuration and the trade-off analysis, not in running the job.

**What you will do:**
- Compare the four customisation options on weights, data, labelling, time, cost and citations
- Build valid JSONL training and validation datasets and apply the data quality rules that decide success
- Walk every field of a Bedrock custom model job — epochs, learning rate, overfitting — and stop before submitting
- Work out for yourself why provisioned throughput dominates the cost of fine-tuning
- Choose the cheapest sufficient approach across five scenarios and justify each choice
