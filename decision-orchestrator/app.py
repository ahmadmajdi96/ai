import os
import httpx
import json
from fastapi import FastAPI, Depends, HTTPException
from common_lib.tenants import require_tenant
from aggregator import aggregate_ratings

COST_AGENT_URL        = os.getenv("COST_AGENT_URL")
WORKFLOW_AGENT_URL    = os.getenv("WORKFLOW_AGENT_URL")
BOTTLENECK_AGENT_URL  = os.getenv("BOTTLENECK_AGENT_URL")
RISK_AGENT_URL        = os.getenv("RISK_AGENT_URL")

AGENTS = {
    "cost": COST_AGENT_URL,
    "workflow": WORKFLOW_AGENT_URL,
    "bottleneck": BOTTLENECK_AGENT_URL,
    "risk": RISK_AGENT_URL
}

app = FastAPI(title="Decision Orchestrator")

@app.post("/evaluate_decision")
async def evaluate_decision(payload: dict, tenant_id: str = Depends(require_tenant)):
    decision = payload.get("decision")
    if not decision:
        raise HTTPException(status_code=400, detail="Missing 'decision'")

    requested_agents = payload.get("agents", ["cost","workflow","bottleneck","risk"])

    results = []
    async with httpx.AsyncClient(timeout=60) as client:
        for a in requested_agents:
            url = AGENTS.get(a)
            if not url:
                continue
            r = await client.post(
                url,
                headers={"X-Tenant-ID": tenant_id},
                json={"decision": decision}
            )

            data = r.json()
            if isinstance(data, str):
                try:
                    data = json.loads(data)
                except:
                    data = {"dimension": a, "error": "unparseable string"}

            if isinstance(data, dict) and "dimension" in data:
                results.append(data)
            elif "choices" in data:
                try:
                    msg = data["choices"][0]["message"]["content"]
                    results.append(json.loads(msg))
                except:
                    results.append({"dimension": a, "error": "bad llm response"})

    summary = aggregate_ratings(results, tenant_id)

    return {
        "tenant_id": tenant_id,
        "results": results,
        "summary": summary
    }
