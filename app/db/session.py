from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import app_settings

db_engine = create_engine(
    app_settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)