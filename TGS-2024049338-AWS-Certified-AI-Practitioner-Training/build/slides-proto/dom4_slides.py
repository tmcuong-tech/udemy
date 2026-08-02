# ============================================================ DOMAIN 4
# Guidelines for Responsible AI (14%) · Tasks 4.1–4.2 · Labs 19–22
section("DOMAIN 4","Guidelines for Responsible AI","14%",sub="Exam weighting 14% · Tasks 4.1–4.2 · Labs 19–22")

# ---------------- Task 4.1 — Developing responsible AI systems ----------------
big_statement("Responsible AI is a design requirement, not an afterthought.",
 "Fairness, transparency and safety must be built into data, models and operations across the whole lifecycle.",
 "TASK 4.1 · WHY IT MATTERS",color=VIOLET)

tile_grid("Core Dimensions of Responsible AI",[
 ("Fairness","Treat groups equitably; avoid discriminatory outcomes."),
 ("Explainability","Show why a model produced a result."),
 ("Robustness","Perform reliably on edge cases and adversarial input."),
 ("Privacy & security","Protect data and guard the model from misuse."),
 ("Governance","Policies, roles and oversight across the lifecycle."),
 ("Transparency","Communicate capabilities, limits and intended use."),
 ("Veracity","Ground outputs in fact; limit hallucination."),
 ("Safety","Prevent harmful, unsafe or unintended behaviour."),
 ("Controllability","Keep humans able to steer and override.")],
 kicker="TASK 4.1 · THE NINE DIMENSIONS",cols=3,size=13)

two_col("Bias and Variance",[
 ("Bias — error from over-simplifying",0),
 ("High bias → underfitting; model misses real patterns",1),
 ("Also unfairness: skewed outcomes across groups",1),
 ("Fix: richer features, more capable model",1)],
 [("Variance — sensitivity to the training data",0),
 ("High variance → overfitting; memorises noise",1),
 ("Poor generalisation to new data",1),
 ("Fix: more data, regularisation, simpler model",1)],
 kicker="TASK 4.1 · MODEL ERROR",lhead="Bias",rhead="Variance")

cards3("Where Bias Creeps In",[
 (BLUE,"Data bias",["Unrepresentative sampling","Skewed / imbalanced classes","Historical labels bake in bias"]),
 (TEAL,"Model bias",["Feature selection choices","Proxy variables for protected traits","Objective favours majority"]),
 (VIOLET,"Human bias",["Labelling & annotation bias","Cognitive bias in review","Biased feedback loops"])],
 kicker="TASK 4.1 · SOURCES OF BIAS")

picture("Responsible Dataset Preparation","s277_0.png",
 caption="Inclusive, diverse, balanced data with consent, privacy protection and regular audits.",
 kicker="TASK 4.1 · RESPONSIBLE DATA")

tile_grid("Building a Responsible Dataset",[
 ("Inclusivity","Represent diverse populations and perspectives."),
 ("Diversity","Wide range of attributes to avoid bias."),
 ("Balanced datasets","Equal representation; avoid skew."),
 ("Privacy protection","Safeguard sensitive data; meet regulations."),
 ("Consent & transparency","Informed consent; clear data-usage notice."),
 ("Regular audits","Periodic reviews to catch bias and issues.")],
 kicker="TASK 4.1 · DATA PRACTICES",cols=3,size=13)

big_statement("Generative AI adds new risks.",
 "Hallucination, toxic or biased output, prompt injection, data privacy leaks and exposure of proprietary algorithms all need guarding.",
 "TASK 4.1 · GENERATIVE AI RISKS",color=AMBER)

cards3("Amazon Bedrock Guardrails",[
 (BLUE,"Content filters",["Filter hate, insults, sexual, violence","Adjustable strength per category","Screen both prompts and responses"]),
 (TEAL,"Denied topics",["Block subjects you define","e.g. religion, guns, legal advice","Keep the model on-topic"]),
 (VIOLET,"Sensitive info & words",["Detect and redact PII","Block words and phrases","Return a custom blocked message"])],
 kicker="TASK 4.1 · BEDROCK GUARDRAILS")

picture("Guardrails for Amazon Bedrock","s283_0.png",
 caption="Content filters and denied topics screen the request before it reaches the model.",
 kicker="TASK 4.1 · BEDROCK GUARDRAILS")

