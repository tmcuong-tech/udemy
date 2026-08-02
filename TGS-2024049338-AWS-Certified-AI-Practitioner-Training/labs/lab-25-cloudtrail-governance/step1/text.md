# Step 1 — Generate AI API activity to audit

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
