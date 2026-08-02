# Step 3 — Create the knowledge base

> **This is the step that starts the meter.** Creating a knowledge base with a Bedrock-managed vector store provisions an OpenSearch Serverless collection that bills continuously from creation until deletion. Note the time you create it. Do not leave this lab unfinished.

### Enable an embedding model

Before creating anything, confirm you have access to an embedding model:

1. Open the Bedrock console at <https://console.aws.amazon.com/bedrock/> and check your Region.
2. In the left navigation choose **Model access**.
3. Confirm access is granted to at least one **embeddings** model and at least one **text** model. Embedding models are listed separately from text models and are easy to overlook — a knowledge base cannot be created without one.

### Create the knowledge base

1. In the left navigation, choose the **Knowledge bases** area and start creating a knowledge base.
2. **Name and description.** Name it something you will recognise when cleaning up — `northwind-kb` is fine.
3. **IAM permissions.** Let the console **create and use a new service role** unless your organisation requires otherwise. This role needs to read your S3 bucket, call the embedding model, and write to the vector store. If you supply your own role and the sync fails later, missing permissions on one of those three is the usual cause.
4. **Data source.** Choose **Amazon S3** and browse to the bucket you created in Step 1. Point at the bucket, or at a prefix within it. Note that other data source types may be offered — check the console for what is available in your Region.
5. **Chunking strategy.** You are asked how to split the documents. For this first pass choose the **default** strategy. Do not tune it yet — Lab 16 changes this deliberately and compares results, and you need an untuned baseline for that comparison to mean anything.

   Note what the console tells you here, particularly: **chunking configuration cannot be changed on an existing data source.** To change it you delete and recreate the data source, then re-sync. This is a real operational constraint worth remembering.

6. **Embeddings model.** Select the embedding model you enabled. Note its name — this choice is locked in for the life of the knowledge base, because changing it would invalidate every stored vector.
7. **Vector store.** You will be offered a choice between letting Bedrock create one for you and connecting one you already run.

   > **Pause here.** Selecting the quick-create option provisions an **Amazon OpenSearch Serverless collection**. Read whatever the console tells you about this on screen. This collection bills by the hour from creation, independently of the knowledge base, and it is the resource people forget in cleanup. Note down the collection name shown, if one is displayed — you will need it in Step 7.

8. **Review and create.** Creation takes several minutes while the vector store is provisioned and the index is set up.

### Record what was created

Before moving on, write down:

| Item | Value |
|---|---|
| Knowledge base name | |
| Knowledge base ID | |
| Region | |
| S3 bucket name | |
| Vector store type | |
| OpenSearch Serverless collection name | |
| Embedding model | |
| Time created | |

This table **is** your cleanup checklist. Filling it in now is the difference between a clean teardown and an unexplained bill.

You can confirm the knowledge base exists from the CLI:

```bash
aws bedrock-agent list-knowledge-bases --region us-east-1
```

And, if a collection was created for you:

```bash
aws opensearchserverless list-collections --region us-east-1
```

Run both now, so you know what "present" looks like. In Step 7 you will run the same two commands and expect them to come back empty.

**Checkpoint:** Knowledge base created, and every row of the resource table filled in.
