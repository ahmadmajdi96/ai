import json
from fastapi import FastAPI, Depends, HTTPException, Header
from common_lib.db import fetch_one, execute
from common_lib.tenants import require_tenant
from common_lib.utils import now_iso

app = FastAPI(title="Rules Service")

@app.get("/rules")
async def get_rules(tenant_id: str = Depends(require_tenant)):
    row = fetch_one(
        "SELECT rules, updated_at FROM tenant_rules WHERE tenant_id=%s",
        [tenant_id]
    )
    if not row:
        return {
            "tenant_id": tenant_id,
            "rules": {},
            "updated_at": now_iso()
        }
    return {
        "tenant_id": tenant_id,
        "rules": row["rules"],
        "updated_at": row["updated_at"].isoformat() + "Z"
    }

@app.post("/rules/update")
async def update_rules(payload: dict, x_tenant_id: str = Header(None)):
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="Missing tenant")

    rules = payload.get("rules", {})
    execute("""
        INSERT INTO tenant_rules (tenant_id, rules, updated_at)
        VALUES (%s, %s, NOW())
        ON CONFLICT (tenant_id)
        DO UPDATE SET rules = EXCLUDED.rules, updated_at = NOW();
    """, [x_tenant_id, json.dumps(rules)])
    return {"status": "ok"}
