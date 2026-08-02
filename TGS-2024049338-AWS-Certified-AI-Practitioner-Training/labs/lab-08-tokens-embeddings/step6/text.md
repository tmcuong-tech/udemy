# Step 6 — Clean up

This lab used **on-demand, serverless** inference only. No endpoint, index, collection or instance was created, so there is nothing running up a bill.

1. **Delete the local files** you created:

   ```bash
   rm -f embed-cat.json a.json b.json c.json d.json cosine.py
   ```

   Embedding output files are large — a single vector is hundreds of floating point numbers — and they clutter a working directory quickly.

2. **Unset the shell variables** if you are handing the terminal to someone else:

   ```bash
   unset MODEL_ID REGION
   ```

3. **Confirm you did not create a vector store.** Step 5 described the RAG pipeline but you did **not** build one. If you went exploring in the console and created any of the following, delete them **now** — every one of them bills continuously, whether you query it or not:

   | Resource | Why it matters |
   |---|---|
   | **OpenSearch Serverless collection** | Bills for a minimum capacity allocation from the moment it exists, independent of usage. This is the most expensive accidental resource in the whole course. |
   | **Bedrock Knowledge Base** | Creating one may create a vector store for you as a side effect — deleting the Knowledge Base does not always delete that store. Check both. |
   | **Kendra index** | Bills continuously per index. |
   | **Aurora / RDS cluster used for pgvector** | Bills per instance-hour. |

   Check the OpenSearch Serverless and Bedrock consoles directly if you are unsure.

   > **Do not leave these for "later".** They are the resources most likely to produce an unwelcome bill after a training day, precisely because nothing about them looks like it is running.

4. **Leave model access enabled** if you are continuing to Lab 09. Enabled access costs nothing; **invocations** are billed on tokens processed.

5. **Close the playground tab** so a stray keystroke does not submit another request.

**Checkpoint:** Local files removed, and you have confirmed no vector store, Knowledge Base or search index exists in your account.
