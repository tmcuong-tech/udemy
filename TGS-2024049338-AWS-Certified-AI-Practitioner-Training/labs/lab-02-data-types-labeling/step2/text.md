# Step 2 — Create an S3 bucket and organise a dataset

Amazon S3 is the default landing zone for ML data on AWS. SageMaker training jobs,
Ground Truth labelling jobs and batch transform jobs all read from and write to S3.

### 2.1 Create the bucket

1. Open the [Amazon S3 console](https://console.aws.amazon.com/s3/).
2. Choose **Create bucket**.
3. **Bucket name:** `aif-lab02-<your-initials>-<random-digits>` — bucket names are globally
   unique, so add something distinctive.
4. **AWS Region:** US East (N. Virginia) `us-east-1`. The bucket must be in the same Region
   as the Ground Truth job you create later.
5. Leave **Block all public access** enabled. Training data should never be public.
6. Leave default encryption at its default setting (server-side encryption is applied
   automatically) and choose **Create bucket**.

### 2.2 Create a prefix structure

Open the bucket and use **Create folder** to make these prefixes. A clear layout matters
more than it looks — Ground Truth writes output back into the same bucket, and you do not
want it mixed with your inputs.

```
tabular/
timeseries/
text/
images/
output/
```

> **Note:** S3 has no real folders. A "folder" is a key prefix — `images/photo1.jpg` is a
> single object whose name happens to contain a slash. The exam has been known to test this.

### 2.3 Create and upload sample files

On your own machine, create these two small files (any text editor will do).

`customers.csv` — tabular, structured:

```csv
customer_id,age,tenure_months,monthly_spend,region,churned
1001,34,18,82.50,APAC,0
1002,52,4,145.00,EMEA,1
1003,29,36,61.20,APAC,0
1004,41,9,210.75,AMER,1
1005,60,52,44.00,EMEA,0
```

`demand.csv` — time-series, structured:

```csv
timestamp,region,demand_mw
2026-01-01T00:00:00Z,APAC,4120
2026-01-01T01:00:00Z,APAC,3980
2026-01-01T02:00:00Z,APAC,3855
2026-01-01T03:00:00Z,APAC,3790
```

`reviews.txt` — unstructured text:

```text
The delivery was two days late but the packaging was excellent.
Battery life is far shorter than advertised. Disappointed.
Setup took five minutes and it has worked flawlessly since.
```

> **Teaching note:** these are illustrative sample records invented for this lab, not real
> customer or grid measurements. Never use production personal data in a training exercise.

Upload each file to its matching prefix using **Upload → Add files**.

### 2.4 Add images for the labelling job

You need a handful of images for Step 3. Use any 6–10 JPEG or PNG photos you own that fall
into two obvious visual categories — for example `cat` and `dog`, or `indoor` and
`outdoor`, or `damaged` and `undamaged`. Phone photos are fine. Keep them small
(under 1 MB each) so upload and labelling are quick.

Upload them all to the `images/` prefix.

> **Important:** do not upload photographs of identifiable people, or anything
> confidential. Ground Truth work team members will see every image you submit.
