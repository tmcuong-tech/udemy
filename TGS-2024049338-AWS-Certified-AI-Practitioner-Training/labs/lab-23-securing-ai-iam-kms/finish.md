# Well done!

You have completed Lab 23 — Securing AI Workloads with IAM and KMS:

✅ Map the shared responsibility model onto an AI workload
✅ Write a least-privilege IAM policy scoped to specific Bedrock models
✅ Create a KMS customer managed key for AI data
✅ Encrypt a training data bucket at rest, and understand encryption in transit
✅ Keep AI traffic off the public internet with VPC endpoints
✅ Clean up

**Key takeaways:**

- AWS secures the cloud; you secure what you put in it. The boundary shifts with the service — a fully managed Bedrock call leaves you far less to patch than a SageMaker training job running your own container, but identity, data classification, encryption choices and network exposure are always yours.
- A Bedrock foundation-model ARN has an empty account field (`arn:aws:bedrock:us-east-1::foundation-model/<model-id>`) because the models are owned by AWS, not your account. Model access and IAM permission are two separate gates and both must allow a call.
- Choose a customer managed KMS key when you must control the key policy, rotation and deletion. Automatic rotation keeps the same key ID and ARN and never requires re-encrypting existing data — "re-encrypt everything" is almost always the wrong answer.
- A KMS key policy is a resource-based policy, and permission must be granted there. An IAM policy allowing `kms:Decrypt` grants nothing if the key policy does not also allow the principal.
- Encryption at rest (SSE-KMS) and in transit (TLS, enforced by the `aws:SecureTransport` condition key) solve different problems, and neither restricts an authorised user with a valid role — that is what least-privilege IAM is for.
- Bedrock and SageMaker use interface endpoints (PrivateLink), which bill hourly per availability zone; only S3 and DynamoDB use free gateway endpoints. Bedrock's control plane and runtime are separate endpoint services, and it is the runtime one that carries your prompts.

**Next:** Lab 24 — Data Protection with Amazon Macie