content("SageMaker Clarify — Bias Detection",[
 "Amazon SageMaker Clarify measures potential bias in data and models across the lifecycle.",
 "Pre-training metrics inspect the dataset before you train — e.g. class imbalance and label imbalance across groups.",
 "Post-training metrics inspect the trained model's predictions for disparate outcomes across groups.",
 "Clarify runs as a processing job: it reads the dataset and configuration from Amazon S3 and writes analysis results back.",
 "Use the findings to rebalance data, adjust features and document residual bias."],
 kicker="TASK 4.1 · SAGEMAKER CLARIFY")

picture("Amazon Clarify Processing Jobs","s280_0.png",
 caption="Clarify reads data and config from S3, queries the model endpoint, and writes analysis results back to S3.",
 kicker="TASK 4.1 · SAGEMAKER CLARIFY")

# ---------------- Task 4.2 — Transparency & explainable models ----------------
big_statement("Transparency lets people trust and challenge AI.",
 "Explain how models reach decisions, document their intended use and limits, and keep a human in control.",
 "TASK 4.2 · TRANSPARENT & EXPLAINABLE MODELS",color=VIOLET)

two_col("Interpretability vs Explainability",[
 ("Interpretability",0),
 ("More transparent — see the internal mechanics",1),
 ("Uses inherently interpretable algorithms",1),
 ("Deep understanding, but performance trade-offs",1)],
 [("Explainability",0),
 ("Less transparent — high-level understanding",1),
 ("Model-agnostic (black-box) approach",1),
 ("Explains outputs without opening the model",1)],
 kicker="TASK 4.2 · TWO LENSES",lhead="Interpretability",rhead="Explainability")

picture("Interpretability Compared to Performance","s287_0.png",
 caption="Simpler, interpretable models are more transparent; complex models often trade interpretability for performance.",
 kicker="TASK 4.2 · THE TRADE-OFF")

tile_grid("Explaining Model Predictions",[
 ("Feature attributions","How much each feature drives a prediction."),
 ("SHAP values","Shapley-based, model-agnostic attribution."),
 ("Partial dependence plots","Effect of a feature across its range."),
 ("SageMaker Clarify","Computes explainability alongside bias.")],
 kicker="TASK 4.2 · EXPLAINABILITY TECHNIQUES",cols=2,size=15)

picture("SageMaker Clarify — Model Explainability","s290_0.png",
 caption="Global SHAP values rank feature importance; partial dependence shows how a feature shifts predictions.",
 kicker="TASK 4.2 · SAGEMAKER CLARIFY")

tile_grid("Documenting Models for Transparency",[
 ("SageMaker Model Cards","Record model details, intended use, training data and risk rating in one place."),
 ("AWS AI Service Cards","AWS transparency docs on the intended use, limits and responsible-AI design of its AI services."),
 ("Purpose","Give stakeholders a clear, shareable record of what a model does and does not do.")],
 kicker="TASK 4.2 · TRANSPARENCY ARTIFACTS",cols=3,size=13)

two_col("Human-Centred Design & Oversight",[
 ("Human-centred principles",0),
 ("Prioritise human needs and values in design",1),
 ("Bring in diverse perspectives and expertise",1),
 ("Enhance — not replace — human abilities",1)],
 [("AWS tools that keep humans in the loop",0),
 ("Amazon A2I — human review of predictions",1),
 ("SageMaker Ground Truth — human data labelling",1),
 ("RLHF — align models to human feedback",1)],
 kicker="TASK 4.2 · HUMAN-CENTRED AI",lhead="Design",rhead="AWS tools")

# ---------------- Recap ----------------
content("Domain 4 — Key Takeaways",[
 "Responsible AI spans nine dimensions: fairness, explainability, robustness, privacy & security, governance, transparency, veracity, safety and controllability.",
 "Manage bias (underfitting/unfairness) and variance (overfitting); bias enters through data, model and human choices.",
 "Build responsible datasets — inclusive, diverse, balanced, consented, private and regularly audited.",
 "Amazon Bedrock Guardrails apply content filters, denied topics and PII/word filters; SageMaker Clarify detects pre- and post-training bias.",
 "Explainability (SHAP, feature attributions, partial dependence via Clarify) trades off against performance; document models with SageMaker Model Cards and AWS AI Service Cards, and keep humans in the loop with A2I, Ground Truth and RLHF."],
 kicker="RECAP")
