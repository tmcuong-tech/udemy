# Well done!

You have completed Lab 20 — Bias Detection with SageMaker Clarify:

✅ Frame the fairness question: facet, label and positive outcome
✅ Pre-training bias metrics: measuring the data
✅ Post-training bias metrics: measuring the model
✅ Path 1: run a Clarify bias job against your own model
✅ Path 2: guided walkthrough of a bias report
✅ Clean up

**Key takeaways:**

- A bias analysis is meaningless without a stated **facet**, **facet value**, **label** and **positive label value**. Clarify forces you to declare all four.
- **Pre-training** metrics measure the dataset and need no model. **Post-training** metrics measure predictions and require a model — which is why they cost money.
- **Class Imbalance** asks whether groups are equally represented; **Difference in Proportions of Labels** asks whether the training labels already favour one group.
- A model can score well post-training simply by faithfully reproducing bias in the labels. Run **both phases** or you will congratulate yourself on inherited unfairness.
- When the prediction gap exceeds the label gap, the model has **amplified** bias — visible only by comparing the two phases.
- **Error-rate** gaps matter more than approval-rate gaps because they identify who is harmed and how. Which error is worse is a domain judgement, not a technical one.
- There is no universal fairness threshold. Acceptable ranges are a documented policy decision, not a number a data scientist picks alone.
- Removing a sensitive column does not remove the bias if proxies remain — "fairness through unawareness" fails.

**Next:** Lab 21 — Explainability and Feature Attribution
