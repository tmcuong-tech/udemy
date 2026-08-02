# Lab 25 — Governance, Audit and Model Lineage

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

## Step 1 — Generate AI API activity to audit

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

## Step 2 — Inspect a real CloudTrail event: identity, action, timestamp

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

## Step 3 — Create a trail for long-term audit retention

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

## Step 4 — Continuous compliance checking with AWS Config

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

## Step 5 — Model lineage and deployment approval with SageMaker Model Registry

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

## Step 6 — Clean up

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

## Verification

- [ ] I generated both successful and failed Bedrock API calls and found both in CloudTrail Event history
- [ ] From a real event in my own account I identified the `userIdentity` type and ARN, the `eventName` and the `eventTime`
- [ ] I located the `errorCode` on the failed call and can explain why logging failures matters
- [ ] I can answer, in one sentence, which service records who called the Bedrock API and when — and state what it does **not** record
- [ ] My trail was created multi-Region with log file validation enabled, and `get-trail-status` showed `IsLogging: true`
- [ ] I added at least one AWS Config managed rule and viewed its compliance result
- [ ] I created a model package group and can describe the three approval statuses and who should be able to set them
- [ ] Config recorder stopped and deleted, trail deleted, buckets emptied and deleted, model package group deleted
- [ ] I swept the account for SageMaker endpoints, notebooks and Studio apps, OpenSearch Serverless collections and Kendra indexes — all clear

## Discussion questions

1. Your security team asks for a record of every prompt sent to Amazon Bedrock last quarter. A colleague says CloudTrail already has it. Explain precisely why they are wrong and what you would need to enable instead — and note that enabling it today does not recover last quarter.
2. A CloudTrail event shows `userIdentity.type` of `AssumedRole`. Your incident report must name a person. Describe how you would trace from the session to a human, and what practice must have been in place beforehand for that to be possible.
3. Contrast CloudTrail and AWS Config using a single scenario: an S3 training-data bucket that became publicly readable last Tuesday. What does each service tell you, and why do you need both?
4. Why should log file validation and a separate audit account be considered part of the same control? What attack does each half address on its own?
5. A pipeline registers a new model version automatically after every retraining run. Explain why the default approval status should be `PendingManualApproval` rather than `Approved`, and which IAM permission enforces separation of duties.
6. An auditor asks for evidence that AWS's own data centres meet ISO 27001, and separately for evidence that your SageMaker notebooks cannot reach the internet. Name the service you would use for each, and explain why they are different services.

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.
