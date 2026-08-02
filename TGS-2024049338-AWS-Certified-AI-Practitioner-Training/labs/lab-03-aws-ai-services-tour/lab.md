# Lab 03 — AWS Managed AI Services Tour

Use Amazon Comprehend, Translate, Polly, Transcribe and Rekognition from the console, and learn to match each managed AI service to a business use case.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 1 — Fundamentals of AI and ML (20%)
**Task statement:** 1.2 Identify practical use cases for AI
**WSQ mapping:** LU3 · Topic 5 Exploring AI Use Cases · K7 · A3 · LO3
**Slide reference:** v11 deck slides 52–83
**Estimated time:** 40 minutes

**Learning objectives:**
- Use Amazon Comprehend to extract sentiment, entities, key phrases, language and PII from free text
- Perform neural machine translation with Amazon Translate and describe how custom terminology controls brand terms
- Synthesise speech with Amazon Polly and control pronunciation and pacing with SSML
- Create an Amazon Transcribe job and evaluate the transcript against known ground truth
- Detect labels, moderate content and read text in images with Amazon Rekognition, and distinguish it from Amazon Textract
- Select the correct AWS AI service for a described business requirement

---

## Step 1 — Extract meaning from text with Amazon Comprehend

Amazon Comprehend is a managed **natural language processing** service. You send text, it
returns sentiment, entities, key phrases, language and PII — with no model to train and no
infrastructure to run.

> **Cost note:** every service in this lab bills per unit of input processed (characters,
> characters translated, seconds of audio, images analysed). The volumes here are tiny, and
> several of these services include a free tier for new accounts. Nothing you create in
> Steps 1–5 runs continuously; Step 7 removes the one storage resource you make.

### 1.1 Open real-time analysis

