"""
Database configuration — SQLite + SQLAlchemy
Uses /tmp on Vercel (ephemeral), local file otherwise.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# On Vercel, filesystem is read-only except /tmp
IS_VERCEL = os.environ.get("VERCEL") == "1"

if IS_VERCEL:
    DB_PATH = "/tmp/inbox_executive.db"
else:
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inbox_executive.db")

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # needed for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency — yields a DB session and closes it after."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables."""
    from models import Email, Task, Suggestion, FollowUp  # noqa
    Base.metadata.create_all(bind=engine)
