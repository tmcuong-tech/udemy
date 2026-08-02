# Well done!

You have completed Lab 16 — Vector Stores and Retrieval Quality:

✅ Set up and measure a baseline
✅ Chunk size and overlap
✅ Top-K
✅ Metadata filtering
✅ Diagnose a bad answer
✅ Clean up

**Key takeaways:**

- **If the correct chunk was never retrieved, no prompt can produce a correct answer.** Always inspect retrieval alone before touching generation — it is the fork that decides which half of the system you work on.
- **Chunks too small** lose context and sever facts at boundaries. **Chunks too large** produce a blurred vector that matches nothing strongly and waste input tokens. **Overlap** stops a fact being cut in half.
- **Hierarchical chunking** resolves the trade-off rather than compromising: match on small precise children, return the larger parent for context.
- **Chunking is fixed at ingestion** and cannot be changed on an existing data source. Top-K is per query and free to experiment with.
- Raising **top-K** raises **recall** and lowers **precision**. The asymmetry matters: an unretrieved fact is unrecoverable, while a retrieved-but-noisy one is merely more expensive — so bias toward recall, then trim.
- **Re-ranking** buys precision after generous recall. **Hybrid search** covers exact identifiers that pure vector similarity handles badly.
- **Metadata filtering is applied before ranking**, so an excluded chunk is not a low-scoring result — it does not exist for that query.
- **Access control in RAG belongs at retrieval, not in the prompt.** Derive the filter from the authenticated session, never from user input. The model cannot leak what it was never given.
- Tune in cost order: data coverage → source documents → metadata and filters → top-K → hybrid or re-ranking → chunking → prompt. Most teams work this list backwards.
- **How documents are written is part of RAG engineering.** Facts stated explicitly retrieve well; facts implied by omission retrieve badly.
- The **vector store bills hourly and survives deletion of the knowledge base**. Always verify with `list-collections`, in every Region you used.

**Next:** Lab 17 — Fine-Tuning and Model Customisation
