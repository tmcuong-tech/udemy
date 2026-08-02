# Well done!

You have completed Lab 21 — Explainability and Feature Attribution:

✅ Global versus local explanations
✅ SHAP feature attribution and the baseline
✅ Configure a Clarify explainability analysis
✅ Read and interpret a feature attribution report
✅ Performance versus interpretability, and when to reject the better model
✅ Clean up

**Key takeaways:**

- **Global** explanations serve developers and governance; **local** explanations serve the affected individual and any appeals process. Governance needs both.
- SHAP attributions are **signed** and **additive**, so they show direction as well as importance and account fully for the gap from the baseline.
- The **baseline defines the counterfactual**. Change it and every attribution changes, so it must be documented alongside any figure you quote.
- SHAP tells you what the **model** used, not what **causes** the outcome. Correlated features split credit unpredictably, and attribution is never causation.
- A **post-hoc explanation is not equivalent to an interpretable model** — it is an approximation that can itself be wrong, which is exactly the weakness a challenge will target.
- Reject the more accurate model when decisions are regulated, contestable, or severe in consequence. Frame the choice as the cost of an unexplainable decision multiplied by how often you will be asked.
- Explainability does not make decisions defensible; it makes them **discussable** by the people accountable for them.

**Next:** Lab 22 — Model Cards and Transparency
