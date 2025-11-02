from fastapi import FastAPI, Depends
from common_lib.tenants import require_tenant
from common_lib.db import fetch_one
from cost_optimizer import compute_cost_view
from workflow_optimizer import compute_workflow_view
from bottleneck_optimizer import compute_bottleneck_view
from risk_model import compute_risk_view

app = FastAPI(title="Optimizer Service")

def get_rules_obj(tenant_id: str):
    row = fetch_one("SELECT rules FROM tenant_rules WHERE tenant_id=%s",[tenant_id])
    return row["rules"] if row else {}

@app.get("/summary")
async def summary(tenant_id: str = Depends(require_tenant)):
    return {
        "tenant_id": tenant_id,
        "cost_recommendations": ["Reduce overtime on Line 2 night shift (-4% labor cost)"],
        "workflow_recommendations": ["Move inspection earlier to cut rework accumulation"],
        "bottleneck_recommendations": ["Run SMED on Packaging Line 2"]
    }

@app.get("/cost_view")
async def cost_view(tenant_id: str = Depends(require_tenant)):
    rules = get_rules_obj(tenant_id)
    return {
        "tenant_id": tenant_id,
        **compute_cost_view(tenant_id, rules)
    }

@app.get("/workflow_view")
async def workflow_view(tenant_id: str = Depends(require_tenant)):
    rules = get_rules_obj(tenant_id)
    return {
        "tenant_id": tenant_id,
        **compute_workflow_view(tenant_id, rules)
    }

@app.get("/bottleneck_view")
async def bottleneck_view(tenant_id: str = Depends(require_tenant)):
    rules = get_rules_obj(tenant_id)
    return {
        "tenant_id": tenant_id,
        **compute_bottleneck_view(tenant_id, rules)
    }

@app.get("/risk_view")
async def risk_view(tenant_id: str = Depends(require_tenant)):
    rules = get_rules_obj(tenant_id)
    return {
        "tenant_id": tenant_id,
        **compute_risk_view(tenant_id, rules)
    }
