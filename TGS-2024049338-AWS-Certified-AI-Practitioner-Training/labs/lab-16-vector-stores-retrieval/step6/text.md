# Step 6 — Clean up

## ⚠️ Mandatory — the vector store is still billing

Your knowledge base is backed by a vector store that has been billing by the hour since it was created — in Lab 15 or at the start of this lab — and it will keep billing until deleted, whether or not you query it again.

**This is the last lab in the course that uses a knowledge base. There is no reason to keep it.** Delete everything.

Remember the trap from Lab 15: **deleting the knowledge base does not reliably delete the OpenSearch Serverless collection underneath.** They are separate resources. Check both.

### 1. Delete any extra data sources or knowledge bases

If you created a second data source or a second knowledge base in Step 2 to test chunking, delete those first. List everything so nothing is missed:

```bash
aws bedrock-agent list-knowledge-bases --region us-east-1
```

### 2. Delete the knowledge base

Console: open the **Knowledge bases** list, select it, delete it.

CLI:

```bash
aws bedrock-agent delete-knowledge-base \
  --knowledge-base-id <YOUR_KB_ID> \
  --region us-east-1
```

Confirm with `list-knowledge-bases` that nothing of yours remains.

### 3. Delete the vector store — the expensive one

```bash
aws opensearchserverless list-collections --region us-east-1
```

Match each result against the collection name in your resource table, then delete it:

```bash
aws opensearchserverless delete-collection --id <COLLECTION_ID> --region us-east-1
```

Re-run `list-collections` and confirm the result no longer contains your collection.

**If you created a second knowledge base for the chunking experiment, it very likely created a second collection.** Delete that one too. `list-collections` returning empty is the only acceptable result.

**Check every Region you worked in.** Both lists are Region-scoped, and a collection in a Region you switched away from is invisible in the console and still billing.

### 4. Remove the remaining resources

- **S3 bucket**, including any metadata files added in Step 4:

  ```bash
  aws s3 rm s3://northwind-kb-docs-<your-unique-suffix>/ --recursive
  aws s3 rb s3://northwind-kb-docs-<your-unique-suffix>
  ```

- **IAM service roles** created by the console for the knowledge bases. They do not bill, but they carry S3 read and Bedrock invoke permissions with no remaining purpose. Remove them from <https://console.aws.amazon.com/iam/>.
- **OpenSearch Serverless policies** — security, network, encryption and data access policies left behind by the deleted collections. They do not bill; remove them for a clean account.

### 5. Final verification

- [ ] `aws bedrock-agent list-knowledge-bases` shows none of yours, in every Region used
- [ ] **`aws opensearchserverless list-collections` shows none of yours, in every Region used**
- [ ] Second knowledge base and second collection from the chunking experiment also deleted
- [ ] S3 bucket emptied and deleted
- [ ] IAM service roles deleted
- [ ] Leftover OpenSearch Serverless policies removed

### 6. Check tomorrow's bill

Open the Billing and Cost Management console **the following day** and look at yesterday's spend by service. An OpenSearch Serverless line item means a collection survived somewhere — go back to step 3 and check every Region.

You are now past the expensive part of this course. Labs 17 and 18 walk through configuration without provisioning, and the remaining labs use serverless or low-cost services.

**Checkpoint:** Every box ticked, both list commands return nothing of yours in every Region you used, and you have a reminder to check tomorrow's bill.
