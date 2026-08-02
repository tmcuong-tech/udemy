# Lab 23 — Securing AI Workloads with IAM and KMS

Apply least-privilege IAM policies, customer managed KMS keys and VPC endpoints to secure an AI workload, and locate the boundary of the AWS shared responsibility model.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 5 — Security, Compliance, and Governance for AI Solutions (14%)
**Task statement:** 5.1 Explain methods to secure AI systems.
**WSQ mapping:** LU5 · Topic 11 Security, Compliance and Governance · K11 · A5 · LO5
**Slide reference:** v11 deck slides 299–333
**Estimated time:** 40 minutes

**Learning objectives:**
- Locate the boundary of the AWS shared responsibility model for Amazon Bedrock and Amazon SageMaker
- Write an IAM policy that grants only the required actions on only the required Bedrock and SageMaker resources
- Choose correctly between AWS owned, AWS managed and customer managed KMS keys, and explain what key rotation does
- Configure default encryption on an S3 bucket with a customer managed key and enforce it with a bucket policy
- Distinguish encryption at rest from encryption in transit and identify the condition keys that enforce each
- Explain when a VPC interface endpoint is required to keep AI inference traffic off the public internet

---

## Step 1 — Map the shared responsibility model onto an AI workload

Before you write a single policy, you need to know which security controls are yours to configure and which AWS already handles. The exam tests this directly.

Under the AWS shared responsibility model, AWS is responsible for **security *of* the cloud** and you are responsible for **security *in* the cloud**. The line moves depending on how managed the service is.

Open a text editor and copy this table. Fill in the last column yourself before reading on.

| Control | Amazon Bedrock | Amazon SageMaker | Who owns it? |
|---|---|---|---|
| Patching the host operating system | AWS | AWS | |
| Physical data centre security | AWS | AWS | |
| Choosing which IAM principals may call the model | You | You | |
| Encrypting training data in S3 | You | You | |
| Patching the training container image | AWS (managed FM) | You (custom container) | |
| Deciding what data goes into a prompt | You | You | |
| Availability of the underlying service | AWS | AWS | |

The pattern to remember:

- **AWS always owns** the physical infrastructure, the hypervisor, the managed service software, and the security of the foundation model hosting environment.
- **You always own** identity and access management, data classification, encryption configuration, network exposure, and what you choose to send to a model.
- **The boundary shifts** with the service model. With Amazon Bedrock (fully managed, serverless) AWS handles far more of the stack. With a SageMaker training job using your own container, you own the container contents, its dependencies and its vulnerabilities.

Three points that come up repeatedly in exam questions:

1. **AWS does not use your Bedrock prompts or completions to train the base foundation models.** Your inputs and outputs are not shared with model providers. This is a service property, not something you configure.
2. **Encryption is available but not automatic at the level you may need.** S3 encrypts objects by default with an AWS managed key. Using a *customer managed* KMS key — so that you control the key policy, rotation and deletion — is your decision and your configuration work.
3. **Network isolation is your job.** By default an API call to Bedrock or SageMaker travels over the public internet to a public AWS endpoint (still TLS-encrypted). Keeping that traffic on the AWS network requires you to create VPC endpoints.

Write one sentence in your notes answering: *if a developer pastes a customer's medical record into a Bedrock prompt, whose responsibility was the failure?* You will confirm the answer in the discussion questions.

---

## Step 2 — Write a least-privilege IAM policy scoped to specific Bedrock models

The default instinct is to attach a broad managed policy and move on. Least privilege means granting only the actions, on only the resources, that a principal actually needs.

## Find the exact model identifiers

You cannot scope a policy to a model without its identifier. In the console, open the **Amazon Bedrock** console at `https://console.aws.amazon.com/bedrock/` and in the left navigation choose **Model access** (it may appear under a configuration or settings grouping). This page lists the foundation models available to you **in your current Region** — availability differs by Region, so always read it rather than assuming.

Or from the CLI:

```bash
aws bedrock list-foundation-models \
  --region us-east-1 \
  --query 'modelSummaries[].modelId' \
  --output table
```

