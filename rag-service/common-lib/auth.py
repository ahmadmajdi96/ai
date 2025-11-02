import os
import jwt
from fastapi import Header, HTTPException

JWT_SECRET = os.getenv("JWT_SECRET", "CHANGE_ME")

def verify_jwt_and_get_tenant(authorization: str):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="No bearer token")
    token = authorization.split(" ", 1)[1]
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    tenant_id = data.get("tenant_id")
    if not tenant_id:
        raise HTTPException(status_code=401, detail="No tenant in token")
    return tenant_id
