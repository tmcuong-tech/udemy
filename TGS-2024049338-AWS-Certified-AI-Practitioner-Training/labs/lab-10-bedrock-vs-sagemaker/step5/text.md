# Step 5 — Classify ten scenarios

For each scenario choose **one** primary answer — **Managed service**, **Bedrock**, or **SageMaker** — and write **one sentence** justifying it. The justification matters more than the label; exam questions turn on the reason.

| # | Scenario | Your choice | Why (one sentence) |
|---|---|---|---|
| 1 | A retailer wants sentiment scores on 50,000 product reviews per day, as a number they can chart. | | |
| 2 | A law firm wants to summarise 80-page contracts in the firm's own house style. | | |
| 3 | A hospital has trained its own diagnostic model on proprietary imaging data and must host it inside its own VPC. | | |
| 4 | An insurer needs to read text out of scanned claim forms, including tables. | | |
| 5 | A startup wants a customer support chatbot answering from its own help centre articles. | | |
| 6 | A media company needs to detect inappropriate images uploaded by users. | | |
| 7 | A bank needs a research team to fine-tune an open-weights model on its own data and control the weights entirely. | | |
| 8 | A logistics firm wants to convert recorded driver voice notes into text. | | |
| 9 | An HR team wants to draft job descriptions from a few bullet points, in the company's tone of voice. | | |
| 10 | An e-commerce site wants product recommendations based on user browsing history. | | |

---

## Answers and reasoning

Check yours only after you have committed to all ten.

1. **Managed service** (Comprehend). Sentiment is exactly what it does, it returns a number with a confidence score, and at 50,000 a day the cost and latency advantage over per-token inference is decisive.
2. **Bedrock**. Summarisation in a specific house style is generation with a custom brief — no fixed API offers "summarise like this firm writes".
3. **SageMaker**. Their own model, their own weights, their own VPC. This is the case that forces SageMaker; nothing else can host it.
4. **Managed service** (Textract). Purpose-built for extracting text, forms and tables from scanned documents, and it returns structure rather than prose.
5. **Bedrock**. A chatbot grounded in their own documents is RAG — Knowledge Bases for Amazon Bedrock (Lab 15). Note the retrieval layer may add its own continuously billed vector store.
6. **Managed service** (Rekognition). Content moderation on images is a built-in capability with confidence scores you can threshold.
7. **SageMaker**. "Fine-tune an open-weights model and control the weights entirely" is the definition of the SageMaker case.
8. **Managed service** (Transcribe). Speech to text, purpose-built.
9. **Bedrock**. Open-ended generation from a short brief, in a specified tone. No fixed API does this.
10. **Managed service** (Personalize). Purpose-built recommendations. Note it is the one managed service that trains on *your* data — managed does not always mean one-size-fits-all.

## If you scored badly

The most common error is choosing **Bedrock** for scenarios 1, 4, 6, 8 and 10. A foundation model *could* attempt all of them — and would be slower, more expensive, less consistent, harder to audit, and would give you no confidence score.

> **Re-read the rule from Step 1: the most specific service that solves the problem is usually the right answer.** "It can do it" is not the same as "it should do it".

The second most common error is choosing **SageMaker** whenever the scenario mentions custom data. Custom *data* does not force SageMaker — RAG on Bedrock handles proprietary documents without any hosting. It is custom *model weights* and control over hosting that force SageMaker.

**Checkpoint:** All ten scenarios classified with a written justification, and you can explain any you got wrong.
