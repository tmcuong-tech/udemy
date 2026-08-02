# Lab 23 — Securing AI Workloads with IAM and KMS

Apply least-privilege IAM policies, customer managed KMS keys and VPC endpoints to secure an AI workload, and locate the boundary of the AWS shared responsibility model.

**What you will do:**
- Map the AWS shared responsibility model onto Amazon Bedrock and Amazon SageMaker
- Write an IAM policy scoped to specific Bedrock foundation models and SageMaker resources
- Create a KMS customer managed key with automatic rotation and inspect its key policy
- Encrypt a training data bucket with the key and enforce encryption in transit
- Create a VPC interface endpoint to keep inference traffic off the public internet
