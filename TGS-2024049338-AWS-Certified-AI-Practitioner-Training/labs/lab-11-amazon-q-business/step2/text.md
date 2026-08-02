# Step 2 — Prepare documents in Amazon S3

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
