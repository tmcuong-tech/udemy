# Step 6 — Clean up

> **Disable Macie.** While Macie is enabled it charges a monthly fee per S3 bucket it monitors, prorated, whether or not you run any job. Leaving it on across a whole account with many buckets is the most likely way to be surprised by a bill from this lab. Discovery jobs themselves are charged once, on the volume already scanned — you cannot un-run a job, but you can stop future ones.

## 1. Cancel the discovery job

A one-time job that has already completed will not run again, but cancel it explicitly so nothing is left in a schedulable state:

```bash
aws macie2 update-classification-job \
  --job-id <job-id> \
  --job-status CANCELLED \
  --region us-east-1
```

Verify no job is in a running or paused state:

```bash
aws macie2 list-classification-jobs --region us-east-1 \
  --query 'items[].{Name:name,Status:jobStatus}' --output table
```

## 2. Delete the custom data identifier

```bash
aws macie2 list-custom-data-identifiers --region us-east-1
aws macie2 delete-custom-data-identifier \
  --id <custom-data-identifier-id> \
  --region us-east-1
```

## 3. Empty and delete the S3 bucket

Delete this bucket even though its contents are synthetic. A bucket named after a data-protection lab, containing files that *look* like a customer export, is exactly the kind of artefact that confuses a future audit of your own account.

```bash
aws s3 rm s3://macie-lab-data-<your-initials>-<random-number>/ --recursive
aws s3api delete-bucket --bucket macie-lab-data-<your-initials>-<random-number>
```

Delete the local copies too:

```bash
rm customer_export.csv support_transcript.txt product_catalogue.csv
```

## 4. Disable Macie

```bash
aws macie2 disable-macie --region us-east-1
```

Understand what this does: disabling Macie **permanently deletes all of your findings and job records** in that Region. If you needed any of it as audit evidence you would have had to export it to S3 first (Step 5). For this lab there is nothing worth keeping, but on a real account confirm exports are in place before you disable.

Confirm the session is gone:

```bash
aws macie2 get-macie-session --region us-east-1
```

This should now return a resource-not-found error. That error is the success condition.

## 5. Check the other Regions

Macie is regional, and it is easy to enable it in a second Region by accident while clicking through the console. If you switched Regions at any point during the lab, check there too:

```bash
aws macie2 get-macie-session --region <other-region>
```

## 6. Verify the spend

Open the **Billing and Cost Management** console the next day and filter Cost Explorer to Amazon Macie. Given three files of a few kilobytes and a session lasting under an hour, the charge should be negligible or zero under a free trial — but confirming it rather than assuming it is the habit that matters.
