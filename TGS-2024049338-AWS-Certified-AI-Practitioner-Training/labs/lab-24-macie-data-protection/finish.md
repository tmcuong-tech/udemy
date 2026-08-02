# Well done!

You have completed Lab 24 — Data Protection with Amazon Macie:

✅ Why PII must never reach training data or prompts
✅ Create a bucket and upload synthetic sample data
✅ Enable Amazon Macie
✅ Create a custom data identifier and run a discovery job
✅ Read the findings and turn them into data controls
✅ Clean up

**Key takeaways:**

- Amazon Macie discovers sensitive data **in Amazon S3, at rest**, using managed and custom data identifiers. Amazon Comprehend detects PII entities **in text you pass to it**. Match the verb and the location — this pairing appears repeatedly in exam questions.
- Macie is a detective control. It finds and reports; it does not block, redact or delete. Turning a finding into prevention means EventBridge, Lambda, bucket policies or a pipeline gate that you build.
- Discovery jobs are charged by the volume of data inspected, so control scope deliberately — pick specific buckets and prefixes, use the sampling depth setting, and prefer one-time jobs over scheduled ones. The free bucket inventory tells you a bucket's size before you commit to scanning it.
- A finding gives you the exact object key and the line or offset of each occurrence, which is what makes remediation scriptable rather than manual.
- Detection is tuned against false positives and depends on surrounding context, so an empty result is not proof that a dataset is clean. Custom data identifiers with proximity keywords cover organisation-specific formats that managed identifiers cannot know about.
- Findings are retained in Macie for 90 days and are deleted when Macie is disabled; export to S3 if you need longer-lived audit evidence. Macie also publishes to EventBridge and Security Hub automatically.
- Data protection for AI is layered: redact before storage, discover and encrypt at rest, guard at inference with Bedrock Guardrails, and audit afterwards with CloudTrail. No single control is sufficient on its own.

**Next:** Lab 25 — Governance, Audit and Model Lineage
