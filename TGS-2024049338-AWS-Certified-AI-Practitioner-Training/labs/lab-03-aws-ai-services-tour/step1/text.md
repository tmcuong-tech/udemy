# Step 1 — Extract meaning from text with Amazon Comprehend

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
