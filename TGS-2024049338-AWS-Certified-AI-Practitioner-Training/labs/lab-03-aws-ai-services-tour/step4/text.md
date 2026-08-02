# Step 4 — Convert speech to text with Amazon Transcribe

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
