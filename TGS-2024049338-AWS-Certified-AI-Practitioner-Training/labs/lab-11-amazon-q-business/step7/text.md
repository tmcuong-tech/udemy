# Step 7 — Clean up

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
