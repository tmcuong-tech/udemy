# Well done!

You have completed Lab 17 — Fine-Tuning and Model Customisation:

✅ The customisation decision
✅ Prepare a fine-tuning dataset
✅ Configure a custom model job — do not submit
✅ Provisioned throughput, and why you stop here
✅ Apply the decision to real scenarios
✅ Clean up

**Key takeaways:**

- Four options, ascending in cost: **prompt engineering → RAG → fine-tuning → continued pre-training**. The exam usually wants the cheapest one that actually solves the stated problem.
- **Fine-tuning is supervised** on labelled prompt–completion pairs. **Continued pre-training is unsupervised** on a large unlabelled domain corpus. Labelled task examples means fine-tuning; a raw document corpus means continued pre-training.
- **RAG changes what the model knows; fine-tuning changes how it behaves.** They combine — a production system often does both.
- Fine-tuning **cannot cite sources** and cannot be updated without retraining. Frequent change or a citation requirement rules it out on its own.
- Training data is **JSONL**, one object per line, with the schema shown in the console for your chosen base model. Validation data must never overlap training data, or your validation loss measures memorisation.
- **Data quality beats data quantity.** Inconsistent labels are worse than fewer labels, because you actively teach the model to be inconsistent.
- **Overfitting** is the model learning training examples so specifically that it generalises worse. The tell is training loss falling while validation loss flattens or rises.
- Your custom model derives from a **specific base model version**. When the provider moves on, customisation does not carry over — retraining is recurring maintenance.
- **A Bedrock custom model cannot be invoked on demand.** Serving requires **provisioned throughput** in model units, which bills for time rather than use and may carry a non-cancellable term. This inverts Bedrock's usual serverless economics and is usually the deciding factor in a cost question.
- **Training data is absorbed into the weights.** Unlike transient RAG context, it cannot be deleted from a trained model — you retrain. Screen for PII and bias *before* training, not after.

**Next:** Lab 18 — Evaluating Foundation Model Performance
