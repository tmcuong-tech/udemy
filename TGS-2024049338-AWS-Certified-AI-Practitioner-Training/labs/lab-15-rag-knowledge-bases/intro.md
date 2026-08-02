# Lab 15 — RAG with Knowledge Bases for Amazon Bedrock

Build a retrieval augmented generation pipeline over your own documents with Knowledge Bases for Amazon Bedrock, read the citations, and prove the difference against an ungrounded model.

> ## ⚠️ COST WARNING
>
> This lab provisions a **vector store**, normally an **Amazon OpenSearch Serverless collection**. It bills continuously by the hour from creation until you delete it, **whether or not you query it**. Deleting the knowledge base does **not** reliably delete the collection underneath.
>
> **Complete this lab in one sitting and do the Clean up step in full.** Set an AWS Budgets alert before you start.

**What you will do:**
- Set a billing alert, upload three fictional policy documents to S3, and record an ungrounded baseline answer
- Walk through the RAG ingestion and query pipelines — chunking, embeddings, vector store, top-K
- Create a knowledge base over the S3 data source and record every resource it provisions
- Sync the data source and inspect raw retrieval separately from generation
- Run retrieve-and-generate and trace each claim back to its citation
- Compare grounded against ungrounded answers, then delete the knowledge base and its vector store
