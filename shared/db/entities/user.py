import datetime

from sqlalchemy import Column, Integer, Text, event

from shared.db.base_engine import Base


class User(Base):
    __tablename__ = 'users'
    id: int = Column(Integer, primary_key=True, index=True)
    name: int = Column(Text, nullable=False, unique=False)
    email: int = Column(Text, nullable=False, unique=False)


@event.listens_for(User, 'before_insert')
def update_created_at(mapper, connection, target):
    target.createdAt = datetime.datetime.utcnow()
    target.updatedAt = datetime.datetime.utcnow()


@event.listens_for(User, 'before_update')
def update_updated_at(mapper, connection, target):
    target.updatedAt = datetime.datetime.utcnow()
