import os
import httpx
import json
from fastapi import FastAPI, Depends
from common_lib.tenants import require_tenant

LLM_ENDPOINT   = os.getenv("LLM_ENDPOINT")
ANALYTICS_URL  = os.getenv("ANALYTICS_URL")
RULES_URL      = os.getenv("RULES_URL")
OPT_URL        = os.getenv("OPT_URL")

app = FastAPI(title="Cost Agent")

@app.post("/evaluate")
async def evaluate(payload: dict, tenant_id: str = Depends(require_tenant)):
    decision = payload.get("decision","")

    async with httpx.AsyncClient(timeout=60) as client:
        analytics = (await client.get(
            ANALYTICS_URL,
            headers={"X-Tenant-ID": tenant_id}
        )).json()
        rules = (await client.get(
            RULES_URL,
            headers={"X-Tenant-ID": tenant_id}
        )).json()
        opt = (await client.get(
            OPT_URL,
            headers={"X-Tenant-ID": tenant_id}
        )).json()

        system_msg = """
You are the COST ANALYSIS AGENT.
Your job: Evaluate ONLY cost and financial impact.
You MUST follow tenant rules.
You MUST respond valid JSON with keys:
dimension, rating, reasoning, risk_cost_estimate.
'rating' is 0-100, higher = better financially.
If high risk cost, lower the rating.
"""
        user_msg = {
            "DECISION": decision,
            "RULES": rules,
            "ANALYTICS": analytics,
            "COST_OPTIMIZER_VIEW": opt
        }

        llm_resp = (await client.post(
            LLM_ENDPOINT,
            json={
                "model":"Qwen2.5-14B-Instruct",
                "messages":[
                    {"role":"system","content":system_msg.strip()},
                    {"role":"user","content":json.dumps(user_msg)}
                ],
                "temperature":0.1,
                "response_format":{"type":"json_object"}
            }
        )).json()

    content = llm_resp["choices"][0]["message"]["content"]
    return json.loads(content)
