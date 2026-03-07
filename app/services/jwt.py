from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import app_settings

def create_access_token(subject: str | int) -> str:
    # Use UTC to prevent timezone drifting bugs across distributed servers
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=app_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    jwt_payload = {
        "sub": str(subject),
        "exp": expire_time
    }
    
    encoded_jwt = jwt.encode(
        jwt_payload, 
        app_settings.SECRET_KEY, 
        algorithm=app_settings.ALGORITHM
    )
    
    return encoded_jwt