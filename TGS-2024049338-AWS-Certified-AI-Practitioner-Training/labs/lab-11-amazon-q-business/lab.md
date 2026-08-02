# Lab 11 — Amazon Q Business Getting Started

Create an Amazon Q Business application, connect it to documents in Amazon S3, and ask questions answered from those documents with citations.

**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — region `us-east-1` unless stated otherwise.

**Exam domain:** Domain 2 — Fundamentals of Generative AI (24%)
**Task statement:** 2.3 Describe AWS infrastructure and technologies for building generative AI applications
**WSQ mapping:** LU1 · Topic 2 Amazon Q Business Getting Started · K2 · A1 · LO1
**Slide reference:** v11 deck slides 173–182
**Estimated time:** 40 minutes

**Learning objectives:**
- Explain what Amazon Q Business is and how it differs from Amazon Bedrock
- Create a Q Business application and connect an Amazon S3 data source
- Run a sync and interpret the sync history
- Ask questions answered from your own documents, and verify the citations
- Test the boundaries of grounding — out-of-scope questions, false premises, stale documents, per-user permissions
- Explain why permission-aware retrieval is the main reason to buy rather than build an enterprise assistant
- Delete the application and confirm from the API that billing has stopped

**Prerequisites:**
- Labs 06 to 10 completed
- AWS CLI configured, with permissions for Amazon S3 and Amazon Q Business
- Amazon Q Business available in your chosen Region — check the console

> ## Cost warning — read before starting
>
> **Amazon Q Business is not free tier and bills continuously for as long as the application exists**, on a per-user subscription and index capacity basis — not per question asked. Closing the browser does **not** stop the charge; only deleting the application does.
>
> Check the current Amazon Q Business pricing page and accept the charge before you begin, **complete this lab in one sitting**, and delete the application in Step 7 the same day. If you would rather not incur the cost, read Steps 2 to 6 for the concepts — the exam tests what Q Business is and when to use it, not your ability to click through the wizard.

Console entry point: <https://console.aws.amazon.com/amazonq/>

---

## Step 1 — What Amazon Q Business is, and what it will cost you

Amazon Q Business is a **managed generative AI assistant for enterprise data**. You point it at your organisation's content, it indexes that content, and employees ask questions in natural language and get answers **with citations back to the source documents**.

Everything you built by hand in Lab 08 and argued for in Lab 09 — retrieval, grounding, citations — Q Business provides as a managed service. You supply documents and permissions; you do not supply prompts, an embedding model, a vector store or any code.

## Where it sits in Lab 10's framework

| Layer | Example |
|---|---|
| Managed AI service | Comprehend, Rekognition |
| **Managed generative AI application** | **Amazon Q Business** |
| Foundation model API | Amazon Bedrock |
| Build and host it yourself | SageMaker |

Q Business sits **above** Bedrock. Where Bedrock gives you a model and you build the RAG pipeline, Q Business gives you the finished application. You trade control for speed: you cannot choose the model or write the prompt, but you get a working, permission-aware, cited assistant in an afternoon.

## Cost warning — read this before Step 3

> ### Amazon Q Business is not free tier, and it bills continuously.
>
> - A Q Business application is charged on a **per-user subscription** basis, and index capacity is charged for **as long as the application exists** — not per question asked.
> - **Closing the browser does not stop the charge. Only deleting the application does.**
> - This is fundamentally unlike the Bedrock labs, where on-demand inference cost nothing when idle.
>
> **Before you begin, decide which applies to you:**
>
> 1. **You are in a managed classroom account** — your trainer will confirm whether you should create an application or follow along on a shared one.
> 2. **You are using your own account** — check the current Amazon Q Business pricing page and confirm you accept the charge. Then complete the lab **in one sitting** and delete the application in Step 7 the same day.
> 3. **You do not want to incur the cost** — read Steps 2 to 6 for the concepts and skip the creation. The exam tests what Q Business *is* and *when to use it*, not your ability to click through the wizard.
>
> Do not create the application and come back to it tomorrow. That is the decision that produces a bill.

## What Q Business does that a raw model cannot

