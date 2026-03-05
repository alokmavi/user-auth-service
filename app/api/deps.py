from typing import Generator
from app.db.session import SessionLocal

def get_db_session() -> Generator:
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()