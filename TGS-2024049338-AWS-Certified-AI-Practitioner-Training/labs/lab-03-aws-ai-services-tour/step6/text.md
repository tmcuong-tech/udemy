# Step 6 — Match services to use cases

You have now used five managed AI services. The exam rarely asks what a service *is* — it
describes a business requirement and asks which service meets it. This step builds the
lookup table you need.

### 6.1 The AWS managed AI service map

| Service | Modality | Core capability |
|---|---|---|
| **Amazon Comprehend** | Text | Sentiment, entities, key phrases, language, PII, topic modelling |
| **Amazon Translate** | Text | Neural machine translation between languages |
| **Amazon Polly** | Text → audio | Text-to-speech synthesis |
| **Amazon Transcribe** | Audio → text | Speech-to-text, batch and streaming |
| **Amazon Rekognition** | Image, video | Objects, scenes, faces, moderation, text in images |
| **Amazon Textract** | Document image → structured text | Forms, tables, key-value extraction |
| **Amazon Lex** | Text, voice | Conversational bot — intents, slots, dialogue |
| **Amazon Kendra** | Documents | Intelligent enterprise search over your content |
| **Amazon Personalize** | User-item interactions | Recommendations and personalised ranking |
| **Amazon Fraud Detector** | Tabular events | Online fraud risk scoring |

> **Teaching note:** this table lists capabilities, not availability. Confirm service and
> feature availability for your own Region in the console before designing a solution.

### 6.2 Match the requirement

For each requirement, name the service. Some need more than one.

| # | Requirement | Service(s) |
|---|---|---|
| 1 | Publish a news article as an audio version for visually impaired readers | |
| 2 | Automatically pull the invoice number and total from scanned supplier PDFs | |
| 3 | Flag user-uploaded photos containing unsafe content before they go live | |
| 4 | Route inbound support emails by topic and urgency | |
| 5 | Produce searchable, speaker-attributed transcripts of recorded sales calls | |
| 6 | Show a Japanese customer your English product catalogue in Japanese | |
| 7 | Recommend the next product to each shopper based on browsing history | |
| 8 | Let staff ask questions in plain English across an internal document store | |
| 9 | Build a voice bot that books appointments | |
| 10 | Caption a live webinar in real time | |

**Answer key:** 1 Polly · 2 Textract · 3 Rekognition (image moderation) · 4 Comprehend
(sentiment plus custom classification) · 5 Transcribe with speaker partitioning ·
6 Translate · 7 Personalize · 8 Kendra · 9 Lex (with Polly and Transcribe underneath) ·
10 Transcribe streaming.

### 6.3 The decision rule for the exam

Work through these questions in order:

1. **Is there a managed AI service for this exact task?** If yes, choose it. It needs no
   training data, no infrastructure and no ML expertise.
2. **Does it need to generate new content, reason over a prompt, or hold a conversation?**
   Then it is a foundation model on **Amazon Bedrock** (Domain 2).
3. **Is the task specific to your own data and unlike anything pre-trained?** Then it is a
   custom model on **SageMaker** (Lab 04), or a customisation feature such as Comprehend
   custom classification or Rekognition Custom Labels.

Choosing SageMaker when a managed service would do is the classic wrong answer: it adds
training data requirements, ML expertise and undifferentiated operational effort for no
benefit.

### 6.4 The shared characteristics

Every service in this lab shares four traits worth stating explicitly, because they turn
up as distractors:

- **Pre-trained** — you supply no training data to use the base capability.
- **API-driven and serverless to you** — no instances to size, no endpoints to keep alive.
- **Pay per unit processed** — characters, seconds of audio, images. No idle cost.
- **Probabilistic** — every result has a confidence score, and every design needs a
  threshold and a human-review path for low-confidence or high-stakes cases.
