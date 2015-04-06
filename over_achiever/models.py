from datetime import datetime
from sqlalchemy import (Column,
                        DateTime,
                        ForeignKey,
                        Integer,
                        String)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    email = Column(String(120), index=True, unique=True)
    password = Column(String(128))


class Goal(Base):
    __tablename__ = 'goal'
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    parent_id = Column(ForeignKey('goal.id'))
    name = Column(String(64), unique=True)
    description = Column(String(512))
    start = Column(DateTime, default=datetime.now)
    end = Column(DateTime, nullable=True)

    user = relationship('User')
    parent = relationship(lambda: Goal,
                          remote_side=id,
                          backref='sub_goals')
