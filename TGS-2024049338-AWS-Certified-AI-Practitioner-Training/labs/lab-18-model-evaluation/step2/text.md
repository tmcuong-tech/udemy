# Step 2 — The automatic metrics

You must be able to name each metric, say what task it belongs to, and state its limitation. That triple is what gets tested.

### ROUGE — summarisation

**Recall-Oriented Understudy for Gisting Evaluation.** Measures how much of the **reference** appears in the generated output. It is **recall-oriented**: the question is "how much of what should have been said was said?"

Variants you should recognise:

- **ROUGE-N** — overlap of n-grams. ROUGE-1 is single words, ROUGE-2 is word pairs. ROUGE-2 is stricter because it requires correct ordering.
- **ROUGE-L** — longest common subsequence. Rewards matching sequence without requiring contiguity, so it tolerates inserted words.

**Use for:** summarisation. Recall orientation fits — a summary that omits the key point has failed, and ROUGE penalises that.

**Limitation:** it measures **word overlap, not meaning**. A summary that is perfectly accurate but uses synonyms throughout scores badly. A summary that copies large chunks of the source verbatim scores well while being a poor summary.

### BLEU — translation

**Bilingual Evaluation Understudy.** Measures how much of the **generated output** appears in the reference — **precision-oriented**, the mirror of ROUGE. Includes a brevity penalty so a model cannot score well by emitting one confidently-correct word.

**Use for:** machine translation. Precision orientation fits — in translation, adding content that was not in the source is an error, and BLEU penalises that.

**Limitation:** same as ROUGE. It is n-gram overlap, so a valid alternative translation using different vocabulary is penalised.

> **The ROUGE and BLEU pairing is heavily examined.** ROUGE for summarisation, recall-oriented, "did we capture the reference". BLEU for translation, precision-oriented, "is what we produced in the reference". If you remember only one thing about metrics, remember this.

### BERTScore — semantic similarity

Uses **embeddings** rather than exact word matching. It embeds the tokens of both texts and compares them in vector space, so semantically equivalent wording scores highly even with no shared words.

**Use for:** any generation task where paraphrase is acceptable — which is most of them.

**Advantage over ROUGE and BLEU:** it captures meaning. "The parcel arrives in two days" and "delivery takes 48 hours" score near zero on n-gram overlap and high on BERTScore.

**Limitation:** it depends on the embedding model, so scores are comparable within a configuration and not across different ones. It is also slower and costlier than counting n-grams, and it can score a fluent, semantically similar but factually **wrong** statement highly. Similarity is not correctness.

### Perplexity — fluency

Measures how "surprised" a model is by a piece of text. **Lower is better.** It is a property of the model's confidence, not a comparison against a reference.

**Use for:** assessing language modelling quality, comparing base models, monitoring training. It is not a task quality metric — a model can produce fluent, low-perplexity text that is completely wrong.

### F1, precision, recall — classification

When the task **does** have one right answer — classification, extraction, question answering with short exact answers — use the classification metrics. They are stronger than any overlap metric because they measure correctness rather than similarity.

**Practical implication:** if you can reframe a generative task as classification or extraction, do it. Evaluation becomes dramatically easier and more meaningful. This is a genuinely useful design insight, not just an exam point.

### Summary table

| Metric | Task | Orientation | Measures | Main limitation |
|---|---|---|---|---|
| **ROUGE** | Summarisation | Recall | N-gram / LCS overlap with reference | Word overlap, not meaning |
| **BLEU** | Translation | Precision | N-gram overlap, with brevity penalty | Penalises valid paraphrase |
| **BERTScore** | General generation | Semantic | Embedding similarity | Similarity is not correctness |
| **Perplexity** | Language modelling | — | Model's surprise at the text | Fluency, not accuracy |
| **F1 / precision / recall** | Classification, extraction | Both | Correctness against a label | Needs one right answer |

### The limitation that applies to all of them

**None of these metrics detects a hallucination.** A summary that invents a plausible fact, phrased in wording similar to the reference, can score well on ROUGE and BERTScore alike. Automatic metrics measure **similarity to a reference**, and similarity is not truth.

This is the reason human evaluation and grounding checks exist, and it is why a mature evaluation strategy never relies on automatic metrics alone. It is also a frequently-tested point.

**Checkpoint:** You can state for each metric its task, its orientation and its limitation, and you can explain why no automatic metric detects hallucination.
