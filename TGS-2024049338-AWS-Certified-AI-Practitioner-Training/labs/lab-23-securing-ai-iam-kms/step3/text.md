# Step 3 — Create a KMS customer managed key for AI data

Training data, model artifacts and inference logs are all sensitive. AWS KMS gives you three tiers of key, and the exam expects you to know why you would pick each.

| Key type | Who controls the key policy | Can you rotate/disable/delete it? | Visible in your account | Cost |
|---|---|---|---|---|
| AWS owned key | AWS | No | No | No charge |
| AWS managed key (`aws/s3`, `aws/sagemaker`) | AWS | No — rotation is automatic | Yes, read-only | No monthly charge |
| **Customer managed key (CMK)** | **You** | **Yes** | **Yes** | **Monthly charge per key, plus API request charges** |

You need a customer managed key when you must **control who can decrypt** — for example, to deny an entire team access to a training dataset by editing one key policy, or to satisfy an auditor who requires that key material be under your administrative control.

> **Cost note:** A customer managed key incurs a monthly charge that is prorated hourly, plus a charge per cryptographic API request. This is small but it is not zero and it is not covered by the free tier. Check the AWS KMS pricing page for current rates. You will schedule this key for deletion in Step 6.

## Create the key

```bash
aws kms create-key \
  --description "AI Practitioner lab - training data and model artifacts" \
  --key-usage ENCRYPT_DECRYPT \
  --region us-east-1
```

Copy the `KeyId` from the output. Give it a friendly alias so you never have to type the UUID again:

```bash
aws kms create-alias \
  --alias-name alias/ai-lab-cmk \
  --target-key-id <key-id> \
  --region us-east-1
```

## Turn on automatic rotation

```bash
aws kms enable-key-rotation --key-id <key-id> --region us-east-1
```

Understand what rotation does and does not do. When KMS rotates a customer managed key it generates new backing key material but **keeps the same key ID and ARN**. Old ciphertext is not re-encrypted — KMS retains the previous material so it can still decrypt data written before the rotation. Nothing in your application changes. This is why "enable automatic key rotation" is almost always the correct answer to a compliance question, and why "re-encrypt all objects" is almost always wrong.

## Inspect the key policy

In the console, open `https://console.aws.amazon.com/kms/`, choose **Customer managed keys** in the left navigation, and select your key. Look at the **Key policy** section.

The key policy is a resource-based policy, and this is the single most important KMS concept for the exam:

**For a principal to use a KMS key, permission must be granted in the key policy.** An IAM identity policy that says `"Action": "kms:Decrypt", "Resource": "*"` grants nothing on its own if the key policy does not also allow it. This is the reverse of most AWS services and it is where KMS questions are usually set.

The default key policy delegates to IAM by allowing the account root principal, which lets IAM policies in the account take effect. If you replace it with an explicit list of principals, only those principals can use the key regardless of their IAM permissions.

## Grant the SageMaker execution role access

For a SageMaker training job to write encrypted model artifacts, its execution role needs key permissions. Add a statement like this to the key policy (in the console, choose **Edit** on the key policy):

```json
{
  "Sid": "AllowSageMakerExecutionRole",
  "Effect": "Allow",
  "Principal": {
    "AWS": "arn:aws:iam::<account-id>:role/<your-sagemaker-execution-role>"
  },
  "Action": [
    "kms:Encrypt",
    "kms:Decrypt",
    "kms:ReEncrypt*",
    "kms:GenerateDataKey*",
    "kms:DescribeKey"
  ],
  "Resource": "*"
}
```

`"Resource": "*"` inside a key policy means *this key* — a key policy is already attached to one key, so there is nothing else it could refer to.

`kms:GenerateDataKey` is the action that matters most in practice. S3 and SageMaker do not send your data to KMS; they ask KMS for a data key, encrypt locally with it, and store the encrypted data key alongside the object. This is **envelope encryption**, and if you omit `GenerateDataKey` from a policy, writes fail while reads may still work.

If you do not have a SageMaker execution role in this account, skip the policy edit — the concept is what is being assessed.
