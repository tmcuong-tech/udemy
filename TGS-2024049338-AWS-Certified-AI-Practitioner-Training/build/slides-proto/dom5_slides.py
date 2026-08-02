# ---------------- DOMAIN 5 — Security, Compliance, and Governance for AI Solutions ----------------
# Raw statements exec'd inside build_slides.py (components + palette in scope).

section("DOMAIN 5","Security, Compliance, and Governance for AI Solutions","14%",sub="Exam weighting 14% · Tasks 5.1–5.2 · Labs 23–25")

# ---- Task 5.1 — Securing AI systems ----
big_statement("Secure the whole AI pipeline, not just the model.",
 "Task 5.1 covers who secures what, how data and models are protected, and how to scope generative-AI risk.",
 "TASK 5.1 · SECURING AI SYSTEMS",color=BLUE)

two_col("AWS Shared Responsibility Model",[
 ("AWS — security OF the cloud",0),
 ("Physical data centres and hardware",1),
 ("Managed infrastructure, compute, storage, networking",1),
 ("Managed service software (e.g. Bedrock, SageMaker)",1)],
 [("You — security IN the cloud",0),
 ("Your data, its classification and encryption",1),
 ("IAM identities, permissions and access",1),
 ("Network and firewall configuration",1)],
 kicker="TASK 5.1 · SHARED RESPONSIBILITY",lhead="AWS responsibility",rhead="Customer responsibility")

picture("Shared Responsibility Model","s300_0.png",
 caption="AWS secures the cloud; the customer secures what they put in it.",kicker="TASK 5.1 · SHARED RESPONSIBILITY")

tile_grid("IAM Least-Privilege for AI",[
 ("IAM Users & Groups","Long-lived identities for people; group permissions by job function."),
 ("IAM Roles","Temporary credentials for services — SageMaker, Bedrock, Lambda assume a role."),
 ("IAM Policies","JSON documents granting only the specific actions each identity needs."),
 ("Least privilege","Start with no access; grant the minimum permissions, then review.")],
 kicker="TASK 5.1 · IDENTITY & ACCESS",cols=2,size=15)

cards3("Access Control for Bedrock & SageMaker",[
 (BLUE,"Scope by service",["Grant only bedrock: or sagemaker: actions needed","Restrict to named models / endpoints","Deny broad admin actions"]),
 (TEAL,"Scope by resource",["Limit to specific S3 buckets and prefixes","Use resource-based policies on data","SageMaker Role Manager builds scoped roles"]),
 (VIOLET,"Protect the root",["Never use the root account for daily work","Enable MFA on all privileged users","Rotate keys; prefer roles over static keys"])],
 kicker="TASK 5.1 · LEAST-PRIVILEGE")

tile_grid("Encryption with AWS KMS",[
 ("At rest","KMS keys encrypt data in S3, EBS, SageMaker volumes and model artifacts."),
 ("In transit","TLS protects data moving between clients, services and endpoints."),
 ("Key control","AWS-managed or customer-managed keys (CMKs) with rotation and policies."),
 ("Auditable","KMS key usage is logged, so you can trace every encrypt/decrypt call.")],
 kicker="TASK 5.1 · KMS ENCRYPTION",cols=2,size=15)

picture("Encryption at Rest","s317_0.png",
 caption="AWS KMS manages the keys that encrypt training data, artifacts and storage volumes.",kicker="TASK 5.1 · KMS")

content("Private Networking with VPC Endpoints",[
 "VPC interface endpoints (AWS PrivateLink) let SageMaker and Bedrock be reached over private AWS network paths.",
 "Traffic stays off the public internet, reducing exposure of data and API calls.",
 "Combine with security groups and subnet controls to isolate training and inference workloads.",
 "SageMaker can run in a VPC with no direct internet access for sensitive projects."],
 kicker="TASK 5.1 · NETWORK ISOLATION")

content("Amazon Macie — Sensitive Data Discovery",[
 "Macie is a managed data-security service that uses ML to discover sensitive data in Amazon S3.",
 "It finds and classifies personally identifiable information (PII) such as names, emails and credit-card numbers.",
 "Automated data-classification jobs surface where sensitive data lives before you train on it.",
 "Findings integrate with your monitoring so you can act on exposure and misconfiguration."],
 kicker="TASK 5.1 · DATA PROTECTION")

picture("Amazon Macie","s319_0.png",
 caption="Macie discovers and classifies PII in S3 so sensitive data is protected before training.",kicker="TASK 5.1 · MACIE")

content("Data & Model Lineage",[
 "Lineage tracks where data came from, how it was transformed, and which model version used it.",
 "Amazon SageMaker ML Lineage Tracking records the steps, datasets and artifacts in a workflow.",
 "Lineage supports reproducibility, auditing and debugging of model behaviour.",
 "It answers governance questions: which data trained this model, and can we trust its provenance?"],
 kicker="TASK 5.1 · LINEAGE")

