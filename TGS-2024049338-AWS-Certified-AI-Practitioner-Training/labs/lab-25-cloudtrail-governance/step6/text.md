# Step 6 — Clean up

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
