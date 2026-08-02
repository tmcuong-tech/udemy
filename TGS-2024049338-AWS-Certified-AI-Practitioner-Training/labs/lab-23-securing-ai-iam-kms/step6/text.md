# Step 6 — Clean up

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
