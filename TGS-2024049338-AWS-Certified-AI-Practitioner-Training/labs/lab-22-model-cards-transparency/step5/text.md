# Step 5 — AWS AI Service Cards and the transparency you inherit

A model card documents a model **you** built. But most AI in most organisations is consumed
as a managed service — you did not train it, cannot inspect it, and have no access to its
training data. The transparency question does not disappear; it moves.

### 5.1 What an AI Service Card is

**AWS AI Service Cards** are AWS's published transparency documents for its own AI services.
They are the managed-service equivalent of a model card: AWS documents the service so that
you can make an informed decision about using it.

An AI Service Card typically covers:

- The **intended use cases** for the service, and uses AWS considers out of scope
- **Design choices** and how the service was built and tested
- **Performance considerations** and factors that affect accuracy
- **Best practices** for deploying the service responsibly, including where human review is
  recommended
- **Limitations** and known factors that degrade performance

You can find the published AI Service Cards through the responsible AI pages on
[aws.amazon.com](https://aws.amazon.com/). Do not assume every service has one — check which
services are covered rather than asserting it.

### 5.2 Why this matters to you as a consumer of the service

When you build on a managed AI service, you inherit its properties and remain accountable
for the outcome. The service card is your primary evidence about a component you cannot
inspect.

| You cannot | So the service card is how you |
|---|---|
| Inspect the training data | Learn what population it was built for |
| Run your own bias analysis on the model internals | Learn what testing AWS performed and what it found |
| Change the model | Learn what AWS recommends as a mitigating control |
| Explain a specific decision from the weights | Learn the accuracy factors that plausibly affected it |

> **The accountability does not transfer.** If you deploy a managed service in a decision
> that affects people, *you* are accountable for that decision — not AWS. The service card
> tells you what AWS knows; deciding whether that is sufficient for your use case is your
> responsibility, and documenting that decision is your governance obligation.

### 5.3 The composition problem

Your model card must document the **system**, not just any model you personally trained.

If your application is a managed AI service plus a foundation model plus a guardrail plus
some business logic, then:

- The managed service's limitations are your limitations
- The foundation model's caveats are your caveats
- Your guardrail (Lab 19) is a documented control that belongs in the card
- The **combination** may have failure modes none of the parts do individually

Record in your card **which components you built and which you consumed**, and cite the AI
Service Card or model provider documentation for each consumed component. A card that
documents only the thin layer you wrote is technically accurate and practically misleading.

### 5.4 Complete the exercise

Write a short additional section for `aif-lab22-loan-approval-card`:

1. **Component inventory.** Suppose the loan system also uses a managed document-analysis
   service to extract fields from uploaded payslips. List the components, and for each state
   whether you built or consumed it.
2. **Inherited limitations.** For the consumed extraction component, what would you need
   from its service card before you would rely on it in a High risk decision? Name three
   specific things.
3. **Composition failure.** Describe one failure mode that arises only from the combination
   — for example, extraction accuracy varying by document quality, feeding a model that has
   no way to know a field was uncertain. What control would you add?
4. **The honest sentence.** Write one sentence for the card stating what you do *not* know
   about the components you consumed. This sentence is the difference between a transparency
   document and a marketing document.
