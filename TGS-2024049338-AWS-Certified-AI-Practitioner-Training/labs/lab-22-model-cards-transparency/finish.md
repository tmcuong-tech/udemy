# Well done!

You have completed Lab 22 — Model Cards and Transparency:

✅ Create a model card and declare intended use
✅ Set the risk rating and record training details
✅ Record evaluation results and caveats
✅ Model cards versus Model Monitor versus Model Registry
✅ AWS AI Service Cards and the transparency you inherit
✅ Clean up

**Key takeaways:**

- A model card records **intended use, out-of-scope uses, risk rating, training details, evaluation results and caveats** — with a named owner, a version and a review date.
- The **out-of-scope** section is the most valuable and most neglected. Every model gets reused by someone who was not in the room; specificity is the only control you have.
- Risk rating follows from **consequence and autonomy**, never from model sophistication. A logistic regression deciding mortgages is high risk; a deep network recommending films is not.
- Evaluation must be **disaggregated by facet group**. A headline accuracy figure hides precisely what the card exists to surface.
- **Registry** answers *which* model, **Model Card** answers *why* this model and what we decided, **Model Monitor** answers *is it still working*. Only Model Monitor bills continuously.
- Model Monitor is what stops a model card becoming a lie over time — bias drift and feature-attribution drift extend Labs 20 and 21 into production.
- **AWS AI Service Cards** are the managed-service equivalent: they document a component you cannot inspect. Accountability for the outcome stays with you.
- Document the **system**, not just the layer you wrote. Inherited limitations are your limitations.

**Next:** Lab 23 — Securing AI Workloads with IAM and KMS
