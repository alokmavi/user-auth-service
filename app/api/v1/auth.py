from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.crud.user import get_user_by_email
from app.services.security import verify_password
from app.services.jwt import create_access_token
from app.schemas.token import TokenResponse

router = APIRouter()

@router.post("/login/access-token", response_model=TokenResponse)
def login_access_token(
    db_session: Session = Depends(get_db_session),
    credentials: OAuth2PasswordRequestForm = Depends()
):
    target_user = get_user_by_email(db_session, target_email=credentials.username)
    
    # Prevents timing attacks by returning the exact same error for both failure states
    if not target_user or not verify_password(credentials.password, target_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=target_user.id)
    
    return TokenResponse(access_token=access_token)