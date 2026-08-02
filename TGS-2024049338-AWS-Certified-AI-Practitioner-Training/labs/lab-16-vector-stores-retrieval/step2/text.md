# Step 2 — Chunk size and overlap

Chunking is the highest-leverage decision in a RAG system and the one most often left at its default. A bad chunking strategy produces bad answers that look like model failures.

### The trade-off

Every chunk is embedded into a **single vector**. That vector must represent everything in the chunk. This creates a direct tension:

**Chunks too small:**
- A vector represents one narrow idea — precise matching.
- But **context is lost**. A chunk reading "This requires 24 hours notice" is nearly useless: which service? Retrieved alone, the model cannot use it.
- Facts get **split across boundaries**. "Claims above 500 Singapore dollars require review by an operations manager" landing in one chunk and "and photographic evidence" in the next means neither chunk answers the question completely.
- More chunks means more vectors, a larger index, and more retrieval calls to cover the same material.

**Chunks too large:**
- Each chunk is self-contained and readable.
- But the vector is a **blurred average** of several topics. A chunk covering claims deadlines, monetary thresholds and temperature excursions has a vector that is not strongly close to any of those queries. Retrieval precision drops.
- You pay input tokens for the **entire** chunk on every retrieval, most of it irrelevant.
- Fewer, larger chunks fill the context window faster, so effective top-K falls.

### Overlap

**Overlap** repeats a slice of text between adjacent chunks. Its single job is to stop a fact being severed at a boundary — with overlap, a sentence spanning the split appears complete in at least one chunk.

Overlap costs storage and duplicates text across retrieved results. A common starting point is a modest overlap, on the order of ten to twenty percent of chunk size. **Treat that as a starting point to be tested, not a rule.** The right number depends on how your documents are written.

### Chunking strategies

Bedrock knowledge bases offer several. Check the console for what is available in your Region:

| Strategy | How it splits | Best for |
|---|---|---|
| **Fixed-size** | A configured number of tokens, with configured overlap | General text; predictable and easy to reason about |
| **No chunking** | One chunk per document | Documents already short and single-topic |
| **Hierarchical** | Parent and child chunks — retrieve on small children, return larger parents | Getting precision *and* context together |
| **Semantic** | Splits at points where meaning shifts rather than at a fixed length | Documents with uneven section lengths |

**Hierarchical chunking is worth understanding well**, because it directly resolves the trade-off above rather than compromising on it: you match against small, precise chunks but hand the model the larger parent that surrounds the match.

### Run the experiment

Chunking configuration **cannot be changed on an existing data source**. To test a different strategy you must create a new data source or a new knowledge base and re-sync.

**If your budget and time allow**, create a second data source over the same S3 bucket with a **noticeably smaller** fixed chunk size and **zero overlap**, sync it, and re-run the five test questions from Step 1.

**If not, reason it through** — this is the exam-relevant part and requires no provisioning. Take `claims-policy.txt` and mark by hand where a small, zero-overlap chunker would split it. Then answer:

1. Does any single chunk still contain the complete answer to **Q2** (maximum liability)?
2. **Q5** needs the Gold shipment threshold *and* what Gold includes. In `service-tiers.txt` those sit in different paragraphs. With small chunks, would one retrieved chunk carry both? What does that imply for top-K?
3. Which chunk boundary would **overlap** have rescued, and which would it not?

### What you should conclude

- **Retrieval failures caused by chunking are invisible in the generated answer.** The model gives a confident partial answer from an incomplete chunk. Nothing signals that the other half of the fact existed and was not retrieved.
- **The right chunk size depends on your documents**, not on a universal best practice. Dense reference material with one fact per line wants different chunking from flowing narrative prose.
- **Chunking is set at ingestion.** Changing it means re-ingesting everything, which is why it is worth testing on a small corpus before committing to a large one.

**Checkpoint:** You can explain both failure modes with a concrete example from these documents, describe what overlap fixes, and say why hierarchical chunking resolves the trade-off rather than compromising on it.
