# Step 3 — Explore the model catalogue

Bedrock's value proposition is **choice through one API**. The catalogue is where you see that choice.

1. In the **left navigation**, open the model catalogue area. Labels vary by console version — look for *Model catalog*, *Foundation models*, or *Base models*.
2. Browse the list. Notice that models are grouped or filterable by **provider** and by **modality**.
3. Pick **three** different models and record the following for each:

| # | Model name | Provider | Modality (text / image / embeddings / multimodal) | Stated use cases (from the console) |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

4. Open the **detail page** for one model. Observe two things:
   - The model is identified by a **model ID** — a string your code passes to the API.
   - Providers publish **multiple versions** of a model over time, and the version is part of that ID.

> **Do not memorise version strings for the exam.** Model IDs change as providers ship new versions. What the exam expects you to know is that models are *selected by ID*, that IDs are *versioned*, and that availability is *per Region*.

**Providers and modalities — the mental model**

- **Provider** answers "who built and trained this model". Bedrock's role is to host several providers behind one consistent interface so you are not locked into one vendor.
- **Modality** answers "what goes in and what comes out". A text model takes text and returns text. An image model returns an image. An **embeddings** model returns a list of numbers (a vector) — you will use one of these in Lab 08. A **multimodal** model accepts more than one input type, such as text plus an image.

**Checkpoint:** You have recorded provider, modality and stated use case for three models, and you can point to where a model ID is displayed.
