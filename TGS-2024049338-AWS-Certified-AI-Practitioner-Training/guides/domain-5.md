# Domain 5 — Security, Compliance and Governance for AI Solutions (14%)

Part of the [AWS Certified AI Practitioner Training (AIF-C01) Learner Guide](../LEARNER%20GUIDE.md) · course code TGS-2024049338

---

## Lab 23 — Securing AI Workloads with IAM and KMS

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

### Step 1 — Map the shared responsibility model onto an AI workload

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

### Step 2 — Write a least-privilege IAM policy scoped to specific Bedrock models

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

### Step 3 — Create a KMS customer managed key for AI data

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

### Step 4 — Encrypt a training data bucket at rest, and understand encryption in transit

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

### Step 5 — Keep AI traffic off the public internet with VPC endpoints

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

### Step 6 — Clean up

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

### Verification

- [ ] I can state one control AWS owns and one I own for a Bedrock workload, and explain why the boundary moves for a SageMaker custom container
- [ ] My IAM policy names a specific foundation-model ARN, and I can explain why that ARN has an empty account field
- [ ] I created a customer managed key, gave it an alias and enabled automatic rotation
- [ ] I can explain why an IAM policy alone is not enough to use a KMS key
- [ ] `get-bucket-encryption` shows `aws:kms` with my key, and `head-object` confirms an uploaded object was encrypted without my passing any flag
- [ ] I can name the condition key that denies non-TLS requests and the one that restricts calls to a VPC endpoint
- [ ] I can state which endpoint type Bedrock requires and why it costs money
- [ ] The VPC endpoint is deleted, the bucket is deleted, and the KMS key is in `PendingDeletion`

### Discussion questions

1. A developer pastes a customer's medical record into a Bedrock prompt. Under the shared responsibility model, whose failure is this, and which of the controls in this lab would have prevented it? Which would not?
2. Your policy scopes `bedrock:InvokeModel` to one model ARN, but a teammate reports that model access is granted on the Model access page yet calls still fail with `AccessDeniedException`. List three distinct causes you would check, in order.
3. An auditor asks you to prove that a departing employee can no longer read last year's training data. Explain how a customer managed key lets you answer this in a way that an AWS managed key would not.
4. Your organisation requires that no Bedrock traffic leaves the AWS network. You create an interface endpoint for the Bedrock control plane and consider the requirement met. What have you missed, and how would you verify the fix?
5. Compare the cost and security trade-off of an interface endpoint against a NAT gateway with a restrictive route table. When is the endpoint clearly worth its hourly charge?

---

---

## Lab 24 — Data Protection with Amazon Macie

Use Amazon Macie to discover synthetic personal data in an S3 bucket, read the findings and connect them to the controls that keep PII out of training data and prompts.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 5 — Security, Compliance, and Governance for AI Solutions (14%)
**Task statement:** 5.1 Explain methods to secure AI systems.
**WSQ mapping:** LU5 · Topic 11 Security, Compliance and Governance · K11 · A5 · LO5
**Slide reference:** v11 deck slides 299–333
**Estimated time:** 35 minutes

> **COST WARNING:** Amazon Macie sensitive data discovery jobs are **charged by the volume of data inspected**, and a job that has run cannot be un-run. This lab scans three files totalling a few kilobytes. Never point a discovery job at a bucket whose size you have not checked first. Macie also charges a monthly per-bucket monitoring fee while it is enabled — you will disable it in Step 6.

> **SYNTHETIC DATA ONLY:** every name, email address, phone number and identifier used in this lab is invented for teaching. Email addresses use the reserved `example.com` domain and phone numbers use the reserved `555-01xx` fiction range. **No real personal data appears anywhere in this lab, and you must not substitute any.**

**Learning objectives:**
- Explain the three ways personal data leaks through an AI system: memorisation in a trained model, exposure through prompts and logs, and retrieval from a RAG knowledge base
- Distinguish Amazon Macie from Amazon Comprehend by what each inspects and where
- Enable Macie and use its no-cost bucket inventory to assess scope before incurring discovery charges
- Create a custom data identifier for an organisation-specific format and scope a discovery job to control cost
- Interpret a Macie finding, including severity, affected resource and occurrence locations
- Map each finding to a preventive, detective, runtime or corrective control

---

### Step 1 — Why PII must never reach training data or prompts

Amazon Macie is a managed data security service that uses machine learning and pattern matching to discover sensitive data in Amazon S3. Before you run it, be clear about the problem it solves for an AI workload.

## The three failure modes

**1. PII in training data becomes PII in the model.**
A model trained on records containing names, email addresses and account numbers can reproduce them at inference time. This is *memorisation*, and it is not a bug you can patch — the information is distributed through the weights. Once a model has memorised a customer's phone number, the only reliable remedies are retraining from clean data or blocking the output. Neither is cheap. Data minimisation before training is the only control that actually scales.

**2. PII in prompts leaves your control boundary.**
Every prompt sent to a foundation model is data leaving the application. Amazon Bedrock does not use your prompts to train the base models, and prompts are encrypted in transit — but they may still be written to your own model invocation logs, to CloudWatch, to an application database, or to a third-party observability tool. Under GDPR or Singapore's PDPA, a customer's medical detail pasted into a prompt and then written to a log file is a processing activity you must be able to account for.

**3. PII in a RAG knowledge base is retrievable by anyone who can query it.**
This is the one teams miss most often. If you index an S3 bucket of internal documents into a knowledge base and one spreadsheet contains employee salaries, then any user who can ask the chatbot a question can potentially retrieve them. The vector store has no concept of "this user may not see this row" unless you build it. **Filter at ingestion, not at generation.**

## Where Macie fits

Macie answers a question you usually cannot answer by inspection: *what sensitive data is actually sitting in these buckets?* On a bucket holding tens of thousands of files that no one has audited, this is not a question a human can answer manually.

Typical placement in an AI pipeline:

```
Raw data lands in S3
        │
        ▼
  [ Macie discovery job ]  ← you are here
        │
        ├── findings: PII detected → quarantine, redact, or exclude
        │
        ▼
Curated training / knowledge base bucket
        │
        ▼
Fine-tuning job  or  Knowledge base ingestion
```

