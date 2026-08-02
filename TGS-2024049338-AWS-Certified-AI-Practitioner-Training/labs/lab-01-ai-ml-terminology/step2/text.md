# Step 2 — Map the AI, ML, deep learning and generative AI hierarchy

The exam repeatedly asks you to place a described technique in the right box. The four
terms are **nested**, not parallel — each is a subset of the one before it.

### 2.1 The nesting

```
Artificial Intelligence
└── Machine Learning
    └── Deep Learning
        └── Generative AI
```

- **Artificial intelligence (AI)** — any technique that lets a machine perform tasks that
  normally need human intelligence. This includes hand-written rule engines and search
  algorithms that do no learning at all.
- **Machine learning (ML)** — a subset of AI in which the system learns patterns from data
  instead of being explicitly programmed with rules.
- **Deep learning (DL)** — a subset of ML that uses neural networks with many hidden
  layers. It excels where features are hard to hand-engineer: images, audio, raw text.
- **Generative AI** — a subset of deep learning whose models *produce new content*
  (text, image, audio, code) rather than only producing a label or a number.

### 2.2 Classify these workloads

Write **AI only**, **ML**, **DL** or **GenAI** against each row. Choose the *narrowest*
box that fits.

| # | Workload | Your answer |
|---|---|---|
| 1 | A tax form validator built from 400 hand-written `if` rules | |
| 2 | A linear regression that predicts house price from floor area | |
| 3 | A convolutional network that flags manufacturing defects in photos | |
| 4 | A model that writes a product description from five bullet points | |
| 5 | A decision tree that scores loan applications from tabular data | |
| 6 | A model that produces a photo-realistic image from a text prompt | |

**Answer key:** 1 = AI only (no learning from data) · 2 = ML · 3 = DL · 4 = GenAI ·
5 = ML · 6 = GenAI.

### 2.3 Check the boundary cases

Two distinctions catch people out on the exam:

- **Rule engines are AI but not ML.** If a human wrote the rules, nothing was learned.
- **All generative AI is deep learning, but most deep learning is not generative.** An
  image classifier is deep learning; it outputs a label, not new content.
