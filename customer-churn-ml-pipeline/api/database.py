# Import SQLAlchemy
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Database connection
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./churn_local.db"
)

# SQLite configuration
connect_args = (
    {"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)

# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)

# Create database session
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# Base class for database models
class Base(DeclarativeBase):
    pass


# Database dependency
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()