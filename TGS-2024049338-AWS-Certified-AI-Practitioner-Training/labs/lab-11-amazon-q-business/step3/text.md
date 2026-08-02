# Step 3 — Create the Amazon Q Business application

> **This is the step that starts the meter.** Re-read the cost warning in Step 1 before continuing. If you decided not to incur the charge, read this step and Steps 4 to 6 for the concepts and go straight to Step 7.

1. Open the Amazon Q Business console at <https://console.aws.amazon.com/amazonq/> and confirm your Region in the selector. Q Business is not offered in every Region — if the console tells you the service is unavailable here, switch to a Region where it is offered.
2. Choose the option to **create an application**.
3. Give the application a name you will recognise later, such as `northwind-lab`.
4. Work through the creation flow. The console will ask you for the following, and the exact wording and ordering change between console versions — follow the **named** item rather than a fixed sequence:

   - **A service role.** Let the console **create a new service role** for you. Q Business needs permission to read from your data sources and write to its index. Note the role name — you may want to remove it in Step 7.

   - **User access and identity.** Q Business identifies users so it can apply document permissions. Depending on the console version this is configured through **AWS IAM Identity Center** or an equivalent identity provider setup. If you have no Identity Center instance, the console will offer to create one.

     > **This is the architecturally important part of the whole lab.** Q Business is user-aware by design. It filters retrieval by what *that user* is permitted to read, so two employees asking the same question can correctly receive different answers. A hand-built RAG system gets this wrong by default — the index does not know who is asking, and every user sees every document. Permission-aware retrieval is the main reason organisations buy this rather than build it.

   - **Index capacity or application tier.** This is the sizing choice that drives cost. Choose the **smallest option offered** — three text files need nothing more. Check the Amazon Q Business pricing page for what each option costs before selecting.

   - **Encryption.** The default AWS-managed key is fine for this lab.

5. Create the application and wait for it to reach an active state. This takes a few minutes.
6. **Write down the application name and its ID.** You need both for Step 7, and Step 7 is the step that stops the charge.

```bash
# Record your application ID now
aws qbusiness list-applications --region "$REGION"
```

**Checkpoint:** The application shows as active, and you have written down its ID.
