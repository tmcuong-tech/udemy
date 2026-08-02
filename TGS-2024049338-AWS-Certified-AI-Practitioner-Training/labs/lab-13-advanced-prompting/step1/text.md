# Step 1 — Set up and define the scenario

Lab 12 covered the four parts of a prompt and the zero-shot to few-shot ladder. This lab adds the techniques you reach for when a well-structured few-shot prompt still is not good enough, and ends by packaging the result as a **reusable template**.

### Open the playground

1. Sign in to the AWS Management Console and open the Amazon Bedrock console at <https://console.aws.amazon.com/bedrock/>.
2. Choose a Region where Bedrock is offered — for example **US East (N. Virginia) us-east-1**.
3. In the left navigation, open the **Chat** playground and choose **Select model**. Pick a text model you have access to and keep it for the whole lab.
4. Open the inference configuration panel. Set **temperature** low (near 0) so that differences you see come from your prompt, not from sampling.

If the playground offers a separate **system prompt** field, note where it is — you will need it in Step 2. If it does not, you will place the system content at the top of the message instead; both are covered.

### The scenario

You are building an internal tool for a fictional company, **Northwind Logistics**. The tool reads a customer's delivery complaint and produces a structured triage record for the operations team.

For every complaint the tool must output:

- a **severity** — `LOW`, `MEDIUM`, `HIGH`
- a **category** — `DELAY`, `DAMAGE`, `WRONG_ITEM`, `BILLING`, `OTHER`
- whether a **refund** is likely warranted — `YES`, `NO`, `NEEDS_REVIEW`
- a **one-sentence summary** for the operations queue

The house rules — these are business rules the model cannot possibly guess:

- A complaint mentioning **perishable or temperature-sensitive goods** is at least `HIGH` severity.
- A complaint from a customer who says they have **contacted us before about the same issue** is escalated one severity level.
- Refund is `NEEDS_REVIEW`, never `YES`, whenever the stated value is **above 500 dollars**.
- **Never** state a refund amount, promise a delivery date, or apologise on the company's behalf. That is a human's job.

### Test complaints

```
A. My order of frozen seafood arrived at room temperature. This is the
   second time I have written to you about this. Order value 180 dollars.

B. The box was dented but the contents seem fine. Nothing urgent.

C. I ordered a laptop stand and received a keyboard. Value 620 dollars.

D. Where is my parcel? It was due Tuesday. I am furious and I want
   compensation immediately.
```

Complaint A triggers two house rules at once. Complaint C crosses the 500-dollar threshold. Complaint D is emotionally charged and will tempt the model into apologising and promising things.

**Checkpoint:** Model selected, temperature low, and you have the four test complaints and the house rules to hand.
