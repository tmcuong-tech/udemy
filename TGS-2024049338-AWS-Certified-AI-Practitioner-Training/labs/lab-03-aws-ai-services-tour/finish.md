# Well done!

You have completed Lab 03 — AWS Managed AI Services Tour:

✅ Extract meaning from text with Amazon Comprehend
✅ Translate text with Amazon Translate
✅ Synthesise speech with Amazon Polly
✅ Convert speech to text with Amazon Transcribe
✅ Analyse images with Amazon Rekognition
✅ Match services to use cases
✅ Clean up

**Key takeaways:**

- Managed AI services are pre-trained, API-driven and billed per unit processed — no training data, no infrastructure, no idle cost. Choosing SageMaker when a managed service would do is the classic wrong answer.
- Comprehend analyses text (sentiment, entities, key phrases, PII); it does not generate text. Generation is a Bedrock foundation-model job.
- Rekognition handles photos and video; Textract handles documents, forms and tables. The word "document" or "form" in a scenario points to Textract.
- Polly is text-to-speech and Transcribe is speech-to-text; SSML and lexicons control Polly output, while custom vocabulary and custom language models improve Transcribe accuracy on domain terms.
- Every managed AI service returns a confidence score. Designs need an explicit threshold and a human-review path for low-confidence or high-stakes results.
- Each service offers a real-time path and a batch or asynchronous path — the same trade-off you met in Lab 01.
- Custom capabilities (Comprehend custom classification, Rekognition Custom Labels, Comprehend endpoints) can create continuously billing resources; the base APIs do not.

**Next:** Lab 04 — Train and Deploy a Model with SageMaker
