# Step 2 — Translate text with Amazon Translate

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
