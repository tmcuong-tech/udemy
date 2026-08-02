# Step 1 — What Amazon Q Business is, and what it will cost you

Amazon Q Business is a **managed generative AI assistant for enterprise data**. You point it at your organisation's content, it indexes that content, and employees ask questions in natural language and get answers **with citations back to the source documents**.

Everything you built by hand in Lab 08 and argued for in Lab 09 — retrieval, grounding, citations — Q Business provides as a managed service. You supply documents and permissions; you do not supply prompts, an embedding model, a vector store or any code.

## Where it sits in Lab 10's framework

| Layer | Example |
|---|---|
| Managed AI service | Comprehend, Rekognition |
| **Managed generative AI application** | **Amazon Q Business** |
| Foundation model API | Amazon Bedrock |
| Build and host it yourself | SageMaker |

Q Business sits **above** Bedrock. Where Bedrock gives you a model and you build the RAG pipeline, Q Business gives you the finished application. You trade control for speed: you cannot choose the model or write the prompt, but you get a working, permission-aware, cited assistant in an afternoon.

## Cost warning — read this before Step 3

> ### Amazon Q Business is not free tier, and it bills continuously.
>
> - A Q Business application is charged on a **per-user subscription** basis, and index capacity is charged for **as long as the application exists** — not per question asked.
> - **Closing the browser does not stop the charge. Only deleting the application does.**
> - This is fundamentally unlike the Bedrock labs, where on-demand inference cost nothing when idle.
>
> **Before you begin, decide which applies to you:**
>
> 1. **You are in a managed classroom account** — your trainer will confirm whether you should create an application or follow along on a shared one.
> 2. **You are using your own account** — check the current Amazon Q Business pricing page and confirm you accept the charge. Then complete the lab **in one sitting** and delete the application in Step 7 the same day.
> 3. **You do not want to incur the cost** — read Steps 2 to 6 for the concepts and skip the creation. The exam tests what Q Business *is* and *when to use it*, not your ability to click through the wizard.
>
> Do not create the application and come back to it tomorrow. That is the decision that produces a bill.

## What Q Business does that a raw model cannot

- **Connects to enterprise data sources** through built-in connectors, rather than you writing ingestion code
- **Respects existing permissions** — a user should only get answers from documents they are already allowed to read. This is the hardest part of enterprise RAG and the main reason to buy rather than build.
- **Cites its sources**, so an answer can be checked (Lab 09's mitigation, built in)
- **Provides a ready-made web experience** with user authentication
- **Declines when the answer is not in the documents** — the grounding behaviour you had to prompt for by hand in Lab 09

**Checkpoint:** You can explain how Q Business differs from Bedrock, and you have made an explicit decision about whether to incur the cost.
