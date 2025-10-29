from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg2://user:secret@localhost:5432/CodeCamp"

engine = create_engine(DATABASE_URL, echo=True)  # echo=True prints SQL queries
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def get_session():
    """Yield a SQLAlchemy session (use with context manager)"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