Copy one model ID you have access to. In the steps below, substitute it wherever you see `<model-id>`. Do not type a model version string from memory — copy the exact value the API returns.

## Build the policy

Create a file called `bedrock-least-privilege.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "InvokeApprovedModelsOnly",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:us-east-1::foundation-model/<model-id>"
    },
    {
      "Sid": "ReadOnlyDiscovery",
      "Effect": "Allow",
      "Action": [
        "bedrock:ListFoundationModels",
        "bedrock:GetFoundationModel"
      ],
      "Resource": "*"
    }
  ]
}
```

Read what this actually does:

- **Only two invocation actions are allowed.** `bedrock:InvokeModel` covers a normal request/response call; `bedrock:InvokeModelWithResponseStream` covers streaming. If you grant only the first, a streaming application fails with `AccessDeniedException` — a classic troubleshooting scenario.
- **The resource is a single model ARN.** A principal with this policy cannot invoke any other foundation model, even one it has been granted access to on the Model access page. Model access and IAM permission are two separate gates and **both** must allow the call.
- **The foundation-model ARN has an empty account field** (`bedrock:us-east-1::`). Foundation models are owned by AWS, not by your account, so there is no account ID in that position. Getting this wrong is a common source of silent access denials.
- **Discovery actions are separated and read-only.** Listing models reveals no data, so `"Resource": "*"` is acceptable there. Never reuse that wildcard on the invocation statement.

Create the policy:

```bash
aws iam create-policy \
  --policy-name BedrockLeastPrivilegeLab \
  --policy-document file://bedrock-least-privilege.json
```

Note the `Arn` value in the output — you will need it in Step 6.

## Add a condition (optional but exam-relevant)

You can tighten further with a condition key. Adding this block to the invoke statement restricts calls to requests that arrive over a VPC endpoint:

```json
"Condition": {
  "StringEquals": {
    "aws:SourceVpce": "<vpc-endpoint-id>"
  }
}
```

You will create such an endpoint in Step 5. The pattern to remember for the exam: **identity policies say *who* and *what*; condition keys say *under what circumstances*.**

## The SageMaker equivalent

