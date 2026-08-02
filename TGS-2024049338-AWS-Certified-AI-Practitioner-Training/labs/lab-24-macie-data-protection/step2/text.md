# Step 2 — Create a bucket and upload synthetic sample data

> **SYNTHETIC DATA ONLY.** Every value below is fabricated for teaching. The names are invented, the email addresses use the reserved `example.com` domain which cannot receive mail, and the identifiers are made-up strings. **Do not replace any of it with real personal data.**

## Create the bucket

```bash
aws s3api create-bucket \
  --bucket macie-lab-data-<your-initials>-<random-number> \
  --region us-east-1

aws s3api put-public-access-block \
  --bucket macie-lab-data-<your-initials>-<random-number> \
  --public-access-block-configuration \
    "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

Use the same bucket name throughout. Substitute it wherever you see `<bucket>` below.

## File 1 — a "customer export" that should never have been used for training

Create `customer_export.csv`:

```csv
record_id,full_name,email,phone,employee_ref,notes
1001,Marigold Thistlewick,marigold.thistlewick@example.com,+1-555-0142,EMP-ZZ-4417,Requested account closure
1002,Barnaby Quillfeather,barnaby.quillfeather@example.com,+1-555-0177,EMP-ZZ-8802,Escalated billing dispute
1003,Persimmon Vandergrift,persimmon.vandergrift@example.com,+1-555-0198,EMP-ZZ-1250,Upgraded to premium tier
1004,Cornelius Pemberwick,cornelius.pemberwick@example.com,+1-555-0121,EMP-ZZ-6634,Reported login failure
1005,Ottoline Frostwhistle,ottoline.frostwhistle@example.com,+1-555-0165,EMP-ZZ-3391,Requested data export
1006,Fitzwilliam Grimsdale,fitzwilliam.grimsdale@example.com,+1-555-0189,EMP-ZZ-7728,Cancelled subscription
1007,Hyacinth Ravensworth,hyacinth.ravensworth@example.com,+1-555-0133,EMP-ZZ-2065,Password reset request
1008,Ignatius Bellweather,ignatius.bellweather@example.com,+1-555-0154,EMP-ZZ-9143,Feedback on new feature
```

The names are deliberately absurd — that is the point. If any of them matched a real person it would be coincidence, and the `555-01xx` phone range is reserved for fiction. `example.com` is reserved by RFC 2606 and can never be registered.

## File 2 — a "support transcript" of the kind that ends up in a RAG knowledge base

Create `support_transcript.txt`:

```
Ticket ZZ-88213 — Support transcript (SYNTHETIC TEST DATA)

Agent: Thank you for contacting support. May I have your name?
Customer: Marigold Thistlewick.
Agent: And a contact email for the case?
Customer: marigold.thistlewick@example.com
Agent: I can see the account. The best callback number we have is
       +1-555-0142 — is that still correct?
Customer: Yes. My internal reference is EMP-ZZ-4417 if that helps.
Agent: Noted. I have escalated the case and you will hear back within
       two business days.
```

This file is the realistic threat. A CSV in a data lake is at least obviously structured data that someone might review. A support transcript looks like harmless prose, gets indexed into a knowledge base without a second thought, and quietly makes every detail in it retrievable through a chatbot.

## File 3 — a clean control file

Create `product_catalogue.csv`:

```csv
sku,product_name,category,unit_price,in_stock
SKU-4410,Ceramic Mug,Kitchenware,12.50,true
SKU-4411,Steel Kettle,Kitchenware,44.00,true
SKU-4412,Linen Napkin Set,Kitchenware,18.75,false
SKU-4413,Bamboo Cutting Board,Kitchenware,29.90,true
```

Including a file with no personal data lets you confirm Macie is discriminating rather than flagging everything. A detection tool that fires on every object is as useless as one that fires on none.

## Upload

```bash
aws s3 cp customer_export.csv    s3://<bucket>/raw/
aws s3 cp support_transcript.txt s3://<bucket>/raw/
aws s3 cp product_catalogue.csv  s3://<bucket>/raw/
aws s3 ls s3://<bucket>/raw/
```

All three objects should be listed. Keep the total tiny — the next step explains why data volume is the thing you are billed on.
