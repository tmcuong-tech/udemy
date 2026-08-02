# Step 2 — Request access to foundation models

Having a Bedrock console does not mean you can call every model in it. Access is granted **per AWS account, per Region, per model**. Some models are available as soon as you ask; some providers require you to submit use case details first.

1. In the **left navigation**, find the configuration or settings area and choose **Model access**.
2. Read the page before clicking anything. It lists the foundation models offered in *this* Region and shows a status for each one — typically indicating whether access is already available, has been granted, or must still be requested.

   > This page — not your memory, not this handout, not a blog post — is the source of truth for which models you can use. Check the **Model access** page for the models available in your Region.

3. Choose the button that lets you **modify** or **manage** model access. Depending on the console version the label may read *Enable specific models*, *Modify model access*, or similar.
4. Select at least **two models from two different providers**. For example, one Amazon Titan text model and one Anthropic Claude model, or a Meta Llama model. Choosing two *different providers* matters, because Lab 07 asks you to compare them.
5. Also select one **embeddings** model if the Region offers one — Lab 08 needs it. Embedding models are usually listed with the others but produce vectors, not text.
6. If a provider asks for **use case details**, complete the short form honestly. Describe the use case as internal training and evaluation of foundation models.
7. Review your selections and **submit** the request.
8. Return to the **Model access** page and refresh until your chosen models show as granted. Some are granted almost immediately; others take longer. If one is still pending after a few minutes, carry on with any model that *has* been granted.

**Why this exists (exam relevance):** model access is an explicit, auditable opt-in. It is the account owner deciding which third-party models their organisation is permitted to send data to. Enabling access by itself does **not** generate charges — only invocations do.

**Checkpoint:** At least two models, from two different providers, show access granted in your chosen Region.
