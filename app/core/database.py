"""
Database session management using SQLAlchemy.
"""
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.
    
    Yields:
        Session: SQLAlchemy database session
        
    Example:
        ```python
        @app.get("/stations")
        def get_stations(db: Session = Depends(get_db)):
            return db.query(Station).all()
        ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
