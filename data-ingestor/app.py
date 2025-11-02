from fastapi import FastAPI, Header, HTTPException
from normalizer import load_and_normalize_csv
from storage import store_file_reference

app = FastAPI(title="Data Ingestor")

@app.post("/ingest")
async def ingest(payload: dict, x_tenant_id: str = Header(None)):
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="Missing tenant")

    s3_path = payload["s3_path"]
    schema_map = payload["schema_map"]
    table_type = payload.get("table_type", "production_events")

    store_file_reference(x_tenant_id, s3_path, table_type)
    rows_inserted = load_and_normalize_csv(
        tenant_id=x_tenant_id,
        s3_path=s3_path,
        schema_map=schema_map,
        table_type=table_type
    )

    return {"status": "ok", "inserted_rows": rows_inserted}
