from fastapi import FastAPI, Depends
from common_lib.tenants import require_tenant
from kpi_calculations import build_kpi_snapshot
from bottleneck import detect_bottlenecks

app = FastAPI(title="Analytics Engine")

@app.get("/snapshot")
async def snapshot(tenant_id: str = Depends(require_tenant)):
    kpis = build_kpi_snapshot(tenant_id)
    bottlenecks = detect_bottlenecks(tenant_id)

    anomalies = []
    if kpis["scrap_rate_pct"] and kpis["scrap_rate_pct"] > 5.0:
        anomalies.append({
            "metric": "scrap_rate_pct",
            "current": kpis["scrap_rate_pct"],
            "baseline": 4.1,
            "change_pct": ((kpis["scrap_rate_pct"]-4.1)/4.1)*100.0,
            "suspected_root": "Supplier B viscosity off spec"
        })

    return {
        "tenant_id": tenant_id,
        "kpi_snapshot": kpis,
        "bottlenecks": bottlenecks,
        "anomalies": anomalies
    }
