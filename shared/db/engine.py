import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shared.db.base_engine import SQLALCHEMY_DATABASE_SYNC_URI


def get_session() -> sessionmaker:
    """
    Creates a new SQLAlchemy session maker object.

    This function returns a session maker object that can be used to create
    new database sessions for non-async operations in your Python application.

    Returns:
        sessionmaker: A session maker object.
    """

    # Configure your database engine here (replace with your actual configuration)

    engine = create_engine(
        SQLALCHEMY_DATABASE_SYNC_URI,
        pool_recycle=1,
        pool_pre_ping=True,
        echo=os.getenv('DEBUG_SQL') == 'TRUE',
        pool_size=100,
        max_overflow=200,
    )

    Session = sessionmaker(bind=engine,
                           expire_on_commit=False,
                           autocommit=False,
                           autoflush=False,
                           )
    session = Session()

    return session
