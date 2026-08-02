# Step 1 — The customisation decision

## ⚠️ How this lab works — read first

**You will configure a fine-tuning job but you will NOT submit it, and you will NOT purchase provisioned throughput.**

This is deliberate, and it is not a shortcut. In Amazon Bedrock, a **custom model cannot be invoked on demand** — running inference against one requires **provisioned throughput**, which is purchased in model units for a committed term. It is **substantially more expensive than anything else in this course**, it commits you for the duration, and there is no meaningful free tier for it.

A single learner who provisions throughput in class can incur a bill far larger than every other lab in this course combined.

**So: walk through the configuration screens, fill them in, understand every field — and stop at the final button. Do not submit the training job. Do not purchase provisioned throughput.** This is stated again at each point where it matters.

Everything examinable about Task 3.3 is in the configuration, the data preparation and the trade-off analysis. None of it requires you to actually run a job.

---

## The four customisation options

Ordered by cost and effort. The exam tests whether you can pick the **cheapest option that actually solves the stated problem** — a question type that appears repeatedly.

### 1. Prompt engineering

Change the text you send. No training, no infrastructure, effect is immediate.

- **Changes weights:** no
- **Needs data:** no, or a handful of examples
- **Time to first result:** minutes
- **Cost:** tokens only; few-shot examples are paid for on every call
- **Fixes:** output format, tone, task framing, edge case handling

### 2. RAG

Retrieve relevant documents at query time and insert them into the prompt.

- **Changes weights:** no
- **Needs data:** a document corpus, no labelling
- **Time to first result:** hours
- **Cost:** vector store hourly, plus embedding and retrieval tokens per query
- **Fixes:** the model does not know your facts, your facts change often, you need citations

### 3. Fine-tuning

Continue training a pre-trained model on **labelled examples of your task** — prompt and completion pairs. This is **supervised** learning.

- **Changes weights:** yes
- **Needs data:** typically hundreds to thousands of labelled examples, curated
- **Time to first result:** days to weeks including data preparation
- **Cost:** training compute, plus **provisioned throughput to serve it**
- **Fixes:** consistent house style at scale, a specialised task shape, domain vocabulary, shorter prompts for high-volume workloads

### 4. Continued pre-training

Continue the original **unsupervised** pre-training objective on a large corpus of your **unlabelled** domain text.

- **Changes weights:** yes
- **Needs data:** large volumes of unlabelled domain text — a corpus, not a labelled set
- **Time to first result:** weeks
- **Cost:** the highest of the four, plus provisioned throughput
- **Fixes:** the model does not understand your **domain language** at all — highly specialised medical, legal or scientific vocabulary

### The distinction that gets tested

**Fine-tuning is supervised and uses labelled prompt–completion pairs. Continued pre-training is unsupervised and uses unlabelled raw text.** If a question mentions labelled examples of a task, it is fine-tuning. If it mentions a large body of domain documents with no labels, it is continued pre-training.

### The comparison table

| | Prompt engineering | RAG | Fine-tuning | Continued pre-training |
|---|---|---|---|---|
| Weights changed | No | No | Yes | Yes |
| Data needed | None to a few examples | Document corpus | Hundreds to thousands of labelled pairs | Large unlabelled corpus |
| Labelling required | No | No | **Yes** | **No** |
| Learning type | — | — | Supervised | Unsupervised |
| Time | Minutes | Hours | Days to weeks | Weeks |
| Adds new facts | No | **Yes** | Poorly | Somewhat |
| Update a fact | — | Re-sync, seconds | Retrain | Retrain |
| Citations | No | **Yes** | No | No |
| Serving cost | On demand | On demand | **Provisioned throughput** | **Provisioned throughput** |

### The heuristic

**RAG changes what the model knows. Fine-tuning changes how the model behaves.**

If the complaint is *"it does not know our data"* → **RAG**.
If the complaint is *"it does not sound like us"* or *"it will not stick to our format"* → **prompt engineering first, fine-tuning only if that genuinely fails**.
If the complaint is *"it does not understand our field's language at all"* → **continued pre-training**, and this is rare.

**And they combine.** A production system commonly fine-tunes for behaviour and uses RAG for facts. These are not competing choices.

**Checkpoint:** You can state the supervised versus unsupervised distinction between fine-tuning and continued pre-training, and you understand that you will not submit a job or provision throughput in this lab.