Macie is a **detective** control — it tells you what is there. It does not block, redact or delete anything. Pair it with:

- **Preventive controls:** Amazon Comprehend PII detection and redaction to strip entities from text before storage; S3 bucket policies and Block Public Access; the KMS encryption from Lab 23.
- **Runtime controls:** Amazon Bedrock Guardrails, which can block or mask PII in prompts *and* responses (Lab 19).

A common exam trap: a question describes wanting to *find* sensitive data across many S3 buckets and offers both Macie and Comprehend. Macie discovers **in S3 at rest**; Comprehend detects entities **in text you pass to it**. Match the verb and the location.

## Safety rule for this lab

> **You will create only synthetic data.** Every name, email address and identifier you upload in Step 2 is invented for this exercise — no real person's data appears anywhere in this lab, and **you must not substitute real customer, employee or personal data for any of it.** Uploading real PII to a practice account to "make the test more realistic" would itself be the exact governance failure this lab teaches you to prevent.

---

### Step 2 — Create a bucket and upload synthetic sample data

> **SYNTHETIC DATA ONLY.** Every value below is fabricated for teaching. The names are invented, the email addresses use the reserved `example.com` domain which cannot receive mail, and the identifiers are made-up strings. **Do not replace any of it with real personal data.**

## Create the bucket

```bash
aws s3api create-bucket \
  --bucket macie-lab-data-<your-initials>-<random-number> \
  --region us-east-1

aws s3api put-public-access-block \
  --bucket macie-lab-data-<your-initials>-<random-number> \
  --public-access-block-configuration \
    "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

Use the same bucket name throughout. Substitute it wherever you see `<bucket>` below.

## File 1 — a "customer export" that should never have been used for training

Create `customer_export.csv`:

```csv
record_id,full_name,email,phone,employee_ref,notes
1001,Marigold Thistlewick,marigold.thistlewick@example.com,+1-555-0142,EMP-ZZ-4417,Requested account closure
1002,Barnaby Quillfeather,barnaby.quillfeather@example.com,+1-555-0177,EMP-ZZ-8802,Escalated billing dispute
1003,Persimmon Vandergrift,persimmon.vandergrift@example.com,+1-555-0198,EMP-ZZ-1250,Upgraded to premium tier
1004,Cornelius Pemberwick,cornelius.pemberwick@example.com,+1-555-0121,EMP-ZZ-6634,Reported login failure
1005,Ottoline Frostwhistle,ottoline.frostwhistle@example.com,+1-555-0165,EMP-ZZ-3391,Requested data export
1006,Fitzwilliam Grimsdale,fitzwilliam.grimsdale@example.com,+1-555-0189,EMP-ZZ-7728,Cancelled subscription
1007,Hyacinth Ravensworth,hyacinth.ravensworth@example.com,+1-555-0133,EMP-ZZ-2065,Password reset request
1008,Ignatius Bellweather,ignatius.bellweather@example.com,+1-555-0154,EMP-ZZ-9143,Feedback on new feature
```

The names are deliberately absurd — that is the point. If any of them matched a real person it would be coincidence, and the `555-01xx` phone range is reserved for fiction. `example.com` is reserved by RFC 2606 and can never be registered.

## File 2 — a "support transcript" of the kind that ends up in a RAG knowledge base

Create `support_transcript.txt`:

```
Ticket ZZ-88213 — Support transcript (SYNTHETIC TEST DATA)

Agent: Thank you for contacting support. May I have your name?
Customer: Marigold Thistlewick.
Agent: And a contact email for the case?
Customer: marigold.thistlewick@example.com
Agent: I can see the account. The best callback number we have is
       +1-555-0142 — is that still correct?
Customer: Yes. My internal reference is EMP-ZZ-4417 if that helps.
Agent: Noted. I have escalated the case and you will hear back within
       two business days.
```

This file is the realistic threat. A CSV in a data lake is at least obviously structured data that someone might review. A support transcript looks like harmless prose, gets indexed into a knowledge base without a second thought, and quietly makes every detail in it retrievable through a chatbot.

## File 3 — a clean control file

Create `product_catalogue.csv`:

```csv
sku,product_name,category,unit_price,in_stock
SKU-4410,Ceramic Mug,Kitchenware,12.50,true
SKU-4411,Steel Kettle,Kitchenware,44.00,true
SKU-4412,Linen Napkin Set,Kitchenware,18.75,false
SKU-4413,Bamboo Cutting Board,Kitchenware,29.90,true
```

Including a file with no personal data lets you confirm Macie is discriminating rather than flagging everything. A detection tool that fires on every object is as useless as one that fires on none.

## Upload

```bash
aws s3 cp customer_export.csv    s3://<bucket>/raw/
aws s3 cp support_transcript.txt s3://<bucket>/raw/
aws s3 cp product_catalogue.csv  s3://<bucket>/raw/
aws s3 ls s3://<bucket>/raw/
```

All three objects should be listed. Keep the total tiny — the next step explains why data volume is the thing you are billed on.

---

### Step 3 — Enable Amazon Macie

> **COST WARNING — read before you click.**
> Amazon Macie bills on two separate dimensions:
> 1. **Automated S3 bucket inventory and evaluation**, charged per bucket monitored per month.
> 2. **Sensitive data discovery jobs, charged by the volume of data inspected.** This is the one that surprises people. Pointing a discovery job at a production data lake containing terabytes can produce a very large bill from a single click, and the job cannot be un-run.
>
> Macie offers a free trial period for new accounts, but **do not rely on it** — check the Amazon Macie pricing page and your account's trial status in the Macie console before running any job.
>
> **In this lab you will scan three tiny files, a few kilobytes in total.** Never point a discovery job at a bucket whose size you have not checked. Before scanning any real bucket, look at its size in the S3 console or Macie's own bucket inventory first.

## Enable the service

In the console, open `https://console.aws.amazon.com/macie/` and choose the option to enable Macie. Macie is a **regional** service — enabling it in `us-east-1` does not enable it elsewhere, and it can only scan buckets in the Region where it is enabled.

From the CLI:

```bash
aws macie2 enable-macie --region us-east-1
```

Confirm:

