# Step 5 — Analyse images with Amazon Rekognition

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
