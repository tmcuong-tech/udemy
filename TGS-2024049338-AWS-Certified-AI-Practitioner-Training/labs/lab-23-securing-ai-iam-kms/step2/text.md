# Step 2 — Write a least-privilege IAM policy scoped to specific Bedrock models

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
