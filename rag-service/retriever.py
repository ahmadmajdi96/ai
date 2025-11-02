from common_lib.db import fetch_all

def retrieve_relevant_context(tenant_id: str, question: str):
    rows = fetch_all("""
        SELECT doc_id, chunk_id, content
        FROM tenant_docs
        WHERE tenant_id=%s
        ORDER BY doc_id DESC, chunk_id DESC
        LIMIT 2
    """,[tenant_id])
    out = []
    for r in rows:
        out.append({
            "source": f"{r['doc_id']}#{r['chunk_id']}",
            "text": r["content"]
        })
    if not out:
        out = [{"source":"none","text":"No context"}]
    return out
