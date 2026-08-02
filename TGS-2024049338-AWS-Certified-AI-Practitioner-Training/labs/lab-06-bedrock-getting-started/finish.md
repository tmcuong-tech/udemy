# Well done!

You have completed Lab 06 — Amazon Bedrock Getting Started:

✅ Open Amazon Bedrock and choose a Region
✅ Request access to foundation models
✅ Explore the model catalogue
✅ Run your first prompt in the playground
✅ See the same catalogue from the AWS CLI
✅ Clean up

**Key takeaways:**

- Amazon Bedrock is a fully managed service offering foundation models from multiple providers through a single API — there are no servers, clusters or endpoints for you to create.
- Model availability is specific to an **account, Region and model**. The **Model access** page in your Region is the source of truth, not a blog post or a remembered demo.
- Model access is an explicit opt-in that some providers gate behind use case details. Enabling access costs nothing; **invocations** are billed on tokens processed, input and output.
- A model is selected by a versioned **model ID**, and has a **provider** and **input/output modalities** (text, image, embeddings, multimodal).
- `aws bedrock` is the control plane (list and manage models); `aws bedrock-runtime` is the data plane (invoke a model).
- On-demand inference is serverless, but **Provisioned Throughput, custom models and Knowledge Bases bill continuously** and must be deleted.

**Next:** Lab 07 — Comparing Foundation Models and Inference Parameters