- **Connects to enterprise data sources** through built-in connectors, rather than you writing ingestion code
- **Respects existing permissions** — a user should only get answers from documents they are already allowed to read. This is the hardest part of enterprise RAG and the main reason to buy rather than build.
- **Cites its sources**, so an answer can be checked (Lab 09's mitigation, built in)
- **Provides a ready-made web experience** with user authentication
- **Declines when the answer is not in the documents** — the grounding behaviour you had to prompt for by hand in Lab 09

**Checkpoint:** You can explain how Q Business differs from Bedrock, and you have made an explicit decision about whether to incur the cost.

---

## Step 2 — Prepare documents in Amazon S3

Q Business needs something to be grounded in. You will create a small set of fictional company documents — deliberately containing facts that **no foundation model could possibly know**, so that when you get a correct answer in Step 5 you know for certain it came from retrieval and not from training data.

## Create a bucket

```bash
REGION=us-east-1
BUCKET=q-business-lab-$(date +%s)

aws s3 mb "s3://$BUCKET" --region "$REGION"
echo "Bucket: $BUCKET"
```

Write the bucket name down. You will need it in Step 4 and again in Step 7.

## Create the documents

```bash
mkdir -p qdocs

cat > qdocs/leave-policy.txt <<'EOF'
NORTHWIND LOGISTICS PTE LTD - ANNUAL LEAVE POLICY (2026)

Full-time employees are entitled to 21 days of paid annual leave per
calendar year. Employees who have completed five years of continuous
service are entitled to 26 days.

Leave requests must be submitted through the Meridian portal at least
14 calendar days before the intended start date. Requests of more than
10 consecutive working days require approval from a department head.

A maximum of 7 unused days may be carried forward into the following
year. Carried-forward days expire on 31 March. Unused days beyond the
carry-forward limit are forfeited and are not paid out.

The leave year runs from 1 January to 31 December.
EOF

cat > qdocs/expense-policy.txt <<'EOF'
NORTHWIND LOGISTICS PTE LTD - EXPENSE REIMBURSEMENT POLICY (2026)

Claims must be submitted within 30 days of the expense being incurred.
Claims submitted after 60 days will not be reimbursed.

Meal allowance while travelling domestically is SGD 45 per day.
International travel meal allowance is SGD 80 per day.

Air travel in economy class is approved by default. Business class
requires prior written approval from a director and is permitted only
for flights exceeding 7 hours.

Taxi and ride-hailing fares are reimbursable. Private vehicle mileage
is reimbursed at SGD 0.62 per kilometre.

All claims over SGD 500 require an itemised receipt.
EOF

cat > qdocs/it-support.txt <<'EOF'
NORTHWIND LOGISTICS PTE LTD - IT SUPPORT GUIDE (2026)

The service desk operates Monday to Friday, 08:30 to 18:30 Singapore
time. Outside these hours, only Priority 1 incidents are handled, via
the on-call number listed in the Meridian portal.

Password resets are self-service through the Meridian portal. Accounts
lock after five failed attempts and unlock automatically after 30
minutes.

Laptop replacement is on a four-year cycle. Requests for early
replacement require a documented hardware fault.

Software installation requires a ticket. Employees do not have local
administrator rights.
EOF
```

Notice what these contain: **21 days of leave, SGD 45 meal allowance, a four-year laptop cycle, five failed login attempts.** These numbers exist nowhere in any model's training data. They are the perfect test of grounding.

## Upload

```bash
aws s3 cp qdocs/ "s3://$BUCKET/docs/" --recursive
aws s3 ls "s3://$BUCKET/docs/"
```

You should see three objects.

> **S3 storage costs are negligible** for three small text files — a few cents a month at most. It is the Q Business application in Step 3, not this bucket, that carries the real cost. You will still delete the bucket in Step 7.

**Checkpoint:** Three text files are in S3 under `docs/`, and you have written down your bucket name.

---

## Step 3 — Create the Amazon Q Business application

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

---

## Step 4 — Connect the S3 data source and sync

An application with no data answers nothing. Now connect it to the documents you uploaded in Step 2.

1. Open your application in the Q Business console and find the **data sources** area.
2. Choose to **add a data source**. Browse the available connectors before picking one.

   Note how many there are. Connectors typically cover S3, web crawlers, document stores, wikis, ticketing systems, chat platforms, CRMs and file shares. **This connector catalogue is a large part of what you are buying** — each one is ingestion code, incremental sync logic and permission mapping that you would otherwise write and maintain yourself.

3. Choose the **Amazon S3** connector.
4. Configure it:
   - **Data source name** — something recognisable, such as `northwind-docs`
   - **IAM role** — let the console create one, so it has read access to your bucket
   - **Bucket and prefix** — your bucket from Step 2, with the prefix `docs/`
   - **Sync schedule** — choose **run on demand**. Do not schedule a recurring sync for a lab; a schedule keeps working on documents you no longer care about.
5. Add the data source, then **start a sync** manually.
6. Wait for the sync to complete. Watch the sync history and note what it reports: how many documents were **scanned**, **added**, **modified**, **deleted** and **failed**.

   > **If documents fail, the assistant will not know about them.** A common cause is the data source role lacking read access to the bucket. Check the sync history rather than assuming success — a Q Business application that answers "I don't know" is far more often a failed sync than a model limitation.

7. Confirm three documents were added successfully.

## What just happened

The sync did, as a managed service, exactly the indexing pipeline you built by hand in Lab 08:

| Lab 08, by hand | Q Business, managed |
|---|---|
| Chunk the documents | Done for you |
| Embed each chunk | Done for you — you do not choose the model |
| Store vectors in a vector store | The Q Business index |
| Track document permissions | Done for you, from the source system's ACLs |
| Re-sync when documents change | The connector's incremental sync |

You gave up all control over chunking strategy, embedding model and retrieval tuning. In exchange you wrote no code and manage no vector store. **That is the trade, and it is the right trade for a standard enterprise knowledge assistant** — Lab 15 shows the Bedrock Knowledge Bases route when you need the control back.

**Checkpoint:** The sync completed and the sync history shows three documents added and none failed.

---

## Step 5 — Ask questions grounded in your documents

1. From your application in the console, open the **web experience** — the console provides a deployed URL for it. You may be asked to sign in with the identity you configured in Step 3.
2. Ask each question below and record the answer **and its citation**.

## Questions with answers in the documents

| # | Question | Answer given | Cited source? | Correct? |
|---|---|---|---|---|
| 1 | How many days of annual leave do I get? | | | |
| 2 | What happens to unused leave at the end of the year? | | | |
| 3 | What is the meal allowance when I travel overseas? | | | |
| 4 | How long do I have to submit an expense claim? | | | |
| 5 | When can I fly business class? | | | |
| 6 | My account is locked. What do I do? | | | |
| 7 | Can I install software on my laptop myself? | | | |

Check each answer against the source text from Step 2. **Every one of these facts is invented and appears nowhere in any model's training data.** A correct answer therefore proves retrieval worked.

## Now test the harder behaviours

**8. A question requiring synthesis across one document:**

```
I have been here six years and want to take three weeks off. How many
days do I have, and what approval do I need?
```

This needs the model to combine the five-year service rule (26 days), the 10-consecutive-day threshold, and the 14-day notice rule. Did it get all three?

**9. A question spanning two documents:**

```
I am travelling overseas for work next month. What do I need to know
about booking and about claiming afterwards?
```

Does it draw on the expense policy for both the booking rules and the claim rules? Does it cite more than one source?

**10. A question phrased in words the documents never use:**

```
I can't get into my account.
```

The IT document says "accounts lock after five failed attempts". Your question says none of those words. If this works, you have watched the semantic retrieval from Lab 08 operating inside a managed service.

## What to look for in every answer

- **Is there a citation?** Q Business is designed to show where an answer came from. Click through and verify the cited passage actually says what the answer claims. This is Lab 09's "cite sources" mitigation, and it is what makes checking cheap enough to actually do.
- **Is the answer complete?** A partial answer that omits a condition — the approval requirement, the deadline — is a real risk in a policy assistant.
- **Is the tone appropriate for an employee-facing tool?**

**Checkpoint:** All ten questions asked, answers and citations recorded, and you have clicked through at least one citation to verify it.

---

## Step 6 — Test the boundaries of grounding

Step 5 showed the system working. This step is more useful: it shows you where it stops. **Knowing where an assistant fails is what qualifies you to deploy one.**

## Test 1 — A question the documents cannot answer

```
What is Northwind Logistics' parental leave entitlement?
```

Your leave policy says nothing about parental leave. Record exactly what happens:

- Did it say it **could not find** the answer? — correct behaviour, and the whole point of grounding
- Did it answer from **general knowledge** about typical parental leave? — this is the failure mode. Note it carefully.
- Did it give a **partial** answer, or bridge from annual leave to parental leave? — subtly the most dangerous outcome, because it looks authoritative

Compare this with Lab 09, where you had to write "if the answer is not in the reference text, say Not found" by hand. A managed assistant should do this by default.

## Test 2 — A question with a false premise

```
Why does the company only give 14 days of annual leave?
```

The policy says **21**. Does the assistant correct the premise, or accept it and explain a policy that does not exist? Accepting false premises is a well-documented failure mode (Lab 09, Step 3) and it appears in grounded systems too.

## Test 3 — A stale-document scenario

You do not need to run this one — reason it through and write your answer:

> Suppose HR updates the leave policy in S3 to 25 days, but nobody triggers a sync and no schedule is configured. What does the assistant tell employees tomorrow?

It confidently gives the **old** answer, with a citation, and the citation makes it *more* convincing. **Grounding guarantees the answer matches the indexed documents. It guarantees nothing about whether those documents are current.**

This is why Step 4 asked you to notice the sync schedule. Operationally: who owns the sync, how often does it run, and how would anyone find out it had been failing for three weeks?

## Test 4 — The permissions question

Also reason this one through:

> Two employees ask "what is the meal allowance?" One is in finance and can read a confidential document listing director-level allowances. One cannot.

In a hand-built RAG system the index typically has no idea who is asking — both users get the same retrieval, and the confidential figure leaks. Q Business filters retrieval by the user's permissions, inherited from the source system's access controls. **The two employees correctly get different answers.**

This is the single strongest technical argument for a managed enterprise assistant, and it is heavily weighted on the exam.

## Record your findings

| Test | What you expected | What actually happened | Implication for deployment |
|---|---|---|---|
| Out-of-scope question | | | |
| False premise | | | |
| Stale documents | *(reasoned)* | | |
| Per-user permissions | *(reasoned)* | | |

**Checkpoint:** All four boundary tests recorded, and you can state what grounding does and does not guarantee.

---

## Step 7 — Clean up

> ## This is the most important cleanup in the course. Do it now, not later.
>
> Unlike every Bedrock lab, **Amazon Q Business bills for as long as the application exists** — per-user subscriptions and index capacity accrue whether or not anyone asks a question. Closing the web experience, closing the browser and signing out of the console all do **nothing**. Only **deleting the application** stops the charge.

## 1. Delete the Q Business application

Deleting the application removes its index, its data source configurations and its web experience together.

**Console:** open the Amazon Q Business console at <https://console.aws.amazon.com/amazonq/>, select your application, and choose **Delete**. Confirm by typing the name if prompted.

**CLI:**

```bash
# Confirm the application ID
aws qbusiness list-applications --region "$REGION"

# Delete it
aws qbusiness delete-application \
  --region "$REGION" \
  --application-id <your-application-id>
```

Then **verify** — do not assume:

```bash
aws qbusiness list-applications --region "$REGION"
```

The output must no longer contain your application. Deletion may take a few minutes; if it still appears, wait and check again. **Do not close your laptop until this list is clear.**

## 2. Delete the S3 bucket

```bash
aws s3 rm "s3://$BUCKET" --recursive
aws s3 rb "s3://$BUCKET"
aws s3 ls | grep q-business-lab   # should return nothing
```

## 3. Remove local files

```bash
rm -rf qdocs
```

## 4. Identity Center and IAM roles

- If the console **created an AWS IAM Identity Center instance** for you in Step 3 and your account had none before, decide whether to keep it. Identity Center itself does not carry a charge in the way the Q Business application does, but an instance you did not intend to create is a governance concern in a shared account. If your organisation was already using Identity Center, **leave it alone** — deleting it affects far more than this lab.
- The **service roles** created in Steps 3 and 4 do not cost anything. Delete them for tidiness if this is your own account; leave them if you are unsure what else might use them. Deleting an IAM role that something else depends on is a worse outcome than leaving an unused role behind.

## 5. Set a budget

If you have not already, create an **AWS Budget** or billing alert on this account. Q Business is exactly the kind of resource that shows up as an unwelcome surprise at month end, because nothing about an idle application looks like it is running.

## Final verification

- [ ] `aws qbusiness list-applications` no longer lists your application
- [ ] The S3 bucket is deleted
- [ ] Local `qdocs` directory removed
- [ ] You have made a deliberate decision about the Identity Center instance and the service roles
- [ ] A budget or billing alert exists on the account

**Checkpoint:** The application is confirmed deleted from the API, not just closed in the browser.

---

## Verification

- [ ] You can explain how Amazon Q Business differs from Amazon Bedrock in what it provides and what it takes away
- [ ] Three documents were uploaded to S3 and the sync history shows three added and none failed
- [ ] You asked the seven document-grounded questions and recorded the answers and citations
- [ ] You clicked through at least one citation and verified the source says what the answer claimed
- [ ] You tested a question that spans two documents and one phrased in words the documents never use
- [ ] You recorded what happened on the out-of-scope question and the false-premise question
- [ ] You can explain what grounding guarantees and what it does not — specifically the stale-document case
- [ ] You can explain why permission-aware retrieval is hard to build and why it is the main reason to buy
- [ ] **`aws qbusiness list-applications` no longer lists your application**, the S3 bucket is deleted, and a budget or billing alert exists

## Discussion questions

1. Amazon Q Business gives you a finished, permission-aware, cited assistant but no control over the model, the prompt, the chunking or the embedding model. Describe a use case where that trade is clearly right, and one where you would build on Bedrock Knowledge Bases instead.
2. HR updates a policy document but the sync never runs. The assistant confidently gives the old answer, with a citation that makes it more convincing. Who owns this failure operationally, and what controls would you put in place to detect it?
3. Two employees ask the same question and correctly receive different answers because of document permissions. Why is this so difficult in a hand-built RAG system, and what could go wrong in a system that ignores it?

---

Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.
