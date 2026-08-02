# Tools and Setup

Everything needed before starting the labs.

## AWS account

Create a free tier account: https://aws.amazon.com/free/

Before you begin, secure it:

- Enable MFA on the root user.
- Create an IAM admin user and stop using root for daily work.
- Set a billing alarm so runaway resources surface early.

## AWS CLI

Install the AWS CLI, then configure it:

```bash
aws configure
aws sts get-caller-identity
```

Set the working region and a few conveniences:

```bash
export AWS_DEFAULT_REGION=us-east-1
export AWS_PAGER=""
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
```

## Amazon Bedrock model access

Labs 06 onward need foundation model access. Request it before class:

1. Open the Amazon Bedrock console: https://console.aws.amazon.com/bedrock/
2. In the left navigation, choose **Model access**.
3. Request access to the models you need.

Approval is not always instant, and available models vary by Region — check the
Model access page for what is available in yours.

## Cost awareness

Most labs stay within the free tier, but several create resources that bill
continuously until deleted:

| Resource | Used in |
|---|---|
| SageMaker notebook instances, Studio apps, inference endpoints | Labs 04, 05, 20, 21, 22 |
| OpenSearch Serverless collections (behind Bedrock knowledge bases) | Labs 15, 16 |
| Amazon Q Business applications | Lab 11 |
| Amazon Macie discovery jobs (charged by data volume) | Lab 24 |
| Bedrock provisioned throughput | Lab 17 — **do not provision in class** |

Deleting a Bedrock knowledge base does **not** reliably delete the vector store
beneath it. After Labs 15 and 16, verify with:

```bash
aws opensearchserverless list-collections
```

Check every Region you worked in — a collection left in an unused Region is
invisible in the console and still billing.

## Verify your setup

```bash
aws sts get-caller-identity          # returns your account and identity
aws bedrock list-foundation-models   # returns models available in your Region
```

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.
