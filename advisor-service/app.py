import os
import httpx
import json
from fastapi import FastAPI, Depends
from common_lib.tenants import require_tenant
from merge_context import build_context_bundle
from prompt_builder import build_advisor_prompt

ANALYTICS_URL  = os.getenv("ANALYTICS_URL")
RULES_URL      = os.getenv("RULES_URL")
OPTIMIZER_URL  = os.getenv("OPTIMIZER_URL")
RAG_URL        = os.getenv("RAG_URL")
LLM_ENDPOINT   = os.getenv("LLM_ENDPOINT")

app = FastAPI(title="Advisor Service")

@app.post("/advise")
async def advise(payload: dict, tenant_id: str = Depends(require_tenant)):
    ask = payload.get("ask","Analyze operations and next steps")

    async with httpx.AsyncClient() as client:
        analytics = (await client.get(
            ANALYTICS_URL,
            headers={"X-Tenant-ID": tenant_id}
        )).json()

        rules     = (await client.get(
            RULES_URL,
            headers={"X-Tenant-ID": tenant_id}
        )).json()

        optimizer = (await client.get(
            OPTIMIZER_URL,
            headers={"X-Tenant-ID": tenant_id}
        )).json()

        ragctx    = (await client.post(
            RAG_URL,
            headers={"X-Tenant-ID": tenant_id},
            json={"ask": ask}
        )).json()

        bundle = build_context_bundle(analytics, rules, optimizer, ragctx)
        msgs = build_advisor_prompt(tenant_id, ask, bundle)

        llm_resp = (await client.post(
            LLM_ENDPOINT,
            json={
                "model":"Qwen2.5-14B-Instruct",
                "messages":msgs,
                "temperature":0.2,
                "response_format":{"type":"json_object"}
            },
            timeout=60
        )).json()

    content = llm_resp["choices"][0]["message"]["content"]
    result = json.loads(content)

    return {
        "tenant_id": tenant_id,
        **result
    }
