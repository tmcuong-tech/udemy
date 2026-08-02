# Step 7 — Clean up

## ⚠️ This step is mandatory

**You created a vector store. It has been billing by the hour since Step 3, and it will keep billing until you delete it — whether or not you ever query it again.**

The critical point, and the one most often missed: **deleting the knowledge base does not reliably delete the OpenSearch Serverless collection underneath it.** They are separate resources with separate lifecycles. You must check for and delete both.

> **Going straight to Lab 16?** Lab 16 extends this knowledge base, so you may keep it — **but only if you are starting Lab 16 now and will finish today.** If there is any chance you will not, delete everything now and rebuild it in Lab 16. Rebuilding costs a few minutes; a forgotten collection costs money every hour indefinitely.

Work through this in order.

### 1. Delete the knowledge base

Console: open the **Knowledge bases** list, select `northwind-kb`, and delete it. Read the confirmation dialog carefully — it may tell you explicitly whether the vector store will also be removed. Whatever it says, verify in step 2 anyway.

CLI:

```bash
aws bedrock-agent delete-knowledge-base \
  --knowledge-base-id <YOUR_KB_ID> \
  --region us-east-1
```

Confirm it is gone:

```bash
aws bedrock-agent list-knowledge-bases --region us-east-1
```

### 2. Delete the vector store — do not skip this

**This is the expensive resource.**

1. Open the Amazon OpenSearch Service console at <https://console.aws.amazon.com/aos/> and find the **Serverless** area, or list collections from the CLI:

   ```bash
   aws opensearchserverless list-collections --region us-east-1
   ```

2. Locate the collection created for your knowledge base — match it against the collection name you recorded in the Step 3 resource table.
3. **Delete the collection.**

   ```bash
   aws opensearchserverless delete-collection --id <COLLECTION_ID> --region us-east-1
   ```

4. Re-run `list-collections` and confirm the result is empty, or no longer contains your collection.

Deleting the collection can leave behind its associated **security, network, encryption and data access policies**. These do not bill, but they are clutter — remove them from the OpenSearch Serverless console if you want a clean account.

**Check every Region you worked in.** Both the knowledge base list and the collection list are Region-scoped. A collection created in a Region you then switched away from is invisible in the console and still billing.

### 3. Delete the S3 bucket

S3 storage for three text files is negligible, but leave nothing behind:

```bash
aws s3 rm s3://northwind-kb-docs-<your-unique-suffix>/ --recursive
aws s3 rb s3://northwind-kb-docs-<your-unique-suffix>
```

### 4. Delete the IAM service role

If you let the console create a service role for the knowledge base, it now has no purpose. IAM roles do not bill, but an unused role with S3 read and Bedrock invoke permissions is unnecessary standing access. Find it in the IAM console at <https://console.aws.amazon.com/iam/> and delete it.

### 5. Verify against your resource table

Go back to the table you filled in at Step 3 and tick off every row:

- [ ] Knowledge base deleted, and `list-knowledge-bases` confirms it
- [ ] **OpenSearch Serverless collection deleted, and `list-collections` confirms it**
- [ ] Checked every Region you worked in
- [ ] S3 bucket emptied and deleted
- [ ] IAM service role deleted
- [ ] Associated OpenSearch Serverless policies removed

### 6. Check your bill tomorrow

Open the Billing and Cost Management console **the following day** and look at yesterday's spend by service. This is the only way to be certain nothing is still running, and it is a habit worth forming — an alert fires on a threshold, but a daily glance catches a slow leak below it.

If you find an unexpected OpenSearch Serverless charge, a collection survived somewhere. Check every Region.

**Checkpoint:** Every box above ticked, `list-collections` returns nothing of yours in every Region you used, and you have a reminder to check tomorrow's bill.
