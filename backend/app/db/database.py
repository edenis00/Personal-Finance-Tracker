"""
Database setup and session management
"""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import Pool
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True

)


@event.listens_for(Pool, "connect")
def on_connect(dbapi_connection, connection_record):
    """
    Event listener for new database connections
    """
    logger.info("New database connection established.")


@event.listens_for(Pool, "checkout")
def on_checkout(dbapi_connection, connection_record, connection_proxy):
    """
    Event listener for checking out a database connection from the pool
    """
    logger.info("Database connection checked out from pool.")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db_context():
    """
    Context manager for database sessions
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logging.error(f"Database transaction failed: {str(e)}")
        raise
    finally:
        db.close()



def get_db():
    """
    Dependency to get DB session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()