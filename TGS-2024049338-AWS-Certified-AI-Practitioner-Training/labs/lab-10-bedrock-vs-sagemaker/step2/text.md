# Step 2 — Option A: a managed AI service (Amazon Comprehend)

Managed AI services are pre-trained models exposed through a task-specific API. You bring data, you get a result. There is no model to choose, no infrastructure, and no ML expertise required.

1. Open the Amazon Comprehend console at <https://console.aws.amazon.com/comprehend/>.
2. Find the real-time analysis area, keep the built-in model selected, and paste this text:

   ```
   The delivery was three days late and nobody answered the phone, but
   the replacement chair arrived quickly and the quality is excellent.
   Order 44192 was placed by Siti Rahman in Singapore on 3 April.
   ```

3. Run the analysis and look at each tab of results:
   - **Sentiment** — a label with confidence scores, not a paragraph of prose
   - **Entities** — people, places, dates, quantities extracted with types and confidence
   - **Key phrases**, **Language**, and **PII** if offered

4. Note what you did **not** do: you did not write a prompt, choose a model, set a temperature, or handle a context window. And note what you **got**: a **structured, typed result with a confidence score**.

## What this layer gives you that a foundation model does not

| Property | Managed AI service | Foundation model |
|---|---|---|
| Output shape | Structured and typed, always | Text you must parse and validate |
| Confidence score | Provided | Not provided — fluent output looks equally confident whether right or wrong |
| Determinism | Same input gives the same output | Varies between runs (Lab 09) |
| Latency | Typically milliseconds | Typically seconds |
| Cost per request | Typically lower | Per token, input and output |
| ML expertise needed | None | Prompt engineering |
| Auditability | Easy — a label and a score | Hard — free text |

> **That confidence score is the sleeper advantage.** It lets you route low-confidence cases to a human automatically. A foundation model gives you no equivalent signal — as Lab 09 demonstrated, a hallucination arrives with exactly the same confident tone as a correct answer.

## Other services in this layer

Recognise these by their task, since the exam tests exactly that mapping:

| Service | Task |
|---|---|
| **Amazon Comprehend** | NLP on text — sentiment, entities, key phrases, language, PII |
| **Amazon Rekognition** | Image and video analysis — objects, faces, moderation, text in images |
| **Amazon Transcribe** | Speech to text |
| **Amazon Polly** | Text to speech |
| **Amazon Translate** | Language translation |
| **Amazon Textract** | Extract text, forms and tables from scanned documents |
| **Amazon Personalize** | Recommendations |
| **Amazon Forecast** | Time-series forecasting |
| **Amazon Fraud Detector** | Fraud detection on transactions |

**The limitation of this layer:** you get exactly the task on offer and nothing else. If you need sentiment classified into your own eleven custom categories, or a summary written in your brand voice, no amount of configuration will produce it. That is when you move up to Bedrock.

**Checkpoint:** You have run text through Comprehend and can state two things its output gives you that a foundation model's does not.