```bash
aws macie2 get-macie-session --region us-east-1
```

The response shows `"status": "ENABLED"` and the `findingPublishingFrequency`.

## Look at the automated bucket inventory first

Once enabled, Macie immediately builds an inventory of every S3 bucket in the Region — **at no per-gigabyte charge, because it is reading metadata, not object contents.** In the left navigation choose the S3 buckets view.

For each bucket you get:

- Total object count and total size — check this *before* scheduling a job
- Whether the bucket is publicly accessible
- Whether it is encrypted, and with which type of key
- Whether it is shared with other AWS accounts
- Object counts by file type, and how many objects Macie *can* classify

This inventory alone is valuable. "Which of my buckets are unencrypted and publicly readable?" is a question most organisations cannot answer quickly, and answering it costs nothing beyond the per-bucket monitoring charge.

Find your `macie-lab-data-...` bucket in the list and note its size. It should be a few kilobytes. That is the number that determines what the next step costs.

## Understand automated discovery versus a discovery job

Macie provides two different mechanisms and the exam may distinguish them:

| | Automated sensitive data discovery | Sensitive data discovery job |
|---|---|---|
| Scope | Continuously samples objects across buckets | Buckets and prefixes you select |
| Control over what is scanned | Low — Macie chooses representative samples | Full — you pick buckets, prefixes, file types |
| Schedule | Ongoing, automatic | One-time or on a schedule you set |
| Cost profile | Designed to be lower via sampling | Charged on the full volume inspected |
| Best for | Broad, continuous visibility | Targeted audits, compliance evidence |

For an AI pipeline, the practical pattern is: leave automated discovery on for broad coverage, and run a targeted **job** against a specific prefix immediately before that data is used for training or knowledge base ingestion.

## Managed data identifiers

Macie ships with managed data identifiers — built-in detection logic for common sensitive data types, including names, email addresses, phone numbers, mailing addresses, credentials such as private keys, and country-specific identifiers like national ID and tax numbers.

Two things to understand about how they work:

- Detection is **not simple regex**. Many identifiers require supporting context — a nearby keyword, a plausible format, or a checksum. A nine-digit number sitting alone in a column may not be reported as a national ID, because Macie is deliberately tuned to limit false positives.
- You can add **custom data identifiers** with your own regular expression, optional proximity keywords and a character-count limit. This is how you detect organisation-specific formats — internal employee references, policy numbers, case IDs. The `EMP-ZZ-####` pattern in your sample data is exactly this kind of value, and you will use a custom identifier for it in Step 4.

---

### Step 4 — Create a custom data identifier and run a discovery job

## Create a custom data identifier for the internal reference format

Managed identifiers will not know what `EMP-ZZ-4417` means — that is an internal format specific to this fictional organisation. Custom data identifiers exist for exactly this.

In the Macie console, in the left navigation find **Custom data identifiers** and create a new one:

- **Name:** `internal-employee-reference`
- **Regular expression:** `EMP-ZZ-[0-9]{4}`
- **Keywords:** (optional) `employee_ref`, `internal reference`
- **Ignore words:** leave empty
- **Maximum match distance:** leave at the default

Macie provides a test box on the creation page. Paste `Customer reference EMP-ZZ-4417 was recorded` into it and confirm the identifier matches before saving. Testing before running is a habit worth forming — a discovery job that runs with a broken regex costs the same as one that works.

The keyword and match-distance settings control *precision*: requiring a keyword within a set number of characters of the match suppresses coincidental hits. Over-broad custom identifiers are the main cause of finding fatigue, where so many false positives accumulate that the team stops reading findings at all.

## Create the discovery job

> **Check the bucket size one more time.** You are about to authorise a job charged by data volume. Your bucket should be a few kilobytes.

In the left navigation choose **Jobs**, then create a job:

1. **Select S3 buckets** — choose your `macie-lab-data-...` bucket only. Do not select all buckets.
2. **Refine the scope** — this page is where cost is controlled. Set:
   - **Sampling depth:** 100% (safe here because the data is tiny; on a large bucket, reducing this reduces both coverage and cost proportionally)
   - **Includes:** add an S3 object prefix condition for `raw/`
   - You can also exclude by file extension, object size or last-modified date
3. **Job type** — choose **one-time job**. A scheduled job re-runs and re-bills on every run.
4. **Managed data identifiers** — keep the recommended set.
5. **Custom data identifiers** — select `internal-employee-reference`.
6. **Name** — `macie-lab-discovery-job`.
7. Review the summary, which shows the estimated volume to be scanned, and submit.

The job moves through `RUNNING` to `COMPLETE`. On three small files this takes a few minutes.

Monitor from the CLI:

```bash
aws macie2 list-classification-jobs --region us-east-1 \
  --query 'items[].{Name:name,Id:jobId,Status:jobStatus}' --output table
```

Note the `jobId` — you need it for cleanup.

## While it runs: what "sensitive data discovery" actually costs you elsewhere

Consider what would have happened without this step. The `raw/` prefix would have been used directly as a fine-tuning dataset or ingested into a knowledge base. Nobody would have opened `support_transcript.txt` — it is one file among thousands.

The cost of *not* scanning is not a bill; it is a model or a retrieval index that contains personal data you cannot enumerate, cannot delete on request, and cannot prove you controlled. When a data subject exercises a right to erasure, "we do not know whether their data is in the model" is not an answer a regulator accepts.

Running a discovery job before ingestion converts an unbounded, unknowable risk into a list of file paths you can act on. That is the whole argument for this control, and it is worth being able to state in one sentence.

---

### Step 5 — Read the findings and turn them into data controls

## Open the findings

When the job status reaches `COMPLETE`, choose **Findings** in the left navigation. Or from the CLI:

```bash
aws macie2 list-findings --region us-east-1
```

```bash
aws macie2 get-findings --region us-east-1 --finding-ids <finding-id>
```

Select a finding and work through its structure. Every Macie finding tells you:

- **Finding type** — sensitive data findings use types beginning `SensitiveData:S3Object/...` (for example a personal-information subtype). A separate family, `Policy:IAMUser/...`, covers bucket configuration problems such as public access or disabled encryption, and those are generated without any discovery job.
- **Severity** — Low, Medium or High, derived from the type and quantity of sensitive data found.
- **Resource affected** — the exact bucket, object key, size and encryption status.
- **Sensitive data detected** — the categories found, the count of occurrences per category, and the **location** of each occurrence: line and column for CSV, offset ranges for text.

That last field is the operationally useful one. It gives you `customer_export.csv`, column 2, rows 2 through 9 — precise enough to script a redaction against.

## What you should see, and what you might not

`customer_export.csv` and `support_transcript.txt` should produce findings; `product_catalogue.csv` should produce none. Expect email addresses and your custom `EMP-ZZ-` identifier to be detected reliably.

**If a category you expected is missing, that is a finding in itself, not a failure of the lab.** Macie's managed identifiers are tuned against false positives, and detection for personal names and some identifier types depends on surrounding context — a column header, nearby keywords, plausible formatting. In a small synthetic file that context is thin.

Sit with the implication rather than moving past it: **a detective control that reports nothing does not mean there is nothing there.** Macie reduces uncertainty; it does not eliminate it. Anyone who treats a clean Macie report as proof of a PII-free dataset has misunderstood the tool. This nuance appears in exam questions about the limits of automated discovery.

## Trace each finding to a control

Take each finding and decide what actually happens next. This is the reasoning the exam tests.

| Finding | Why it matters for AI | Control to apply |
|---|---|---|
| Email addresses in `customer_export.csv` | A fine-tuned model can memorise and reproduce them | Exclude the column, or redact with Amazon Comprehend PII detection, before the file reaches the training bucket |
| Personal data in `support_transcript.txt` | Prose files get indexed into RAG knowledge bases without review; anyone who can query the bot can retrieve them | Keep the file out of the knowledge base data source prefix entirely; filter at ingestion |
| Custom `EMP-ZZ-` references | Internal identifiers are re-identification keys — harmless alone, linkable to a person when joined with another dataset | Tokenise or hash before storage; treat as PII in your data classification |
| No findings in `product_catalogue.csv` | Confirms the control discriminates rather than flagging everything | Safe to promote to the curated bucket |

Notice that not one of these remediations is performed by Macie. Macie produced the list; **you** decide and implement. Every exam question that describes Macie *blocking*, *redacting* or *deleting* data is describing something Macie does not do.

## Wire findings into a workflow

Macie automatically publishes findings to **Amazon EventBridge** and to **AWS Security Hub**. That is what makes it operational rather than a report you read once:

- An EventBridge rule matching Macie findings can trigger a Lambda function that moves the offending object to a quarantine bucket, or blocks a pipeline stage.
- Security Hub aggregates Macie findings alongside GuardDuty, Inspector and Config, giving one compliance view.
- Findings can be exported to an S3 bucket for long-term retention — worth knowing, because **findings are retained in Macie for a limited period (90 days)**. If you need audit evidence beyond that window you must configure the export yourself.

The gap between a *detection* and a *prevention* is the automation you build. Macie tells you the data is there; EventBridge plus Lambda is what stops it reaching your training job.

## Connect back to the AI pipeline

Position the full set of controls you now know:

- **Before storage:** Amazon Comprehend detects and redacts PII entities in text.
- **At rest in S3:** Macie discovers what is actually there; KMS encryption (Lab 23) protects it; IAM restricts who reads it.
- **At inference:** Amazon Bedrock Guardrails (Lab 19) blocks or masks PII in both prompts and model responses.
- **After the fact:** CloudTrail records who accessed what (Lab 25).

No single one of these is sufficient. A question offering only one control for an end-to-end data-protection requirement is usually testing whether you notice that layered controls are the correct answer.

---

### Step 6 — Clean up

> **Disable Macie.** While Macie is enabled it charges a monthly fee per S3 bucket it monitors, prorated, whether or not you run any job. Leaving it on across a whole account with many buckets is the most likely way to be surprised by a bill from this lab. Discovery jobs themselves are charged once, on the volume already scanned — you cannot un-run a job, but you can stop future ones.

## 1. Cancel the discovery job

A one-time job that has already completed will not run again, but cancel it explicitly so nothing is left in a schedulable state:

```bash
aws macie2 update-classification-job \
  --job-id <job-id> \
  --job-status CANCELLED \
  --region us-east-1
```

Verify no job is in a running or paused state:

```bash
aws macie2 list-classification-jobs --region us-east-1 \
  --query 'items[].{Name:name,Status:jobStatus}' --output table
```

## 2. Delete the custom data identifier

```bash
aws macie2 list-custom-data-identifiers --region us-east-1
aws macie2 delete-custom-data-identifier \
  --id <custom-data-identifier-id> \
  --region us-east-1
```

## 3. Empty and delete the S3 bucket

Delete this bucket even though its contents are synthetic. A bucket named after a data-protection lab, containing files that *look* like a customer export, is exactly the kind of artefact that confuses a future audit of your own account.

```bash
aws s3 rm s3://macie-lab-data-<your-initials>-<random-number>/ --recursive
aws s3api delete-bucket --bucket macie-lab-data-<your-initials>-<random-number>
```

Delete the local copies too:

```bash
rm customer_export.csv support_transcript.txt product_catalogue.csv
```

## 4. Disable Macie

```bash
aws macie2 disable-macie --region us-east-1
```

Understand what this does: disabling Macie **permanently deletes all of your findings and job records** in that Region. If you needed any of it as audit evidence you would have had to export it to S3 first (Step 5). For this lab there is nothing worth keeping, but on a real account confirm exports are in place before you disable.

Confirm the session is gone:

```bash
aws macie2 get-macie-session --region us-east-1
```

This should now return a resource-not-found error. That error is the success condition.

## 5. Check the other Regions

Macie is regional, and it is easy to enable it in a second Region by accident while clicking through the console. If you switched Regions at any point during the lab, check there too:

```bash
aws macie2 get-macie-session --region <other-region>
```

## 6. Verify the spend

Open the **Billing and Cost Management** console the next day and filter Cost Explorer to Amazon Macie. Given three files of a few kilobytes and a session lasting under an hour, the charge should be negligible or zero under a free trial — but confirming it rather than assuming it is the habit that matters.