The same discipline applies to SageMaker. A data scientist who needs to run training jobs does not need permission to delete endpoints or read every bucket:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sagemaker:CreateTrainingJob",
        "sagemaker:DescribeTrainingJob",
        "sagemaker:StopTrainingJob"
      ],
      "Resource": "arn:aws:sagemaker:us-east-1:<account-id>:training-job/*"
    },
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": "arn:aws:s3:::<your-training-bucket>/*"
    }
  ]
}
```

Note the difference from the Bedrock ARN: SageMaker resources *are* in your account, so the account ID field is populated.

Remember the distinction between the two roles in play:

- The **user's identity policy** controls whether a person may start a training job.
- The **SageMaker execution role** is what the training job itself assumes to read data and write model artifacts. It is a separate role with a `sagemaker.amazonaws.com` trust policy, and it is the one that needs S3 and KMS permissions.

---

## Step 3 — Create a KMS customer managed key for AI data

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

---

## Step 4 — Encrypt a training data bucket at rest, and understand encryption in transit

Now apply the key to a real bucket — the kind you would use for training data and model artifacts.

## Create the bucket

Bucket names are globally unique, so add your own suffix:

```bash
aws s3api create-bucket \
  --bucket ai-lab-training-data-<your-initials>-<random-number> \
  --region us-east-1
```

Block all public access immediately. For a bucket holding training data this is not optional:

```bash
aws s3api put-public-access-block \
  --bucket ai-lab-training-data-<your-initials>-<random-number> \
  --public-access-block-configuration \
    "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

## Apply the customer managed key as default encryption

```bash
aws s3api put-bucket-encryption \
  --bucket ai-lab-training-data-<your-initials>-<random-number> \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "aws:kms",
        "KMSMasterKeyID": "alias/ai-lab-cmk"
      },
      "BucketKeyEnabled": true
    }]
  }'
```

Verify it took effect:

```bash
aws s3api get-bucket-encryption \
  --bucket ai-lab-training-data-<your-initials>-<random-number>
```

Two things to note:

- **`SSEAlgorithm: aws:kms`** is SSE-KMS. The alternative `AES256` is SSE-S3, which uses an AWS owned key you cannot control or audit. If a question asks for encryption at rest with *auditable, customer-controlled keys*, the answer is SSE-KMS with a customer managed key.
- **`BucketKeyEnabled: true`** turns on S3 Bucket Keys, which dramatically reduces the number of KMS API calls (and therefore the KMS request charges) when many objects share a key. On a bucket holding thousands of training files this matters. Leave it on.

Upload a test object and confirm the encryption is applied:

```bash
echo "sample training record" > sample.txt
aws s3 cp sample.txt s3://ai-lab-training-data-<your-initials>-<random-number>/
aws s3api head-object \
  --bucket ai-lab-training-data-<your-initials>-<random-number> \
  --key sample.txt
```

The response includes `"ServerSideEncryption": "aws:kms"` and an `SSEKMSKeyId` pointing at your key. You never passed an encryption flag on the upload — the bucket default did the work. That is the point: default encryption means a developer cannot accidentally write plaintext.

## Enforce it with a bucket policy

Default encryption applies when the caller specifies nothing. A caller who explicitly requests `AES256` would override it. To make the CMK mandatory, deny anything else:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "DenyWrongEncryption",
    "Effect": "Deny",
    "Principal": "*",
    "Action": "s3:PutObject",
    "Resource": "arn:aws:s3:::<your-bucket-name>/*",
    "Condition": {
      "StringNotEquals": {
        "s3:x-amz-server-side-encryption": "aws:kms"
      }
    }
  }]
}
```

An explicit `Deny` beats any `Allow`, anywhere. This is the standard pattern for making an encryption requirement non-negotiable.

## Encryption in transit versus at rest

Learners routinely confuse these. Fix the distinction now.

| | At rest | In transit |
|---|---|---|
| Protects data that is | Stored on disk | Moving across a network |
| Technology | AWS KMS, SSE-KMS, EBS/EFS encryption | TLS 1.2 or higher |
| Threat it addresses | Stolen media, unauthorised console/API read of stored objects | Eavesdropping, tampering on the wire |
| Who configures it | You (choose the key type) | Enforced by AWS endpoints; you can *require* it |

**All AWS service endpoints, including Bedrock and SageMaker, require TLS.** Your prompts are already encrypted in transit — you do not enable that. What you *can* do is refuse any request that somehow arrives unencrypted, with another bucket policy statement:

```json
{
  "Sid": "DenyInsecureTransport",
  "Effect": "Deny",
  "Principal": "*",
  "Action": "s3:*",
  "Resource": [
    "arn:aws:s3:::<your-bucket-name>",
    "arn:aws:s3:::<your-bucket-name>/*"
  ],
  "Condition": {
    "Bool": { "aws:SecureTransport": "false" }
  }
}
```

`aws:SecureTransport` is a global condition key worth memorising. Note that the resource list contains **both** the bucket ARN and the object ARN — bucket-level actions like `ListBucket` operate on the first, object-level actions on the second. Omitting one leaves a gap.

Neither of these encryption controls protects you from an authorised user with a valid role reading the data. That is what the IAM scoping in Step 2 is for. Encryption and access control are complements, not substitutes.

---

## Step 5 — Keep AI traffic off the public internet with VPC endpoints

Your data is encrypted at rest and in transit. But when an application in your VPC calls Bedrock, the request leaves your VPC, traverses an internet gateway or NAT gateway, and reaches a public AWS endpoint. It is encrypted the whole way — yet many regulated organisations still cannot accept it, because the traffic *left the AWS network* and the instance needed a route to the internet at all.

VPC endpoints solve this. There are two kinds and the exam tests the difference.

| | Gateway endpoint | Interface endpoint (AWS PrivateLink) |
|---|---|---|
| Services supported | Amazon S3 and DynamoDB only | Most services, including **Bedrock** and **SageMaker** |
| How it works | Adds a route to your route table | Creates an ENI with a private IP in your subnet |
| Cost | **No charge** | **Hourly charge per endpoint per AZ, plus data processing charges** |
| Works from on-premises via VPN/DX | No | Yes |

> **Cost warning:** Interface endpoints bill by the hour for every availability zone in which they are provisioned, whether or not any traffic flows. They are not free tier eligible. If you create one in this step you **must** delete it in Step 6. If you would rather not incur the charge, read through this step and inspect the service names without creating anything — the walkthrough below tells you how.

## Inspect the available AI service endpoints (no charge)

This command lists the endpoint services your Region offers, filtered to Bedrock and SageMaker:

```bash
aws ec2 describe-vpc-endpoint-services \
  --region us-east-1 \
  --query 'ServiceNames[?contains(@, `bedrock`) || contains(@, `sagemaker`)]' \
  --output table
```

You will see service names in the form `com.amazonaws.us-east-1.<service>`. Notice that Bedrock exposes **separate endpoint services for the control plane and the runtime**:

- The control plane service covers management calls — listing models, creating customisation jobs.
- The runtime service covers `InvokeModel` — the actual inference traffic that carries your prompts.

This separation matters. If you privatise only the control plane, your prompts still travel over the public path. Securing an inference workload means creating the **runtime** endpoint.

SageMaker is split even further — the API, runtime, notebook, Studio and feature store each have their own endpoint service. Creating one does not privatise the others.

## Create an interface endpoint (optional — incurs charges)

If you choose to proceed, you need an existing VPC, a subnet and a security group. Find your default VPC:

```bash
aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" \
  --query 'Vpcs[0].VpcId' --output text
aws ec2 describe-subnets --filters "Name=vpc-id,Values=<vpc-id>" \
  --query 'Subnets[0].SubnetId' --output text
```

Then create the endpoint:

```bash
aws ec2 create-vpc-endpoint \
  --vpc-id <vpc-id> \
  --vpc-endpoint-type Interface \
  --service-name com.amazonaws.us-east-1.bedrock-runtime \
  --subnet-ids <subnet-id> \
  --security-group-ids <security-group-id> \
  --region us-east-1
```

Record the `VpcEndpointId` — you need it for cleanup.

Two configuration details that are easy to get wrong:

1. **The security group attached to the endpoint must allow inbound HTTPS (port 443) from your application's subnet or security group.** An interface endpoint is an ENI, and ENIs are governed by security groups. If inference calls hang after you create an endpoint, this is almost always why.
2. **Private DNS.** With private DNS enabled (the default for most services), the standard service hostname resolves to the endpoint's private IP inside your VPC. Your application code does not change at all — it keeps calling the normal endpoint and the traffic silently stays private. Private DNS requires `enableDnsSupport` and `enableDnsHostnames` on the VPC.

## Lock it down with an endpoint policy

An interface endpoint accepts a resource policy that constrains what can be reached *through* it:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": "*",
    "Action": [
      "bedrock:InvokeModel",
      "bedrock:InvokeModelWithResponseStream"
    ],
    "Resource": "arn:aws:bedrock:us-east-1::foundation-model/<model-id>"
  }]
}
```

Combine this with the `aws:SourceVpce` condition from Step 2 and you have a closed loop: the identity policy allows the call only from the endpoint, and the endpoint policy allows only that model. Neither control alone is sufficient; together they are hard to bypass.

## The related SageMaker control

For SageMaker notebook instances there is one more network control worth knowing: **disabling direct internet access**. A notebook created with direct internet access disabled cannot reach the internet unless you route it through a NAT gateway you control, which prevents a data scientist from exfiltrating a training dataset to an arbitrary external host. There is an AWS Config managed rule, `sagemaker-notebook-no-direct-internet-access`, that detects violations — you will meet AWS Config in Lab 25.

---

## Step 6 — Clean up

> **Delete the VPC endpoint first.** An interface endpoint bills every hour it exists, in every availability zone, regardless of traffic. It is the only resource in this lab with a meaningful continuous cost. The customer managed key also carries a small monthly charge until it is deleted.

## 1. Delete the interface endpoint (if you created one)

```bash
aws ec2 delete-vpc-endpoints \
  --vpc-endpoint-ids <vpc-endpoint-id> \
  --region us-east-1
```

Confirm it is gone:

```bash
aws ec2 describe-vpc-endpoints \
  --region us-east-1 \
  --query 'VpcEndpoints[].{Id:VpcEndpointId,State:State,Service:ServiceName}' \
  --output table
```

An endpoint in `deleting` state stops billing once it reaches `deleted`. If the list is empty, you are clear.

## 2. Empty and delete the S3 bucket

A bucket must be empty before it can be deleted:

```bash
aws s3 rm s3://ai-lab-training-data-<your-initials>-<random-number>/ --recursive
aws s3api delete-bucket --bucket ai-lab-training-data-<your-initials>-<random-number>
```

If deletion fails with `BucketNotEmpty` and you enabled versioning at any point, delete the object versions and delete markers as well, then retry.

## 3. Delete the IAM policy

```bash
aws iam delete-policy --policy-arn <policy-arn-from-step-2>
```

If this fails because the policy is attached to a principal, detach it first with `aws iam detach-role-policy` or `aws iam detach-user-policy`. IAM will not delete a policy that is still in use.

## 4. Schedule the KMS key for deletion

KMS keys **cannot be deleted immediately**. This is deliberate: deleting a key destroys all ciphertext encrypted under it, permanently and unrecoverably. AWS enforces a waiting period of 7 to 30 days during which you can cancel.

```bash
aws kms schedule-key-deletion \
  --key-id <key-id> \
  --pending-window-in-days 7 \
  --region us-east-1
```

Seven days is the minimum. The key enters `PendingDeletion` state, stops working for cryptographic operations, and **the monthly key charge stops accruing** during the waiting period. If you change your mind, `aws kms cancel-key-deletion` restores it.

Delete the alias too, so the name is free for reuse:

```bash
aws kms delete-alias --alias-name alias/ai-lab-cmk --region us-east-1
```

## 5. Verify nothing is left

```bash
aws kms list-aliases --query 'Aliases[?starts_with(AliasName, `alias/ai-lab`)]'
aws s3 ls | grep ai-lab-training-data
aws ec2 describe-vpc-endpoints --query 'length(VpcEndpoints)'
```

All three should return empty or zero. Also visit the AWS **Billing and Cost Management** console the following day and check **Cost Explorer** — building the habit of verifying that a lab actually stopped costing money is worth more than any single command above.

## What stays

The IAM policy JSON files on your local machine are harmless — keep them as templates. Nothing else from this lab should remain in your account.

---

## Verification

- [ ] I can state one control AWS owns and one I own for a Bedrock workload, and explain why the boundary moves for a SageMaker custom container
- [ ] My IAM policy names a specific foundation-model ARN, and I can explain why that ARN has an empty account field
- [ ] I created a customer managed key, gave it an alias and enabled automatic rotation
- [ ] I can explain why an IAM policy alone is not enough to use a KMS key
- [ ] `get-bucket-encryption` shows `aws:kms` with my key, and `head-object` confirms an uploaded object was encrypted without my passing any flag
- [ ] I can name the condition key that denies non-TLS requests and the one that restricts calls to a VPC endpoint
- [ ] I can state which endpoint type Bedrock requires and why it costs money
- [ ] The VPC endpoint is deleted, the bucket is deleted, and the KMS key is in `PendingDeletion`

## Discussion questions

1. A developer pastes a customer's medical record into a Bedrock prompt. Under the shared responsibility model, whose failure is this, and which of the controls in this lab would have prevented it? Which would not?
2. Your policy scopes `bedrock:InvokeModel` to one model ARN, but a teammate reports that model access is granted on the Model access page yet calls still fail with `AccessDeniedException`. List three distinct causes you would check, in order.
3. An auditor asks you to prove that a departing employee can no longer read last year's training data. Explain how a customer managed key lets you answer this in a way that an AWS managed key would not.
4. Your organisation requires that no Bedrock traffic leaves the AWS network. You create an interface endpoint for the Bedrock control plane and consider the requirement met. What have you missed, and how would you verify the fix?
5. Compare the cost and security trade-off of an interface endpoint against a NAT gateway with a restrictive route table. When is the endpoint clearly worth its hourly charge?

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.
