from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import app_settings
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.token import TokenPayload
from app.crud.user import get_user_by_email # We will need to query by ID ideally, but let's write a get_user function.

# Tell FastAPI where the client should go to get the token
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{app_settings.API_V1_STR}/login/access-token"
)

def get_db_session() -> Generator:
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

def get_current_user(
    db_session: Session = Depends(get_db_session),
    token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, app_settings.SECRET_KEY, algorithms=[app_settings.ALGORITHM]
        )
        # Validate the extracted payload against our Pydantic schema
        token_data = TokenPayload(subject=str(payload.get("sub")))
    except (JWTError, ValidationError):
        raise credentials_exception
        
    # Query the database to ensure the user still exists and hasn't been deleted
    user_record = db_session.query(User).filter(User.id == int(token_data.subject)).first()
    
    if not user_record:
        raise credentials_exception
        
    return user_record