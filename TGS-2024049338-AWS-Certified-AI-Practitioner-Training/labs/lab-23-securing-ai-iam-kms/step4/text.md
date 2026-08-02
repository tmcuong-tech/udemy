# Step 4 — Encrypt a training data bucket at rest, and understand encryption in transit

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
