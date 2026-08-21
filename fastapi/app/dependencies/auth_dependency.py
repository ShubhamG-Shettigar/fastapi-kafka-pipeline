from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.auth_service import verify_token

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = verify_token(token)
        return payload
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )