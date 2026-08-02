# Step 1 — Classify structured, semi-structured and unstructured data

Before you store or label anything, you need the vocabulary. AIF-C01 asks you to identify
a data type from a description and to pick a service that suits it.

### 1.1 The three structural categories

| Category | Definition | Examples | Where it usually lives |
|---|---|---|---|
| **Structured** | Fixed schema; rows and columns defined in advance | Sales table, sensor readings, transaction ledger | Relational database, data warehouse, CSV/Parquet in S3 |
| **Semi-structured** | Self-describing tags or keys, but no rigid schema | JSON, XML, log lines, key-value documents | Amazon DynamoDB, JSON files in S3 |
| **Unstructured** | No predefined model; meaning is in the content itself | Images, audio, video, free-text documents, email | Amazon S3 |

The practical consequence: **structured data is usually ready for classical ML
(XGBoost, Linear Learner) with modest preparation; unstructured data usually needs deep
learning or a managed AI service**, because the useful features are not sitting in
columns.

### 1.2 The four data types you must recognise

| Type | Shape | Distinguishing feature | Typical model or service |
|---|---|---|---|
| **Tabular** | Rows = records, columns = features | Order of rows does not matter | XGBoost, Linear Learner |
| **Time-series** | Values indexed by timestamp | Order *does* matter; past predicts future | Forecasting models |
| **Image** | Pixel grids | Spatial structure | Convolutional networks, Amazon Rekognition |
| **Text** | Sequences of tokens | Sequential and contextual | Language models, Amazon Comprehend |

> **Exam tip:** the giveaway for time-series is that reordering the rows would destroy the
> signal. A table of customers is tabular; a table of one customer's monthly balance is
> time-series.

### 1.3 Classify these

| # | Dataset | Structural category | Data type |
|---|---|---|---|
| 1 | A CSV of 50,000 loan applications with 14 columns | | |
| 2 | Five years of hourly electricity demand | | |
| 3 | 3,000 JPEG photos of warehouse shelves | | |
| 4 | 20,000 customer support emails | | |
| 5 | Application logs in JSON, one object per line | | |

**Answer key:** 1 = structured / tabular · 2 = structured / time-series ·
3 = unstructured / image · 4 = unstructured / text · 5 = semi-structured / text (log data).

Keep this table — you will store one example of each in Step 2.