---

### Verification

- [ ] I can state in one sentence why PII in a fine-tuning dataset is harder to remediate than PII in a database
- [ ] All three sample files are uploaded, and I confirmed every value in them is synthetic
- [ ] I checked my bucket's size in the Macie bucket inventory **before** creating the discovery job
- [ ] My custom data identifier matched the test string in the console before I saved it
- [ ] The discovery job reached `COMPLETE` and was scoped to one bucket and one prefix
- [ ] I opened a finding and located the affected object key and the occurrence locations within it
- [ ] `product_catalogue.csv` produced no findings, confirming the control discriminates
- [ ] The job is cancelled, the custom identifier and bucket are deleted, and `get-macie-session` returns not-found

### Discussion questions

1. A colleague argues that scanning is unnecessary because "the bucket is encrypted and private." Explain why encryption and access control do not address the problem Macie solves.
2. Your discovery job returns no findings on a 400 GB knowledge base source bucket. Give three reasons this result might be misleading, and say what you would do before declaring the data clean.
3. You must detect an internal policy-number format across a data lake. Compare a Macie custom data identifier with a scheduled Lambda function that greps the objects. Which would you choose, and what does each cost you?
4. Design an EventBridge-driven workflow that stops PII reaching a Bedrock knowledge base. At which point in the ingestion pipeline does it intervene, and what happens to the offending object?
5. A data subject requests erasure of their personal data. Your model was fine-tuned six months ago on a dataset that included them. Walk through what you can and cannot do, and explain which control in this lab would have made the request answerable.

---

---

## Lab 25 — Governance, Audit and Model Lineage

Inspect real CloudTrail events for Bedrock and SageMaker API calls, add AWS Config compliance rules, and use the SageMaker Model Registry for version control and deployment approval.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 5 — Security, Compliance, and Governance for AI Solutions (14%)
**Task statement:** 5.2 Recognize governance and compliance regulations for AI systems.
**WSQ mapping:** LU5 · Topic 11 Security, Compliance and Governance · K11 · A5 · LO5
**Slide reference:** v11 deck slides 334–374
**Estimated time:** 35 minutes

> **Cost note:** AWS CloudTrail Event history is free. A trail incurs S3 storage charges, and AWS Config charges per configuration item recorded and per rule evaluation for as long as the recorder runs. Both are cleaned up in Step 6.

**Learning objectives:**
- Identify AWS CloudTrail as the service that records who called a Bedrock or SageMaker API, which action, and when
- Distinguish CloudTrail from Amazon Bedrock model invocation logging, CloudWatch and AWS Config by the question each answers
- Read a CloudTrail event record and extract the identity, action, timestamp, source IP and outcome
- Explain what a trail adds over Event history, including multi-Region coverage, data events and log file validation
- Apply AWS Config managed rules that check SageMaker and S3 resources against a security baseline
- Describe data and model lineage, and the SageMaker Model Registry approval workflow as a deployment gate
- Name the AWS services that supply compliance evidence and relate them to common standards

**Prerequisite:** Lab 23 introduced the shared responsibility model, IAM and KMS; this lab builds directly on it.

---

### Step 1 — Generate AI API activity to audit

You cannot inspect an audit trail with nothing in it. Start by making some calls that CloudTrail will record.

## What CloudTrail is, precisely

AWS CloudTrail records **API activity in your AWS account**: who made a call, which API they called, when, from where, and what the outcome was. It is enabled by default — every account has **CloudTrail Event history**, a rolling **90-day** record of management events, at no charge and with nothing to configure.

Three properties matter for the exam:

- CloudTrail answers **"who did what, when"**. It is an *audit* service.
- Amazon CloudWatch answers **"how is it performing"** — latency, invocation counts, token counts, error rates. It is a *monitoring* service.
- CloudTrail Event history is free but limited to 90 days and management events. A **trail** (Step 3) is what you create for longer retention, data events, and delivery to S3.

Questions that describe needing an audit record of *who invoked a Bedrock model* are CloudTrail questions. Questions about *invocation latency or throttling* are CloudWatch questions. Read the verb.

## Make some Bedrock calls

Run a mix of successful and unsuccessful calls — failed calls are recorded too, and are often the more interesting ones.

```bash
aws bedrock list-foundation-models --region us-east-1 \
  --query 'modelSummaries[0:3].modelId' --output table
```

```bash
aws bedrock get-foundation-model \
  --model-identifier <model-id-from-above> \
  --region us-east-1
```

Now deliberately generate an access-denied event by requesting something that does not exist:

```bash
aws bedrock get-foundation-model \
  --model-identifier this-model-does-not-exist \
  --region us-east-1
```

The command fails at the terminal. **CloudTrail still records it**, with the error code attached. An attacker probing your account produces exactly this pattern, which is why failed calls are what security teams alert on.

## Make some SageMaker calls

```bash
aws sagemaker list-model-package-groups --region us-east-1
aws sagemaker list-training-jobs --region us-east-1 --max-results 5
aws sagemaker list-endpoints --region us-east-1
```

These are read-only and cost nothing, but each produces a CloudTrail event.

## The one distinction that is always tested

CloudTrail records the **API call**. It does not record the **content of the prompt or the model's response**.

When you call `InvokeModel`, the CloudTrail event tells you that identity X invoked model Y at time Z from IP address A. It does **not** contain the prompt text or the completion.

To capture prompt and response content you must enable **Amazon Bedrock model invocation logging** separately, in the Bedrock console under model invocation logging settings, choosing an Amazon S3 bucket or a CloudWatch Logs group (or both) as the destination.

| Requirement | Correct service |
|---|---|
| Who called the Bedrock API, and when | **CloudTrail** |
| The actual prompt text and model response | **Bedrock model invocation logging** |
| Invocation count, latency, token counts | **CloudWatch metrics** |
| Whether resources are configured compliantly | **AWS Config** |

Write these four rows into your notes. The distinction between the first two is the single most commonly missed point in this domain, and it is directly relevant to the assessment question about logging Bedrock API calls.

Wait two to five minutes before the next step — CloudTrail events are typically visible in Event history within about 15 minutes of the call, and often much sooner.

---

