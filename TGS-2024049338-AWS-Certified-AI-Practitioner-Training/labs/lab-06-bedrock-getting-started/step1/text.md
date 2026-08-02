# Step 1 — Open Amazon Bedrock and choose a Region

Amazon Bedrock is a **fully managed service** that gives you a single API to foundation models (FMs) from several providers. There are no servers, clusters or endpoints for you to create — you call a model and you are billed for the tokens you process.

The first thing to understand is that **Bedrock is Region-specific**. The service itself is not offered in every AWS Region, and within a supported Region, the *set of models* offered differs. A model you have seen in a demo may simply not exist in the Region you are sitting in.

1. Sign in to the AWS Management Console.
2. Open the Amazon Bedrock console at <https://console.aws.amazon.com/bedrock/>.
3. Use the **Region selector** at the top right of the console to choose a Region in which Bedrock is offered. This lab assumes **US East (N. Virginia) `us-east-1`**.
4. Write down the Region you chose. Everything you do for the rest of this lab — model access, playground history, model IDs — belongs to that Region and nothing carries over to another one.
5. If a welcome or overview screen appears, choose the option to get started so that the full left navigation is displayed.

> **Console layouts drift.** AWS changes the Bedrock console regularly. Throughout this lab, follow the **named item** in the left navigation rather than a fixed screen position. If a label has been renamed, look for the item that does the job being described.

**Checkpoint:** The Bedrock console is open and you can state, out loud, which Region you are working in.
