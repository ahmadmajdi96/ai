import os
import httpx
from fastapi import FastAPI, Depends, Header
from fastapi import HTTPException
from common_lib.auth import verify_jwt_and_get_tenant

app = FastAPI(title="Gateway API")

DATA_INGESTOR_URL = os.getenv("DATA_INGESTOR_URL")
ANALYTICS_URL     = os.getenv("ANALYTICS_URL")
ADVISOR_URL       = os.getenv("ADVISOR_URL")
DECISION_URL      = os.getenv("DECISION_URL")

async def require_tenant(authorization: str = Header(...)):
    tenant_id = verify_jwt_and_get_tenant(authorization)
    return tenant_id

@app.post("/upload_csv")
async def upload_csv(file_meta: dict, tenant_id: str = Depends(require_tenant)):
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{DATA_INGESTOR_URL}/ingest",
            headers={"X-Tenant-ID": tenant_id},
            json=file_meta,
            timeout=60
        )
    return r.json()

@app.get("/kpi_snapshot")
async def kpi_snapshot(tenant_id: str = Depends(require_tenant)):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{ANALYTICS_URL}/snapshot",
            headers={"X-Tenant-ID": tenant_id},
            timeout=30
        )
    return r.json()

@app.post("/advisor/recommendations")
async def advisor_recommendations(question: dict, tenant_id: str = Depends(require_tenant)):
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{ADVISOR_URL}/advise",
            headers={"X-Tenant-ID": tenant_id},
            json=question,
            timeout=60
        )
    return r.json()

@app.post("/decision/evaluate")
async def decision_evaluate(payload: dict, tenant_id: str = Depends(require_tenant)):
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{DECISION_URL}/evaluate_decision",
            headers={"X-Tenant-ID": tenant_id},
            json=payload,
            timeout=120
        )
    return r.json()