### Step 2 — Inspect a real CloudTrail event: identity, action, timestamp

This is the core exercise of the lab. You are going to open a real event from your own account and extract the three facts an auditor asks for.

## Find your Bedrock events

In the console, open `https://console.aws.amazon.com/cloudtrail/` and in the left navigation choose **Event history**. Set the lookup attribute to **Event source** and enter `bedrock.amazonaws.com`.

Or from the CLI:

```bash
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventSource,AttributeValue=bedrock.amazonaws.com \
  --max-results 5 \
  --region us-east-1
```

Pick the `GetFoundationModel` event you generated in Step 1 and open its full JSON. In the console, select the event and choose to view the event record.

## Extract the three facts

Work through the JSON and write down the answers. A typical event record looks like this — **your values will differ; this is illustrative structure, not real data from your account**:

```json
{
  "eventVersion": "1.09",
  "userIdentity": {
    "type": "IAMUser",
    "principalId": "AIDAEXAMPLEPRINCIPALID",
    "arn": "arn:aws:iam::111122223333:user/lab-student",
    "accountId": "111122223333",
    "userName": "lab-student"
  },
  "eventTime": "2026-07-20T09:14:52Z",
  "eventSource": "bedrock.amazonaws.com",
  "eventName": "GetFoundationModel",
  "awsRegion": "us-east-1",
  "sourceIPAddress": "203.0.113.42",
  "userAgent": "aws-cli/2.x.x",
  "requestParameters": { "modelIdentifier": "..." },
  "responseElements": null,
  "eventID": "EXAMPLE-EVENT-ID",
  "readOnly": true,
  "eventType": "AwsApiCall",
  "managementEvent": true,
  "recipientAccountId": "111122223333"
}
```

Answer these from **your own** event:

1. **WHO — identity.** Find `userIdentity`. What is the `type`, and what is the `arn`?
2. **WHAT — action.** Find `eventName` and `eventSource`. Which API was called, on which service?
3. **WHEN — timestamp.** Find `eventTime`. Note that it is in **UTC**, in ISO 8601 format, always ending in `Z`.

## Read the identity field properly

The `userIdentity.type` field is where audit investigations begin, and each value tells a different story:

| `type` | What it means | Where to look next |
|---|---|---|
| `Root` | The account root user. Should be essentially never — this is an alert-worthy event on its own. | Why was root used at all? |
| `IAMUser` | A long-lived IAM user with access keys | `userName`, `accessKeyId` |
| `AssumedRole` | Someone assumed a role — the common case for applications, federated users and SSO | `sessionContext.sessionIssuer` for the role, and `sessionContext.attributes` for MFA and session start time |
| `AWSService` | An AWS service acting on your behalf, e.g. SageMaker assuming an execution role | `invokedBy` |

For `AssumedRole`, the `arn` shows the *session*, not the person. To identify the human you follow `sessionContext.sessionIssuer.arn` to the role, and in a federated setup the session name usually carries the user identifier. **Roles obscure individual identity unless session naming is done well** — a real governance point, and a good discussion topic.

## Find the failed call

Now filter Event history by **Event name** = `GetFoundationModel`, and locate the deliberately failed call from Step 1. Its record contains fields the successful one does not:

- `errorCode` — for example `ValidationException` or `AccessDeniedException`
- `errorMessage` — the human-readable reason

**The call failed and was still recorded in full.** This is the property that makes CloudTrail an audit log rather than a success log. A burst of `AccessDeniedException` events from one principal across many services is the classic signature of credential misuse, and it is only detectable because failures are logged.

## Answer the assessment question

You should now be able to answer, in one sentence and without hesitation:

> *Which AWS service records who called the Amazon Bedrock API, which action they called and when?*
>
> **AWS CloudTrail.** It records the identity (`userIdentity`), the action (`eventName`), the timestamp (`eventTime`), the source IP and the outcome for every Bedrock API call — but **not** the prompt or response content, which requires Amazon Bedrock model invocation logging.

Say it out loud. Both halves of that sentence are examinable.

---

### Step 3 — Create a trail for long-term audit retention

Event history gave you 90 days for free. Most compliance regimes require considerably longer, and Event history cannot be queried at scale or protected from tampering. That is what a **trail** is for.

## What a trail adds

| | Event history (default) | A trail |
|---|---|---|
| Retention | 90 days, rolling | As long as you keep the S3 objects |
| Event types | Management events only | Management events, **data events**, Insights events |
| Destination | Console only | S3, and optionally CloudWatch Logs |
| Multi-Region | Current Region view | Can apply to all Regions in one trail |
| Integrity protection | None | **Log file validation** with digest files |
| Cost | Free | First copy of management events per Region is free; S3 storage, data events and additional copies are charged |

## Create the trail

```bash
aws s3api create-bucket \
  --bucket cloudtrail-ai-lab-<your-initials>-<random-number> \
  --region us-east-1
```

```bash
aws cloudtrail create-trail \
  --name ai-governance-trail \
  --s3-bucket-name cloudtrail-ai-lab-<your-initials>-<random-number> \
  --is-multi-region-trail \
  --enable-log-file-validation \
  --region us-east-1
```

```bash
aws cloudtrail start-logging --name ai-governance-trail --region us-east-1
```

If bucket-policy permissions cause the create call to fail, use the console instead — open `https://console.aws.amazon.com/cloudtrail/`, choose to create a trail, and let it create the bucket for you with the correct policy attached. The console handles the CloudTrail service-principal bucket policy automatically.

Verify:

```bash
aws cloudtrail get-trail-status --name ai-governance-trail --region us-east-1
```

`IsLogging: true` means it is recording.

## The three flags that matter

**`--is-multi-region-trail`.** An action taken in a Region you never use is more suspicious, not less. A single-Region trail is blind to it. Always make audit trails multi-Region.

**`--enable-log-file-validation`.** CloudTrail writes a signed digest file alongside the logs, letting you prove afterwards that no log file was modified or deleted. Without it, an attacker with S3 write access could edit the record of their own activity. Any exam question asking how to *prove log integrity* or *detect tampering* is answered by log file validation.

