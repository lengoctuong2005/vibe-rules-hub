---
name: data-engineering-suite
description: |
  Master Data Engineering Suite for modern analytics and lakehouses: Medallion Architecture (Bronze/Silver/Gold), streaming ingestion (Kafka/Redpanda), vectorized query processing (DuckDB, Polars), dbt transformation models, Great Expectations data contracts, and Change Data Capture (CDC).
triggers:
  - "data-engineering"
  - "data-engineering-suite"
  - "kafka"
  - "duckdb"
  - "polars"
  - "dbt"
  - "etl"
  - "lakehouse"
license: MIT
metadata:
  origin: ECC
---

# Data Engineering Master Suite

Production-grade framework for designing, implementing, securing, and operating scalable batch and real-time data pipelines, analytical lakehouses, and dimensional data marts.

---

## 1. System Architecture Topology

```
+─────────────────────────────────────────────────────────────────────────+
|                          RAW DATA SOURCES                               |
|  Transactional DBs (Postgres CDC) · Webhook Streams · IoT Telemetry     |
+────────────────────────────────────┬────────────────────────────────────+
                                     │ Streaming (Kafka) / Batch Files
                                     ▼
+─────────────────────────────────────────────────────────────────────────+
|                       BRONZE LAYER (RAW STORAGE)                        |
|  Immutable Append-Only Parquet / Iceberg · Ingestion Metadata Tagging    |
+────────────────────────────────────┬────────────────────────────────────+
                                     │ Vectorized Ingestion (Polars/DuckDB)
                                     ▼
+─────────────────────────────────────────────────────────────────────────+
|                      SILVER LAYER (CLEANED & TYPED)                     |
|  Deduplication · Schema Enforcement · Great Expectations Contract Gate  |
+────────────────────────────────────┬────────────────────────────────────+
                                     │ dbt Incremental Transformations
                                     ▼
+─────────────────────────────────────────────────────────────────────────+
|                     GOLD LAYER (DIMENSIONAL MARTS)                      |
|  Star Schema (Facts & Dimensions) · Aggregations · Feature Stores       |
+────────────────────────────────────┬────────────────────────────────────+
                                     │ SQL Queries / BI Connectors
                                     ▼
+─────────────────────────────────────────────────────────────────────────+
|                     ANALYTICS & CONSUMPTION TIER                        |
|  Executive BI Dashboards · ML Feature Extraction · Ad-hoc DuckDB SQL    |
+─────────────────────────────────────────────────────────────────────────+
```

---

## 2. Fast Columnar Processing with DuckDB

```python
# analytics/duckdb_analytics.py
import duckdb

# ponytail: In-memory vectorized analytics query on Parquet files
def analyze_daily_sales_trends(parquet_glob: str) -> duckdb.DuckDBPyRelation:
    con = duckdb.connect(database=":memory:")
    query = f'''
        SELECT
            date_trunc('day', timestamp) AS order_date,
            country_code,
            COUNT(order_id) AS total_orders,
            SUM(amount_cents) / 100.0 AS total_revenue_usd,
            AVG(amount_cents) / 100.0 AS average_order_value
        FROM read_parquet('{parquet_glob}')
        WHERE status = 'COMPLETED'
        GROUP BY 1, 2
        ORDER BY 1 DESC, 4 DESC;
    '''
    return con.sql(query)
```

---

## 3. Polars Streaming Pipeline with Checkpointing

```python
# pipeline/streaming_pipeline.py
import polars as pl
from pathlib import Path

def process_stream_batch(source_dir: str, output_parquet: str) -> int:
    # Scan new raw JSON files incrementally
    lazy_df = (
        pl.scan_ndjson(f"{source_dir}/*.json")
        .with_columns(
            pl.col("timestamp").str.to_datetime(),
            pl.col("user_id").cast(pl.Utf8),
            pl.col("amount_cents").cast(pl.Int64)
        )
        .filter(pl.col("amount_cents") > 0)
    )

    df = lazy_df.collect()
    df.write_parquet(output_parquet, compression="zstd")
    return len(df)
```

---

## 4. dbt Dimensional Model Blueprint

```sql
-- models/marts/fct_orders.sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge'
) }}

WITH source_data AS (
    SELECT * FROM {{ ref('stg_orders') }}
    {% if is_incremental() %}
      WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
    {% endif %}
),

customers AS (
    SELECT * FROM {{ ref('dim_customers') }}
)

SELECT
    s.order_id,
    c.customer_key,
    s.order_date,
    s.status,
    s.total_amount_cents,
    s.discount_amount_cents,
    (s.total_amount_cents - s.discount_amount_cents) AS net_amount_cents,
    s.updated_at
FROM source_data s
INNER JOIN customers c ON s.customer_id = c.customer_id AND c.is_current = true
```

---

## 5. Great Expectations Data Contract Suite

```json
{
  "expectation_suite_name": "orders_bronze_to_silver",
  "meta": {
    "great_expectations_version": "0.18.0"
  },
  "expectations": [
    {
      "expectation_type": "expect_column_values_to_not_be_null",
      "kwargs": { "column": "order_id" }
    },
    {
      "expectation_type": "expect_column_values_to_be_in_set",
      "kwargs": {
        "column": "status",
        "value_set": ["PENDING", "PROCESSING", "COMPLETED", "CANCELLED"]
      }
    },
    {
      "expectation_type": "expect_column_values_to_be_between",
      "kwargs": {
        "column": "amount_cents",
        "min_value": 0,
        "max_value": 100000000
      }
    }
  ]
}
```

---

## 6. Real-Time Kafka Streaming Consumer (Python)

```python
# pipeline/kafka_consumer.py
import json
from kafka import KafkaConsumer
import polars as pl

def stream_cdc_events(bootstrap_servers: str, topic: str):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='analytics_bronze_writer',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    batch = []
    for message in consumer:
        payload = message.value.get('payload', {})
        batch.append({
            'op': payload.get('op'),
            'table': message.value.get('schema', {}).get('name'),
            'after': json.dumps(payload.get('after', {})),
            'ts_ms': payload.get('ts_ms')
        })
        if len(batch) >= 1000:
            df = pl.DataFrame(batch)
            df.write_parquet(f"/data/bronze/cdc_{message.offset}.parquet")
            batch = []
```

---

## 7. Subagent Delegation Matrix

| Subagent | Role & Objective | Deliverable |
|----------|------------------|-------------|
| `data-architect` | Medallion architecture & dimensional modeling | `data_architecture.md` |
| `pipeline-engineer` | Kafka consumers, Polars ETL & CDC ingestion | Pipeline source scripts |
| `dbt-modeler` | dbt incremental models & schema tests | dbt SQL models |
| `data-quality-guard`| Great Expectations data contracts & alerts | Data quality test suite |
| `performance-tuner` | Parquet compression, indexing & SQL tuning | Performance benchmark |
