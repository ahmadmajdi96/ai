from fastapi import Header, HTTPException

async def require_tenant(x_tenant_id: str = Header(None)):
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="Missing tenant header X-Tenant-ID")
    return x_tenant_id
