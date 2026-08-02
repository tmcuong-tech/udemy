# Step 3 — Synthesise speech with Amazon Polly

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
