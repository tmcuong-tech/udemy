# Step 2 — Inspect a real CloudTrail event: identity, action, timestamp

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
