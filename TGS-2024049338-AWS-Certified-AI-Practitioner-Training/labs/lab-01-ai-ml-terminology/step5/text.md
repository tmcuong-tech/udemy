# Step 5 — Compare inferencing options: real-time versus batch

Once a model exists, *how* you run inference is a design decision with direct cost and
latency consequences. AIF-C01 expects you to pick the right option from a scenario.

### 5.1 The options

| Option | Latency | Input | Infrastructure | Bills |
|---|---|---|---|---|
| **Real-time endpoint** | Milliseconds | One request at a time | Always-on instances | Continuously, while the endpoint exists |
| **Batch transform** | Minutes to hours | A whole dataset in S3 | Spun up for the job, then torn down | Only for the job's duration |
| **Asynchronous inference** | Seconds to minutes | Large payloads, queued | Can scale to zero when idle | Only while processing (plus storage) |
| **Serverless inference** | Milliseconds, plus cold start | One request at a time | Managed, no instance to choose | Per request and duration |

### 5.2 Choosing between them

Ask two questions:

1. **Does a user or system wait for the answer?** If yes, you need real-time (or
   serverless) inference. A fraud check during checkout cannot wait.
2. **Do you have all the inputs already?** If yes, and nobody is waiting, batch transform
   is cheaper because nothing runs between jobs. Scoring last night's transactions,
   generating monthly churn scores, or captioning an archive of images are batch jobs.

Serverless inference is the middle ground for **intermittent, spiky traffic** where an
always-on endpoint would idle expensively and an occasional cold start is acceptable.
Asynchronous inference suits **large payloads or long processing times** — a several-minute
video, for example — where a synchronous HTTP request would time out.

### 5.3 Match the scenario

| Scenario | Best option |
|---|---|
| Recommend products as a shopper browses | |
| Score 40 million customer records once a month | |
| Caption uploaded 1 GB videos; results emailed when ready | |
| An internal tool used by 12 staff a few times a day | |

**Answer key:** real-time endpoint · batch transform · asynchronous inference ·
serverless inference.

### 5.4 Confirm in the console

1. In the **Amazon SageMaker AI** console left navigation, open **Batch transform jobs**
   (under the inference section) and note that a job has a *start* and an *end* — it is not
   a standing resource.
2. Open **Endpoints** again and note that an endpoint has a *status* of **InService** — it
   stands there until you delete it. That difference is exactly why Lab 04 carries a cost
   warning and this lab does not.
