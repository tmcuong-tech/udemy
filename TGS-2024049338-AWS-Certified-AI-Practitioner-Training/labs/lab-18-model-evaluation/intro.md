# Lab 18 — Evaluating Foundation Model Performance

Run an Amazon Bedrock automatic model evaluation job against your own dataset, interpret the results critically, and place ROUGE, BLEU, BERTScore, benchmarks, human review and business metrics in a complete evaluation strategy.

> **Cost note.** An evaluation job runs inference on every prompt against every model selected, so cost scales with records multiplied by models. Keep to eight or ten records and at most two models. A job runs, finishes, and stops charging — it is not a continuously-billing resource.

**What you will do:**
- Build a JSONL evaluation dataset with consistent reference answers
- Learn what ROUGE, BLEU, BERTScore, perplexity and F1 each measure, and where each breaks down
- Run an automatic model evaluation job in Amazon Bedrock against your own data
- Interpret the report per record and find a score that misrepresents the output
- Configure human evaluation, and place benchmarks and business metrics in a full strategy