**S3 destination hardening.** The trail's bucket needs the same discipline as any other: Block Public Access on, encryption with a KMS key (Lab 23), and ideally **S3 Object Lock** or MFA delete so log objects cannot be removed even by an administrator. In a mature setup the trail writes to a bucket in a *separate* AWS account that the workload's administrators cannot reach at all. Separating the audited from the auditor is the underlying governance principle.

## Data events and why Bedrock is different

By default a trail records **management events** — control-plane calls like `CreateEndpoint` or `CreateTrainingJob`. **Data events** are high-volume resource operations, such as `s3:GetObject` on individual objects, and they are **not** logged by default because the volume and cost can be substantial.

For an AI workload this shapes two decisions:

- **S3 data events** on your training data bucket tell you *which specific objects* a training job or a person read. This is often exactly what an auditor wants, and exactly what management events do not give you. It is charged per event, so scope it to the sensitive prefixes rather than the whole account.
- **Bedrock `InvokeModel`** is recorded by CloudTrail as an API call, so you get the who/what/when. But as established in Step 2, **the prompt and completion content is not in the CloudTrail event.** For content you enable Amazon Bedrock model invocation logging to S3 or CloudWatch Logs, which is a Bedrock feature and not a CloudTrail one.

Keep those two mechanisms clearly separate in your mind. A question offering CloudTrail as the way to review *what users are asking the model* is offering the wrong answer.

## Query the trail with Athena (concept)

Once logs are in S3, the standard pattern for answering audit questions is **Amazon Athena**. The CloudTrail console can generate the Athena table definition for a trail's bucket for you. With it, an auditor's question becomes a SQL query — "list every distinct principal that called `bedrock:InvokeModel` in Q2, with a count per principal" is one `GROUP BY`.

You do not need to build this for the lab. Recognise the pattern: **CloudTrail collects, S3 retains, Athena queries.**

---

### Step 4 — Continuous compliance checking with AWS Config

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

---

### Step 5 — Model lineage and deployment approval with SageMaker Model Registry

Governance of an AI system is not only about API calls and resource configuration. It also has to answer questions about the model itself:

- Which exact dataset produced this model?
- Which version is in production right now?
- **Who approved it, and when?**
- If it starts behaving badly, what do we roll back to?

The SageMaker Model Registry exists to answer these.

## Data and model lineage

**Lineage** is the recorded chain from raw data to deployed model:

```
raw dataset (S3 object, versioned)
      │
      ▼
processing job  ──► curated dataset
      │
      ▼
training job  ──► model artifact + hyperparameters + container image
      │
      ▼
registered model package (versioned)
      │
      ▼
endpoint (production)
```

Without lineage, "which data trained the model that made this decision?" is unanswerable — and under regimes that grant a right to an explanation, or when a customer requests erasure, that is a serious position to be in. SageMaker's lineage tracking builds this graph automatically from the jobs you run, and Model Cards (Lab 22) are where the human-readable summary lives.

## Create a model package group

A **model package group** is a container for successive versions of one logical model. Every retraining produces a new **model package version** inside it.

```bash
aws sagemaker create-model-package-group \
  --model-package-group-name ai-lab-governance-demo \
  --model-package-group-description "Governance and approval walkthrough" \
  --region us-east-1
```

```bash
aws sagemaker list-model-package-groups --region us-east-1 \
  --query 'ModelPackageGroupSummaryList[].{Name:ModelPackageGroupName,Created:CreationTime}' \
  --output table
```

Creating a group costs nothing — you are creating metadata, not compute.

In the console, open `https://console.aws.amazon.com/sagemaker/` and find the model registry in the left navigation. Open your group. It is empty, because registering a version requires a trained model artifact from a real training job (Lab 04). Inspect the structure rather than populating it.

## The approval workflow

This is the governance mechanism, and it is what the exam asks about. Every registered model version carries an **approval status**:

| Status | Meaning |
|---|---|
| `PendingManualApproval` | Registered, evaluated, **not** cleared for production |
| `Approved` | A human with the right permission signed off |
| `Rejected` | Explicitly blocked from deployment |

The pattern:

1. A training pipeline registers a new version with status `PendingManualApproval`. Automation can produce a model; it cannot approve one.
2. A reviewer inspects the evaluation metrics, the bias report from SageMaker Clarify (Lab 20) and the model card (Lab 22).
3. If satisfied, they change the status to `Approved`:

   ```bash
   aws sagemaker update-model-package \
     --model-package-arn <model-package-arn> \
     --model-approval-status Approved \
     --region us-east-1
   ```

4. A deployment pipeline is configured to deploy only `Approved` versions, so the approval is a genuine gate rather than a note in a ticket.

Two governance properties fall out of this:

- **Separation of duties.** `sagemaker:UpdateModelPackage` can be granted to a distinct role, so the person who trains a model is not the person who approves it. That separation is a control auditors specifically look for.
- **Auditability.** The approval is an API call, so **CloudTrail records who approved which model version and when.** Go back to Event history and filter by event source `sagemaker.amazonaws.com` — your `CreateModelPackageGroup` call is there now, with your identity and timestamp on it.

That closes the loop of this entire lab: the registry provides the gate, and CloudTrail provides the proof that the gate was used.

## Rollback

Because every version is retained with its artifact and metadata, rolling back a bad model is a matter of pointing an endpoint configuration at an earlier approved version. Compare that with an environment where models are overwritten in an S3 prefix and nobody is certain which file is live. **Version control for models is an availability control as much as a governance one.**

## The governance stack, assembled

You have now met the whole of Domain 5. Fix the mapping:

| Governance question | Service |
|---|---|
| Who may call this model? | IAM (Lab 23) |
| Is the data encrypted, with keys we control? | KMS (Lab 23) |
| Does traffic stay off the public internet? | VPC endpoints (Lab 23) |
| Is there sensitive data in our S3 buckets? | Amazon Macie (Lab 24) |
| Is PII blocked at inference time? | Bedrock Guardrails (Lab 19) |
| Who called the API, and when? | **CloudTrail** |
| What did they actually prompt the model with? | **Bedrock model invocation logging** |
| Are our resources configured compliantly? | **AWS Config** |
| Which data produced this model? | **SageMaker lineage tracking** |
| Which version is approved for production? | **SageMaker Model Registry** |
| Where do we get AWS's own audit reports? | **AWS Artifact** |

