# Step 4 — Connect the S3 data source and sync

An application with no data answers nothing. Now connect it to the documents you uploaded in Step 2.

1. Open your application in the Q Business console and find the **data sources** area.
2. Choose to **add a data source**. Browse the available connectors before picking one.

   Note how many there are. Connectors typically cover S3, web crawlers, document stores, wikis, ticketing systems, chat platforms, CRMs and file shares. **This connector catalogue is a large part of what you are buying** — each one is ingestion code, incremental sync logic and permission mapping that you would otherwise write and maintain yourself.

3. Choose the **Amazon S3** connector.
4. Configure it:
   - **Data source name** — something recognisable, such as `northwind-docs`
   - **IAM role** — let the console create one, so it has read access to your bucket
   - **Bucket and prefix** — your bucket from Step 2, with the prefix `docs/`
   - **Sync schedule** — choose **run on demand**. Do not schedule a recurring sync for a lab; a schedule keeps working on documents you no longer care about.
5. Add the data source, then **start a sync** manually.
6. Wait for the sync to complete. Watch the sync history and note what it reports: how many documents were **scanned**, **added**, **modified**, **deleted** and **failed**.

   > **If documents fail, the assistant will not know about them.** A common cause is the data source role lacking read access to the bucket. Check the sync history rather than assuming success — a Q Business application that answers "I don't know" is far more often a failed sync than a model limitation.

7. Confirm three documents were added successfully.

## What just happened

The sync did, as a managed service, exactly the indexing pipeline you built by hand in Lab 08:

| Lab 08, by hand | Q Business, managed |
|---|---|
| Chunk the documents | Done for you |
| Embed each chunk | Done for you — you do not choose the model |
| Store vectors in a vector store | The Q Business index |
| Track document permissions | Done for you, from the source system's ACLs |
| Re-sync when documents change | The connector's incremental sync |

You gave up all control over chunking strategy, embedding model and retrieval tuning. In exchange you wrote no code and manage no vector store. **That is the trade, and it is the right trade for a standard enterprise knowledge assistant** — Lab 15 shows the Bedrock Knowledge Bases route when you need the control back.

**Checkpoint:** The sync completed and the sync history shows three documents added and none failed.
