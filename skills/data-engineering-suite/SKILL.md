---
name: data-engineering-suite
description: |
  Master Data Engineering & High-Throughput Pipelines Suite unifying PostgreSQL relational storage, ClickHouse columnar OLAP analytics, Kafka/Redis event streaming, ETL/ELT batch processors, distributed scraping pipelines, and autonomous data quality validation (planner, architect, database-reviewer, tdd-guide).
triggers:
  - "data engineering"
  - "data pipeline"
  - "data-engineering-suite"
  - "clickhouse"
  - "kafka stream"
  - "etl pipeline"
  - "data scraper"
  - "high throughput data"
license: MIT
metadata:
  origin: ECC
---

# Data Engineering & High-Throughput Pipelines Master Suite

Enterprise architecture and engineering patterns for high-volume data ingestion, analytical columnar storage, stream processing, and distributed scraping.

---

## 1. End-to-End Data Pipeline Architecture

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  DATA SOURCES   │      │   EVENT STREAM  │      │  TRANSFORM/ETL  │
│  APIs, Webhooks │ ───► │  Kafka / Redis  │ ───► │ Workers / Celery│
│  Scrapers, DBs  │      │  Partitioned    │      │ Micro-batching  │
└─────────────────┘      └─────────────────┘      └────────┬────────┘
                                                           │
                                ┌──────────────────────────┴──────────────────────────┐
                                ▼                                                     ▼
                     ┌─────────────────────┐                               ┌─────────────────────┐
                     │     OLTP STORE      │                               │     OLAP STORE      │
                     │ PostgreSQL / MySQL  │                               │     ClickHouse      │
                     │ Relational & State  │                               │ Columnar Analytics  │
                     └─────────────────────┘                               └─────────────────────┘
```

---

## 2. ClickHouse OLAP Best Practices

### Engine Selection & Partitioning Strategy
- **ReplacingMergeTree**: Best for deduplication based on version column.
- **SummingMergeTree**: Ideal for pre-aggregated metrics and timeseries rollups.
- **Partition By**: Partition by `toYYYYMM(event_time)` to keep active partition count small.
- **Order By**: Order by primary filter columns in increasing cardinality order: `(tenant_id, event_type, event_time)`.

```sql
-- ponytail: Production ClickHouse Event Table Definition
CREATE TABLE default.events_stream (
    event_id UUID,
    tenant_id UInt32,
    event_type LowCardinality(String),
    payload String,
    event_time DateTime64(3, 'UTC'),
    created_at DateTime DEFAULT now()
) ENGINE = ReplacingMergeTree(created_at)
PARTITION BY toYYYYMM(event_time)
ORDER BY (tenant_id, event_type, event_time, event_id)
TTL event_time + INTERVAL 90 DAY;
```

---

## 3. Stream Processing & Kafka Consumers

```python
# ponytail: Idempotent Kafka Consumer Pattern with Schema Validation
from pydantic import BaseModel, Field
from datetime import datetime
import json

class EventMessage(BaseModel):
    event_id: str
    tenant_id: int
    event_type: str
    payload: dict
    timestamp: datetime = Field(default_factory=datetime.utcnow)

def process_stream_message(raw_msg_bytes: bytes, processed_ids_cache: set) -> bool:
    try:
        data = json.loads(raw_msg_bytes.decode('utf-8'))
        event = EventMessage.parse_obj(data)

        # Idempotency check
        if event.event_id in processed_ids_cache:
            return True

        # Process business transformation...
        processed_ids_cache.add(event.event_id)
        return True
    except Exception as err:
        # Route to Dead Letter Queue (DLQ)
        return False
```

---

## 4. Distributed Web Scraping & Ingestion

### Resilience Standards
1. **Header Rotation & User-Agent Management**: Mimic standard desktop browser headers without synthetic anomalies.
2. **Politeness & Rate Limits**: Maximum 5 concurrent requests per domain with randomized delays (100ms - 500ms).
3. **Structured HTML Extraction**: Use CSS selectors with fallback heuristics. Verify required fields exist before committing records.
