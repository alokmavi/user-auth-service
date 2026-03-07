from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserRead
from app.crud.user import create_user, get_user_by_email
from app.api.deps import get_db_session, get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_new_user(
    user_registration: UserCreate,
    db_session: Session = Depends(get_db_session)
):
    existing_user = get_user_by_email(db_session, target_email=user_registration.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists."
        )
    
    try:
        created_user = create_user(db_session, user_creation_request=user_registration)
        return created_user
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

@router.get("/me", response_model=UserRead)
def read_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user