If you can reproduce that table from memory, you are ready for this domain.

---

### Step 6 — Clean up

> **AWS Config is the item to deal with first.** Once enabled, the configuration recorder runs continuously and charges per configuration item recorded and per rule evaluation, indefinitely, with no prompt to review it. A CloudTrail trail also accrues S3 storage charges for as long as the log objects exist. Neither is dramatic on a lab account, but both bill silently forever if left in place.

## 1. Stop the AWS Config recorder and delete the rules

```bash
aws configservice describe-configuration-recorders --region us-east-1
```

```bash
aws configservice stop-configuration-recorder \
  --configuration-recorder-name <recorder-name> \
  --region us-east-1
```

Delete each rule you added:

```bash
aws configservice describe-config-rules --region us-east-1 \
  --query 'ConfigRules[].ConfigRuleName' --output table

aws configservice delete-config-rule \
  --config-rule-name <rule-name> \
  --region us-east-1
```

Then remove the recorder and the delivery channel:

```bash
aws configservice delete-delivery-channel --delivery-channel-name <channel-name> --region us-east-1
aws configservice delete-configuration-recorder --configuration-recorder-name <recorder-name> --region us-east-1
```

Stopping the recorder halts the charges; deleting it removes the configuration entirely.

## 2. Stop and delete the CloudTrail trail

```bash
aws cloudtrail stop-logging --name ai-governance-trail --region us-east-1
aws cloudtrail delete-trail --name ai-governance-trail --region us-east-1
```

Deleting the trail does **not** delete the logs it already wrote to S3 — those are ordinary S3 objects and continue to accrue storage charges until you remove them.

**Event history is unaffected by any of this.** It is on by default, cannot be turned off, is free, and will continue giving you 90 days of management events. That is the correct end state, not something to clean up.

## 3. Empty and delete the CloudTrail S3 bucket

```bash
aws s3 rm s3://cloudtrail-ai-lab-<your-initials>-<random-number>/ --recursive
aws s3api delete-bucket --bucket cloudtrail-ai-lab-<your-initials>-<random-number>
```

If you enabled S3 Object Lock or MFA delete on this bucket, deletion will be blocked — by design, since the whole point of those features is to make audit logs immutable. You would need to wait out the retention period.

Also delete the AWS Config delivery bucket if the setup wizard created a separate one.

## 4. Delete the model package group

```bash
aws sagemaker delete-model-package-group \
  --model-package-group-name ai-lab-governance-demo \
  --region us-east-1
```

If the group contained model package versions you would have to delete each version first with `aws sagemaker delete-model-package`. An empty group deletes directly.

## 5. Check for anything left running from earlier labs

This is the final lab in the course, so sweep the whole account. These resources bill **continuously**, by the hour, whether or not you use them, and are the most common source of an unexpected AWS bill:

```bash
aws sagemaker list-endpoints --region us-east-1
aws sagemaker list-notebook-instances --region us-east-1
aws sagemaker list-apps --region us-east-1
aws opensearchserverless list-collections --region us-east-1
aws kendra list-indices --region us-east-1
aws ec2 describe-vpc-endpoints --region us-east-1 --query 'length(VpcEndpoints)'
aws macie2 get-macie-session --region us-east-1
```

Every one of these should come back empty, zero, or with a not-found error. In particular:

- **SageMaker inference endpoints and notebook instances** bill per hour until deleted or stopped — endpoints must be *deleted*, and notebook instances *stopped or deleted*.
- **SageMaker Studio applications** keep running after you close the browser tab. Closing the tab is not shutting down.
- **OpenSearch Serverless collections** (Labs 15 and 16) bill for a minimum OCU capacity continuously and are among the most expensive things in this course to leave behind.
- **Amazon Kendra indexes** bill per hour from creation and have no free tier on the standard editions.

Repeat the checks in any other Region you worked in.

## 6. Verify the spend

Open the **Billing and Cost Management** console and review **Cost Explorer**, grouped by service, for the period covering this course. Anything still accruing tomorrow is something you missed today. Consider setting an AWS Budget with an alert so any future stray resource tells you within a day rather than at the end of the month.

---

### Verification

- [ ] I generated both successful and failed Bedrock API calls and found both in CloudTrail Event history
- [ ] From a real event in my own account I identified the `userIdentity` type and ARN, the `eventName` and the `eventTime`
- [ ] I located the `errorCode` on the failed call and can explain why logging failures matters
- [ ] I can answer, in one sentence, which service records who called the Bedrock API and when — and state what it does **not** record
- [ ] My trail was created multi-Region with log file validation enabled, and `get-trail-status` showed `IsLogging: true`
- [ ] I added at least one AWS Config managed rule and viewed its compliance result
- [ ] I created a model package group and can describe the three approval statuses and who should be able to set them
- [ ] Config recorder stopped and deleted, trail deleted, buckets emptied and deleted, model package group deleted
- [ ] I swept the account for SageMaker endpoints, notebooks and Studio apps, OpenSearch Serverless collections and Kendra indexes — all clear

### Discussion questions

1. Your security team asks for a record of every prompt sent to Amazon Bedrock last quarter. A colleague says CloudTrail already has it. Explain precisely why they are wrong and what you would need to enable instead — and note that enabling it today does not recover last quarter.
2. A CloudTrail event shows `userIdentity.type` of `AssumedRole`. Your incident report must name a person. Describe how you would trace from the session to a human, and what practice must have been in place beforehand for that to be possible.
3. Contrast CloudTrail and AWS Config using a single scenario: an S3 training-data bucket that became publicly readable last Tuesday. What does each service tell you, and why do you need both?
4. Why should log file validation and a separate audit account be considered part of the same control? What attack does each half address on its own?
5. A pipeline registers a new model version automatically after every retraining run. Explain why the default approval status should be `PendingManualApproval` rather than `Approved`, and which IAM permission enforces separation of duties.
6. An auditor asks for evidence that AWS's own data centres meet ISO 27001, and separately for evidence that your SageMaker notebooks cannot reach the internet. Name the service you would use for each, and explain why they are different services.

---

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.