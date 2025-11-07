"""
Database initialization and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from kosmos.db.models import Base
import logging
from typing import Generator


logger = logging.getLogger(__name__)


# Global engine and session factory
_engine = None
_SessionLocal = None


def init_database(database_url: str, echo: bool = False):
    """
    Initialize database engine and create tables.

    Args:
        database_url: SQLAlchemy database URL
        echo: Whether to echo SQL statements

    Example:
        ```python
        from kosmos.db import init_database

        init_database("sqlite:///kosmos.db")
        ```
    """
    global _engine, _SessionLocal

    logger.info(f"Initializing database: {database_url}")

    _engine = create_engine(database_url, echo=echo)
    _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

    # Create all tables
    Base.metadata.create_all(bind=_engine)

    logger.info("Database initialized successfully")


def get_session() -> Generator[Session, None, None]:
    """
    Get database session (context manager).

    Yields:
        Session: SQLAlchemy session

    Example:
        ```python
        from kosmos.db import get_session
        from kosmos.db.models import Hypothesis

        with get_session() as session:
            hypothesis = session.query(Hypothesis).first()
            print(hypothesis.statement)
        ```
    """
    if _SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")

    session = _SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_from_config():
    """
    Initialize database from Kosmos configuration.

    Example:
        ```python
        from kosmos.config import get_config
        from kosmos.db import init_from_config

        init_from_config()
        ```
    """
    from kosmos.config import get_config

    config = get_config()
    init_database(
        database_url=config.database.url,
        echo=config.database.echo
    )
