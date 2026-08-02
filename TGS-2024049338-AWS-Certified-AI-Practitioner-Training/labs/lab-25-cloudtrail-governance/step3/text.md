# Step 3 — Create a trail for long-term audit retention

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
