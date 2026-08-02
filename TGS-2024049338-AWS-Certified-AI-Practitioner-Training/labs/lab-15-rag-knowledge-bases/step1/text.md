# Step 1 — Cost warning, and prepare the S3 data source

## ⚠️ Read this before you create anything

**This is the most expensive lab in the course, and the only one that leaves behind a resource billing continuously by the hour.**

A knowledge base needs a **vector store**. If you let Bedrock create one for you, it will typically provision an **Amazon OpenSearch Serverless collection**. That collection bills on provisioned capacity units **from the moment it is created until you delete it** — continuously, around the clock, **whether or not you ever run a single query**. Deleting the knowledge base does **not** always delete the collection underneath it.

Four rules for this lab:

1. **Complete the lab in one sitting.** Do not create the knowledge base at the start of the day and clean up tomorrow.
2. **Do Step 7 — Clean up.** It is not optional here. It deletes the knowledge base **and** the vector store, and it verifies the deletion.
3. **Set a billing alert before you begin** if you have not already. AWS Budgets can notify you on a threshold. Do this now.
4. **Check current pricing yourself** on the official Amazon OpenSearch Serverless and Amazon Bedrock pricing pages before creating anything. Do not rely on any figure quoted from memory or from older course material.

If you are working in a shared classroom account, confirm with your trainer before creating a knowledge base. If time is short, read this lab through and run the walkthrough steps without provisioning — Steps 2, 6 and 7 still teach most of the content.

Lab 16 extends this same knowledge base. If you intend to do Lab 16 immediately afterwards, you may keep the knowledge base between the two labs — but **only** if you will finish both today.

---

## Create the data source

RAG needs documents. You will create three small text files describing a fictional company so that the model cannot possibly answer from its training data — which is exactly what makes the demonstration honest.

### Create the S3 bucket

Bucket names are globally unique, so substitute your own suffix.

```bash
aws s3 mb s3://northwind-kb-docs-<your-unique-suffix> --region us-east-1
```

Or in the console: open <https://console.aws.amazon.com/s3/>, choose **Create bucket**, name it, and keep **Block all public access** enabled. There is no reason for these documents to be public, and a knowledge base reads them through an IAM role, not through public access.

### Create three documents

Create these locally, then upload them. The content is deliberately fictional.

**`shipping-policy.txt`**

```
Northwind Logistics Shipping Policy, revision 4.

Standard delivery within Singapore is 2 working days. Standard delivery to
Malaysia and Indonesia is 5 working days.

Express delivery is available in Singapore only and is next working day for
orders placed before 1400 hours.

Temperature-controlled shipping is available for perishable goods. It is
offered on the Singapore domestic network only and requires 24 hours notice.

Northwind does not ship lithium batteries, aerosols, or live animals.

Deliveries are not made on Sundays or public holidays.
```

**`claims-policy.txt`**

```
Northwind Logistics Claims Policy, revision 2.

A damage claim must be filed within 7 calendar days of delivery. A claim for
a parcel that never arrived must be filed within 21 calendar days of the
despatch date.

Claims above 500 Singapore dollars require review by an operations manager
and photographic evidence.

Temperature excursion claims on perishable goods are treated as priority and
must be acknowledged within 4 working hours.

Northwind's maximum liability for a standard parcel without declared value
is 100 Singapore dollars.
```

**`service-tiers.txt`**

```
Northwind Logistics Service Tiers.

Tier Bronze: standard delivery, email support, no service credit.
Tier Silver: standard delivery, email and phone support, 5 percent service
credit for a delivery more than 2 days late.
Tier Gold: express delivery included, dedicated account manager, 10 percent
service credit for any late delivery, and priority claims handling.

Tier is assigned annually based on shipment volume in the previous calendar
year. Gold requires more than 5000 shipments.
```

Upload them:

```bash
aws s3 cp shipping-policy.txt s3://northwind-kb-docs-<your-unique-suffix>/
aws s3 cp claims-policy.txt   s3://northwind-kb-docs-<your-unique-suffix>/
aws s3 cp service-tiers.txt   s3://northwind-kb-docs-<your-unique-suffix>/
```

Confirm all three are present:

```bash
aws s3 ls s3://northwind-kb-docs-<your-unique-suffix>/
```

### Establish the baseline now

Before building anything, open the Bedrock **Chat** playground, select a text model, and ask:

```
What is Northwind Logistics' maximum liability for a standard parcel with
no declared value?
```

Record the answer verbatim. The model has never seen these documents. It will either decline to answer or **produce a confident, plausible, entirely invented figure** — which is the more instructive outcome. Keep this answer; Step 6 compares against it.

**Checkpoint:** Billing alert set, three documents in an S3 bucket, and a recorded baseline answer from a model with no access to them.