1. Open the [Amazon Comprehend console](https://console.aws.amazon.com/comprehend/) in
   `us-east-1`.
2. In the left navigation, choose **Real-time analysis**.
3. Leave the analysis type set to the built-in option (rather than a custom model).

### 1.2 Analyse a sample

1. Clear the sample text and paste this in the input box:

```text
I ordered the AeroTrack X2 from Contoso Retail in Singapore on 14 March. Delivery was
three days late and the courier left it in the rain, so the box was soaked. Support did
answer within an hour and shipped a replacement, which arrived perfectly. Call me on
+65 6555 0100 if you need the order number.
```

2. Choose **Analyze**.

### 1.3 Read each output tab

Work through the result tabs and note what each one gives you:

| Tab | What it returns | Why it matters |
|---|---|---|
| **Sentiment** | One of `POSITIVE`, `NEGATIVE`, `NEUTRAL`, `MIXED`, with confidence scores | Note that this text should score **MIXED** — a late, damaged delivery but good support. A single overall label hides that nuance. |
| **Entities** | Detected entities with types such as `ORGANIZATION`, `LOCATION`, `DATE`, `COMMERCIAL_ITEM`, `QUANTITY` | This is how you turn free text into structured fields. |
| **Key phrases** | The noun phrases that carry the content | Useful for tagging and search. |
| **Language** | Detected dominant language with a confidence score | Feeds the translation step that follows. |
| **PII** | Detected personally identifiable information and its offsets | It should flag the phone number. This is the feature you use for redaction. |
| **Targeted sentiment** | Sentiment attached to each specific entity | Shows negative sentiment towards delivery and positive towards support — the nuance the overall label lost. |

### 1.4 Note the confidence scores

Every result carries a **confidence score** between 0 and 1. Managed AI services are
probabilistic, not deterministic. Two consequences the exam expects you to know:

- You should set a **confidence threshold** appropriate to the risk of being wrong, and
  route low-confidence results to a human.
- Confidence is **not** accuracy. A high-confidence wrong answer is entirely possible.

### 1.5 Note what Comprehend does not do

Comprehend classifies and extracts. It does not *generate* text. If the requirement is
"summarise these reviews in a paragraph" or "draft a reply", that is a generative AI job
for Amazon Bedrock (Domain 2), not Comprehend. Choosing between an analytical managed
service and a foundation model is a recurring exam theme.

> **Optional:** Comprehend also supports **custom classification** and **custom entity
> recognition**, where you supply labelled examples and it trains a model for you. Those
> create asynchronous training jobs and take longer than this lab allows — look at the
> **Custom classification** page in the left navigation to see where they live, but do not
> start a job.

---

## Step 2 — Translate text with Amazon Translate

Amazon Translate is managed **neural machine translation**. It pairs naturally with
Comprehend: detect the language, then translate it.

### 2.1 Run a real-time translation

1. Open the [Amazon Translate console](https://console.aws.amazon.com/translate/) in
   `us-east-1`.
2. In the left navigation, choose **Real-time translation**.
3. Set **Source language** to **Auto (auto)** — Translate will call language detection for
   you, the same capability you saw in Comprehend.
4. Set **Target language** to a language you can sanity-check, or to **Chinese (Simplified)**.
5. Paste the review text from Step 1.2 into the source box.

The translation appears as you type. Note the detected source language shown next to the
**Auto** setting.

### 2.2 Translate back and inspect the loss

1. Copy the translated output.
2. Swap the languages: set the source to your target language and the target back to
   **English**.
3. Paste the translation in and compare the round-trip result with your original.

Round-tripping is a quick, informal quality check. Product names, idioms and units are
where meaning drifts. Two things follow:

- Machine translation output should be **reviewed by a human when the stakes are high** —
  legal, medical or safety-critical text.
- Named entities such as `AeroTrack X2` and `Contoso Retail` should usually be left
  untranslated.

### 2.3 See how you would control brand terms

You cannot fix brand-name translations by prompting — Translate has no prompt. Instead it
offers two customisation features. Open each page in the left navigation and read the
description; do not create anything.

| Feature | What it does | Use when |
|---|---|---|
| **Custom terminology** | A CSV of source-to-target term pairs that Translate applies verbatim | Brand names, product names, internal jargon |
| **Parallel data / Active Custom Translation** | Example translated sentence pairs that adapt output style and domain | Domain-specific tone, e.g. legal or medical register |

### 2.4 Note the batch option

**Real-time translation** handles one piece of text at a time. For a folder of documents,
the **Batch translation** page runs an asynchronous job that reads from one S3 prefix and
writes to another — the same real-time-versus-batch trade-off you met in Lab 01. Look at
the page, but do not start a job; batch jobs take longer than this lab allows.

---

## Step 3 — Synthesise speech with Amazon Polly

Amazon Polly is managed **text-to-speech (TTS)**. It turns written text into lifelike
spoken audio.

### 3.1 Create an S3 bucket for this lab

You will need somewhere to keep the audio file for Step 4.

1. Open the [Amazon S3 console](https://console.aws.amazon.com/s3/) and choose
   **Create bucket**.
2. **Bucket name:** `aif-lab03-<your-initials>-<random-digits>`.
3. **Region:** `us-east-1`. Leave **Block all public access** enabled.
4. Choose **Create bucket**.

### 3.2 Synthesise speech

1. Open the [Amazon Polly console](https://console.aws.amazon.com/polly/) in `us-east-1`.
2. In the left navigation, choose the text-to-speech page.
3. Paste this text — write it exactly, because you will check whether Transcribe recovers
   it in Step 4:

```text
Good morning. This is a test recording for the AWS Certified AI Practitioner course.
Our quarterly revenue increased by fourteen percent, and customer satisfaction reached
ninety two points.
```

4. Choose an **engine**. The console lists the engines available to your account and
   Region — the neural and newer engines generally sound more natural than the standard
   engine, and voice availability differs per engine.
5. Choose a **language** and a **voice**.
6. Choose **Listen** to preview the audio.

### 3.3 Compare voices and engines

1. Re-synthesise the same text with a different engine or voice and listen again.
2. Note where the two differ: prosody, pauses, and how each handles "ninety two points".

Voice choice is a real product decision — the exam frames Polly use cases as accessibility,
IVR/contact-centre prompts, e-learning narration, and reading long-form content aloud.

### 3.4 Control pronunciation with SSML

1. Switch the input mode from plain text to **SSML**.
2. Try this, which wraps the text in the required `speak` element and inserts a pause:

```xml
<speak>
  Good morning. This is a test recording.
  <break time="1s"/>
  Our quarterly revenue increased by <prosody rate="slow">fourteen percent</prosody>.
</speak>
```

3. Choose **Listen** and note the inserted pause and the slowed phrase.

**Speech Synthesis Markup Language (SSML)** is how you control pauses, emphasis, speaking
rate and pronunciation. **Lexicons** (in the left navigation) go further, mapping specific
words — an acronym, a brand name — to a fixed pronunciation across all your text.

### 3.5 Save the audio

1. Switch back to plain text mode and restore the Step 3.2 text.
2. Use the download option to save the synthesised audio as an MP3 to your machine.
3. In the S3 console, upload that MP3 into your `aif-lab03-...` bucket.

> **Note:** Polly can also write directly to S3 from the console using an asynchronous
> synthesis task, which is the right choice for long documents. Downloading and uploading
> is simpler for a single short clip.

You now have a **real audio file with known ground-truth text** — exactly what you need to
evaluate a speech-to-text service.

---

## Step 4 — Convert speech to text with Amazon Transcribe

Amazon Transcribe is managed **automatic speech recognition (ASR)** — the inverse of Polly.
You will transcribe the audio you just generated and compare the result with the text you
typed.

### 4.1 Create a transcription job

1. Open the [Amazon Transcribe console](https://console.aws.amazon.com/transcribe/) in
   `us-east-1`.
2. In the left navigation, under the transcription section, choose **Transcription jobs**,
   then **Create job**.
3. **Name:** `aif-lab03-transcribe`.
4. **Language settings:** choose **Specific language** and select the language you used in
   Polly. (**Automatic language identification** is the alternative when you do not know
   the language in advance.)
5. **Input data — S3 location:** browse to the MP3 you uploaded in Step 3.5.
6. **Output data:** choose the service-managed S3 bucket, or your own bucket if you prefer
   to keep the JSON.
7. Choose **Next**.

### 4.2 Review the configuration options

On the configure page, note these without enabling most of them:

| Option | What it does | When you would use it |
|---|---|---|
| **Speaker diarization / partitioning** | Labels which speaker said what | Meetings, interviews, contact-centre calls |
| **Custom vocabulary** | A list of domain words and their pronunciations | Drug names, part numbers, internal jargon |
| **Custom language model** | Trained on your own domain text | Heavily domain-specific speech, at scale |
| **Vocabulary filtering** | Masks or removes unwanted words | Redaction, profanity filtering |
| **PII redaction** | Detects and masks personal data in the transcript | Contact-centre recordings under privacy rules |
| **Automatic language identification** | Detects the spoken language | Multilingual inbound audio |

Turn on **PII redaction** if the option is available for your language, then choose
**Create job**.

### 4.3 Read the transcript

1. The job appears with status **In progress**, then **Complete** — usually within a
   minute for a short clip. Refresh the list.
2. Select the job name to open it and read the transcript preview.
3. Compare it word by word with the text you typed into Polly in Step 3.2.

Answer these:

- Did it recover "fourteen percent" and "ninety two points" as words, or convert them to
  digits?
- Are the sentence boundaries and punctuation right?
- Is anything wrong, and would that error matter in a real transcript?

**Word error rate (WER)** is the standard ASR metric — the proportion of words inserted,
deleted or substituted relative to the reference. You have just done a one-sample WER
evaluation by hand.

### 4.4 Inspect the JSON output

If you sent output to your own bucket, open the resulting `.json` file in S3. It contains
the full transcript plus per-word items with **start time**, **end time** and a
**confidence** score. That per-word timing is what makes captioning, search-within-audio
and call analytics possible — and it is another reminder that these services return
probabilities, not certainties.

### 4.5 Note the streaming option

Transcription jobs are **batch**: audio in S3, transcript out when finished. Transcribe
also offers **streaming transcription** over a live audio stream for real-time captions
and live agent assist. The **Real-time transcription** page in the left navigation
demonstrates this with your microphone — try it if your browser permits, then stop it. It
is the same batch-versus-real-time trade-off from Lab 01, applied to speech.

---

## Step 5 — Analyse images with Amazon Rekognition

Amazon Rekognition is managed **computer vision**. It detects objects, scenes, text, faces
and unsafe content in images and video.

### 5.1 Detect labels

1. Open the [Amazon Rekognition console](https://console.aws.amazon.com/rekognition/) in
   `us-east-1`.
2. In the left navigation, choose **Label detection** (it may sit under a demos or
   analysis grouping).
3. The page loads with a sample image. Choose **Upload** and select one of the photos you
   used in Lab 02 — or use the provided sample.
4. Read the **Results** panel.

Note three things:

- Each label carries a **confidence score**, just like Comprehend's sentiment.
- Labels are **hierarchical** — `Dog` typically comes with parent categories such as
  `Animal` and `Pet`.
- **Bounding boxes** appear for objects Rekognition can localise, so you get *where* as
  well as *what*.

Expand the **Response** or JSON view to see the raw API response. That structure —
`Labels[].Name`, `Confidence`, `Instances[].BoundingBox` — is what your application code
would parse.

### 5.2 Try the other capabilities

Work through these pages in the left navigation, using the supplied sample images. Each
takes under a minute.

| Page | What it returns | Representative use case |
|---|---|---|
| **Image moderation** | Moderation labels with confidence, in a category hierarchy | Screening user-uploaded content before publication |
| **Facial analysis** | Attributes of a detected face — pose, eyes open, apparent emotion | Photo tooling, engagement analytics |
| **Face comparison** | A similarity score between two faces | Identity verification against a reference photo |
| **Text in image** | Detected text with bounding boxes | Reading signs, plates, screenshots |
| **PPE detection** | Whether people are wearing head, face and hand cover | Worksite safety compliance |

### 5.3 Draw the boundary against other services

This is exactly the discrimination the exam tests:

- **Rekognition** finds objects, scenes, faces and unsafe content in **photos and video**.
- **Amazon Textract** extracts **structured text** from documents — forms, tables, key-value
  pairs from an invoice or a form. If the requirement mentions a *document*, a *form* or a
  *table*, the answer is Textract, not Rekognition's text detection.
- **Amazon Rekognition Custom Labels** trains on your own labelled images when the
  built-in labels do not cover your domain — a specific defect type, or your own product
  SKUs. That is where the augmented manifest from Lab 02 would be used.

### 5.4 Consider the responsible-AI dimension

Facial analysis and face comparison are the most sensitive features in this lab. Before
using them in production you would need to consider consent, applicable biometric
regulation, demonstrated accuracy across demographic groups, and a confidence threshold
with human review for consequential decisions. Domain 4 (Labs 19–22) covers this in depth
— note the concern here and carry it forward.

---

## Step 6 — Match services to use cases

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

---

## Step 7 — Clean up

Managed AI services bill **per unit processed**, so an idle account costs nothing for
Comprehend, Translate, Polly, Transcribe or Rekognition. The only standing resources you
created are in Amazon S3, plus any custom assets.

> **Cost warning:** none of the five services in this lab leaves a continuously billing
> resource behind — unlike SageMaker endpoints in Lab 04. Storage in S3 *does* bill for as
> long as objects exist, including the transcript JSON and the MP3.

### 7.1 Delete transcription job artefacts

1. Open the [Amazon Transcribe console](https://console.aws.amazon.com/transcribe/) →
   **Transcription jobs**.
2. Select `aif-lab03-transcribe` and delete it. The job record itself carries no ongoing
   charge, but deleting keeps the list clean and removes the transcript held in the
   service-managed bucket.
3. If you have any **custom vocabularies**, **vocabulary filters** or **custom language
   models** from Step 4.2, delete those too.

### 7.2 Empty and delete the S3 bucket

1. Open the [Amazon S3 console](https://console.aws.amazon.com/s3/).
2. Select your `aif-lab03-...` bucket, choose **Empty**, and confirm. This removes the MP3
   and any transcript JSON.
3. Choose **Delete** and confirm with the bucket name.

Or with the AWS CLI:

```bash
aws s3 rm s3://<your-bucket> --recursive
aws s3 rb s3://<your-bucket>
```

### 7.3 Check for other assets

Confirm you did not leave anything behind in the services you toured:

- **Amazon Comprehend** — check the custom classification and custom entity recognition
  pages. If you started an endpoint for a custom model, **delete it immediately**: a
  Comprehend endpoint provisions throughput and bills continuously until deleted. This lab
  did not ask you to create one.
- **Amazon Translate** — check for any custom terminology or parallel data resources.
- **Amazon Polly** — check for lexicons, and delete any you created.
- **Amazon Rekognition** — check that no **Custom Labels** project or model is running. A
  running Custom Labels model bills per inference hour.

### 7.4 Verify

```bash
aws s3 ls
aws transcribe list-transcription-jobs --region us-east-1
aws comprehend list-endpoints --region us-east-1
```

The bucket should be gone and the endpoint list empty.

### 7.5 Check billing

Open the **Billing and Cost Management** console and review the current month's charges by
service. Because these services bill per unit, this is a good opportunity to see how small
per-call charges actually are.

### 7.6 Keep

Save your completed table from Step 6.1 and your answers to Step 6.2. Domain 1 task
statement 1.2 is largely tested through exactly that kind of service-to-use-case matching.

---

## Verification

- [ ] Comprehend returned a MIXED sentiment for the sample review and flagged the phone number as PII
- [ ] You round-tripped the review through Amazon Translate and identified at least one point where meaning drifted
- [ ] Polly produced audible speech, and the SSML sample inserted an audible pause
- [ ] An MP3 of the Step 3.2 text exists in your lab S3 bucket
- [ ] The Transcribe job reached status **Complete** and you compared its transcript with the original text
- [ ] Rekognition returned labels with confidence scores and at least one bounding box
- [ ] You completed the ten-row matching table in Step 6.2
- [ ] The S3 bucket is deleted, the transcription job removed, and no Comprehend endpoint or Rekognition Custom Labels model is running

## Discussion questions

1. Comprehend scored the sample review as MIXED overall while targeted sentiment showed negative delivery and positive support. If you were building a review dashboard, which output would you use, and what would you lose either way?
2. A contact centre wants to transcribe every call and analyse sentiment. Sketch the service chain, and identify every point where personal data appears and what control you would apply there.
3. A team proposes training a custom SageMaker image classifier to detect whether uploaded photos contain unsafe content. Argue against it using what you saw in Step 5, then describe the one circumstance in which they would be right.

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.
