# python_backend/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# ============================================================
# DATABASE URL
# ============================================================

# Priority:
# 1. Railway / Docker / Production: DATABASE_URL env var
# 2. Local development: SQLite fallback
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# ============================================================
# SQLALCHEMY ENGINE
# ============================================================

# SQLite requires special connect args
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    echo=False,          # Set to True for SQL debugging
    future=True,
    connect_args=connect_args
)

# ============================================================
# SESSION FACTORY
# ============================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

# ============================================================
# BASE MODEL
# ============================================================

Base = declarative_base()

# ============================================================
# FASTAPI DEPENDENCY
# ============================================================

def get_db():
    """
    FastAPI dependency that yields a database session.
    Ensures proper cleanup after each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================================
# OPTIONAL: AUTO-CREATE TABLES (if not using Alembic)
# ============================================================

def init_db():
    """
    Creates all tables automatically.
    Call this from main.py after all models are imported.
    """
    Base.metadata.create_all(bind=engine)
