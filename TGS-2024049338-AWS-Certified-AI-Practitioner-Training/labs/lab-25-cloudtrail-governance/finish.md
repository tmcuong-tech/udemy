# Well done!

You have completed Lab 25 — Governance, Audit and Model Lineage:

✅ Generate AI API activity to audit
✅ Inspect a real CloudTrail event: identity, action, timestamp
✅ Create a trail for long-term audit retention
✅ Continuous compliance checking with AWS Config
✅ Model lineage and deployment approval with SageMaker Model Registry
✅ Clean up

**Key takeaways:**

- **AWS CloudTrail records who called the Amazon Bedrock API, which action they called and when** — `userIdentity`, `eventName` and `eventTime` in every event. It does **not** record prompt or completion content; that requires Amazon Bedrock model invocation logging to S3 or CloudWatch Logs. Keep those two mechanisms distinct.
- CloudTrail is an audit service, CloudWatch a monitoring service, and AWS Config a configuration-compliance service. CloudTrail says who did it, Config says whether the result is compliant, CloudWatch says how it is performing.
- Event history is on by default, free, and covers 90 days of management events. A trail is what you create for longer retention, data events, multi-Region coverage and log file validation — the feature that lets you prove logs were not tampered with.
- Failed calls are logged in full, with `errorCode` and `errorMessage`. A burst of access-denied events from one principal is a primary signal of credential misuse.
- AWS Config managed rules such as `sagemaker-notebook-no-direct-internet-access` and `s3-bucket-server-side-encryption-enabled` turn a written policy into continuous, timestamped evidence. Remediation actions and conformance packs scale that across an organisation.
- The SageMaker Model Registry versions every model and gates deployment through an approval status — `PendingManualApproval`, `Approved` or `Rejected` — which supports separation of duties and is itself recorded in CloudTrail.
- AWS Artifact is where you obtain AWS's own compliance reports (SOC, ISO); AWS Audit Manager automates evidence collection against control frameworks. Both cover AWS's side of the shared responsibility model — your Config rules, CloudTrail logs, IAM policies and KMS keys are the evidence for yours.

**Next:** You have completed all 25 labs — review the exam guide and attempt the practice exams.
