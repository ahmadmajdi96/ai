from fastapi import FastAPI, Depends
from common_lib.tenants import require_tenant
from retriever import retrieve_relevant_context

app = FastAPI(title="RAG Service")

@app.post("/retrieve")
async def retrieve(payload: dict, tenant_id: str = Depends(require_tenant)):
    ask = payload.get("ask","")
    ctx = retrieve_relevant_context(tenant_id, ask)
    return {
        "tenant_id": tenant_id,
        "context_snippets": ctx
    }
