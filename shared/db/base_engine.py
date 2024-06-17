import os
from sqlalchemy.orm import  declarative_base

from api.config.config import settings

Base = declarative_base()

SQLALCHEMY_DATABASE_URI = settings.database.SQLALCHEMY_DATABASE_URI

SQLALCHEMY_DATABASE_SYNC_URI = settings.database.SQLALCHEMY_DATABASE_SYNC_URI



