CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS production_events (
    tenant_id TEXT NOT NULL,
    ts TIMESTAMP NOT NULL,
    line_id TEXT,
    units_made INT,
    defects INT,
    downtime_reason TEXT
);

CREATE TABLE IF NOT EXISTS kpi_snapshots (
    tenant_id TEXT NOT NULL,
    snapshot_ts TIMESTAMP NOT NULL DEFAULT NOW(),
    throughput_per_hour NUMERIC,
    scrap_rate_pct NUMERIC,
    downtime_min NUMERIC,
    late_orders_count INT
);

CREATE TABLE IF NOT EXISTS bottleneck_stats (
    tenant_id TEXT NOT NULL,
    line TEXT,
    utilization_pct NUMERIC,
    impact_units_per_shift NUMERIC,
    note TEXT,
    snapshot_ts TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tenant_rules (
    tenant_id TEXT PRIMARY KEY,
    rules JSONB NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tenant_docs (
    tenant_id TEXT NOT NULL,
    doc_id TEXT NOT NULL,
    chunk_id TEXT NOT NULL,
    content TEXT,
    embedding vector(1024),
    PRIMARY KEY (tenant_id, doc_id, chunk_id)
);

CREATE TABLE IF NOT EXISTS decision_log (
    tenant_id TEXT NOT NULL,
    decision TEXT NOT NULL,
    result_json JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
