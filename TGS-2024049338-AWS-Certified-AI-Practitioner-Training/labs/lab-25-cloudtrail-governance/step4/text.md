# Step 4 — Continuous compliance checking with AWS Config

CloudTrail tells you what *happened*. AWS Config tells you what your resources *currently look like* and whether that configuration is compliant. They answer different questions and are frequently confused.

| | AWS CloudTrail | AWS Config |
|---|---|---|
| Question answered | Who did what, when? | Is this resource configured correctly, and how has it changed? |
| Unit of record | An API call | A resource configuration item |
| Time orientation | A log of past actions | Current state plus configuration history |
| Typical use | Investigating an incident | Proving continuous compliance to an auditor |

The two are complements. Config tells you a SageMaker notebook is non-compliant *right now*; CloudTrail tells you who made it that way and when.

## Turn on AWS Config

> **Cost note:** AWS Config charges per configuration item recorded and per rule evaluation. On a small lab account with a handful of resources this is minor, but the recorder runs continuously once enabled and will keep recording every resource change. **You will turn it off in Step 6.** If you would prefer not to enable it, read this step and study the rule list — the concepts are what is assessed.

In the console open `https://console.aws.amazon.com/config/` and work through the setup. Choose to record resources, and select an S3 bucket for the configuration snapshot delivery. To limit cost, restrict the recorder to **specific resource types** rather than all supported resources — SageMaker and S3 types are enough for this lab.

## Add rules relevant to AI workloads

AWS Config rules evaluate resources against a desired configuration. **Managed rules** are pre-built by AWS. In the rules section, add rules by name. These are real managed rules directly relevant to this domain:

| Rule | What it checks | Why it matters for AI |
|---|---|---|
| `sagemaker-notebook-no-direct-internet-access` | Notebook instances cannot reach the internet directly | Prevents a data scientist exfiltrating a training dataset to an arbitrary host |
| `sagemaker-notebook-instance-kms-key-configured` | Notebook storage uses a KMS key | Enforces the encryption-at-rest control from Lab 23 |
| `sagemaker-endpoint-configuration-kms-key-configured` | Inference endpoints use a KMS key | Protects data captured at the endpoint |
| `s3-bucket-server-side-encryption-enabled` | Buckets have default encryption | Covers training data and model artifact buckets |
| `s3-bucket-public-read-prohibited` | Buckets are not publicly readable | The single most common cause of a training-data breach |
| `cloudtrail-enabled` | At least one trail exists | Proves the audit control from Step 3 is actually in place |
| `iam-user-mfa-enabled` | IAM users have MFA | Baseline identity hygiene |

Add two or three, then let them evaluate. Each resource is marked **COMPLIANT**, **NON_COMPLIANT** or **NOT_APPLICABLE**.

```bash
aws configservice describe-compliance-by-config-rule --region us-east-1
```

Open a non-compliant result and look at the resource identified. This is the artefact an auditor asks for: not a policy document asserting that encryption is required, but **evidence that every resource was continuously evaluated against that requirement, with timestamps.** The difference between a written policy and a Config rule is the difference between a claim and proof.

## Remediation and conformance packs

Two features worth recognising by name:

- **Remediation actions** attach an AWS Systems Manager Automation document to a rule so that a non-compliant resource is fixed automatically — for example, enabling default encryption on a bucket the moment it is detected without it. This converts a detective control into a corrective one.
- **Conformance packs** bundle many rules and remediations into a single deployable unit, and AWS publishes sample packs aligned to common frameworks. Deploying a pack across an organisation is how compliance is operated at scale rather than rule by rule.

## Mapping to compliance standards

The exam expects familiarity with the vocabulary rather than depth in any one framework:

- **ISO/IEC 27001** — information security management systems
- **SOC 1 / SOC 2 / SOC 3** — service organisation controls, reported by independent auditors
- **GDPR** and Singapore's **PDPA** — personal data protection, including lawful basis, data minimisation and data subject rights
- **HIPAA** — protected health information in the United States
- **PCI DSS** — payment card data
- **ISO/IEC 42001** — AI management systems, the newer standard specific to governing AI

Two AWS services support these directly:

- **AWS Artifact** provides on-demand access to AWS compliance reports and certifications — the evidence you hand an auditor about AWS's side of the shared responsibility model. If a question asks where to *obtain a SOC report*, the answer is AWS Artifact.
- **AWS Audit Manager** continuously collects evidence and maps it to control frameworks, automating the assessment reporting that would otherwise be manual.

Recall from Lab 23 that these cover AWS's responsibilities. Your controls — Config rules, CloudTrail, IAM, KMS — are the evidence for *your* half.