picture("Amazon SageMaker ML Lineage Tracking","s331_0.png",
 caption="Lineage links datasets, processing steps and model versions for traceability.",kicker="TASK 5.1 · LINEAGE")

tile_grid("Generative AI Security Scoping Matrix",[
 ("Scope 1 — Consumer app","Using a public gen-AI app as-is; least control over data."),
 ("Scope 2 — Enterprise app","A vendor app with enterprise terms and data handling."),
 ("Scope 3 — Pre-trained models","Building on a foundation model via an API (e.g. Bedrock)."),
 ("Scope 4 — Fine-tuned models","Adapting a foundation model with your own data."),
 ("Scope 5 — Self-trained","Training a model from scratch; most control and responsibility.")],
 kicker="TASK 5.1 · SCOPING RISK",cols=1,size=15)

picture("Determine Your Scope","s358_0.png",
 caption="More control means more security responsibility — scope your gen-AI use before you build.",kicker="TASK 5.1 · SCOPING MATRIX")

# ---- Task 5.2 — Governance & compliance ----
big_statement("Prove what happened, and stay compliant.",
 "Task 5.2 covers audit trails, model logging, compliance rules, model governance and data-governance strategy.",
 "TASK 5.2 · GOVERNANCE & COMPLIANCE",color=TEAL)

two_col("CloudTrail vs CloudWatch",[
 ("AWS CloudTrail — the audit trail",0),
 ("Records API activity: who did what, when",1),
 ("Answers 'who called this action, from where'",1),
 ("Used for security auditing and forensics",1)],
 [("Amazon CloudWatch — monitoring",0),
 ("Collects metrics, logs and alarms",1),
 ("Answers 'how is the system performing'",1),
 ("Used for operational health and alerting",1)],
 kicker="TASK 5.2 · AUDIT vs MONITORING",lhead="Audit — who/what/when",rhead="Monitor — health/metrics")

content("Bedrock Model-Invocation Logging",[
 "Amazon Bedrock can log model invocations — the prompts sent and responses returned.",
 "Invocation logs can be delivered to Amazon S3 and/or Amazon CloudWatch Logs.",
 "This gives an audit record of how foundation models are used and what they produced.",
 "Combine with CloudTrail (API calls) for a full picture of access and content."],
 kicker="TASK 5.2 · MODEL LOGGING")

content("AWS Config — Compliance Rules",[
 "AWS Config records the configuration of your resources and how it changes over time.",
 "Config rules continuously evaluate resources against your desired, compliant settings.",
 "Example checks: encryption enabled, public access blocked, logging turned on.",
 "Non-compliant resources are flagged so governance gaps are caught early."],
 kicker="TASK 5.2 · CONFIGURATION COMPLIANCE")

picture("AWS Config","s346_0.png",
 caption="AWS Config continuously checks resources against compliance rules.",kicker="TASK 5.2 · AWS CONFIG")

content("SageMaker Model Registry & Governance",[
 "The SageMaker Model Registry catalogues models, versions and their approval status.",
 "Model groups track versions; approval gates control which models can be deployed.",
 "Metadata and lineage tie each registered model back to its training data and metrics.",
 "This supports repeatable, governed MLOps and clear accountability for what ships."],
 kicker="TASK 5.2 · MODEL GOVERNANCE")

tile_grid("Compliance Standards & Evidence",[
 ("AWS Artifact","On-demand access to AWS compliance reports and agreements."),
 ("Compliance programs","AWS is audited against ISO, SOC, PCI DSS, HIPAA and more."),
 ("Emerging AI standards","New AI-specific regulations and risk frameworks are evolving."),
 ("Shared evidence","Use AWS attestations for your own audits and certifications.")],
 kicker="TASK 5.2 · COMPLIANCE",cols=2,size=15)

flow_h("Data Governance Strategy",[
 "Discover & understand your data (catalog, classify)",
 "Curate — clean and standardise for quality",
 "Protect — encrypt, mask and control access",
 "Manage lifecycle — retention and disposal",
 "Monitor & audit — CloudTrail, Config, Macie"],
 kicker="TASK 5.2 · DATA GOVERNANCE",color=TEAL)

content("Domain 5 — Key Takeaways",[
 "Shared responsibility: AWS secures the cloud; you secure your data, identities and access in it.",
 "Protect AI systems with least-privilege IAM, KMS encryption at rest/in transit, VPC endpoints and Amazon Macie for PII.",
 "Use lineage tracking and the Generative AI Security Scoping Matrix to scope and trace risk.",
 "Govern with CloudTrail (who/what/when audit) vs CloudWatch (monitoring), plus Bedrock model-invocation logging.",
 "AWS Config enforces compliance rules; SageMaker Model Registry, AWS Artifact and a data-governance strategy keep AI accountable."],
 kicker="RECAP")
