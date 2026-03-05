from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.security import get_password_hash

def get_user_by_email(db_session: Session, target_email: str) -> User | None:
    return db_session.query(User).filter(User.email == target_email).first()

def create_user(db_session: Session, user_creation_request: UserCreate) -> User:
    hashed_pwd = get_password_hash(user_creation_request.password)
    
    new_user = User(
        email=user_creation_request.email,
        full_name=user_creation_request.full_name,
        hashed_password=hashed_pwd
    )
    
    try:
        db_session.add(new_user)
        # Flush the transaction to the database to catch constraint violations
        db_session.commit()
        # Refresh the instance to get the auto-generated ID from Postgres
        db_session.refresh(new_user)
        return new_user
    
    except IntegrityError:
        # If the email already exists, Postgres throws an IntegrityError.
        # We must rollback the session so future queries in this request don't fail.
        db_session.rollback()
        raise ValueError("A user with this email already exists.")