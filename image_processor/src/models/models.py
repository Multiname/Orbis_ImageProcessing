from injectors.init_db import engine

from sqlalchemy import Column, Integer, String, Enum, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum


Base = declarative_base()


class Status(enum.StrEnum):
    pending = "pending"
    processing = "processing"
    finished = "finished"
    error = "error"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer(), primary_key=True)
    source_id = Column(Integer(), nullable=False)
    result_id = Column(Integer(), nullable=True)
    status = Column(Enum(Status), nullable=False, default=Status.pending)
    algorithm = Column(String(), nullable=False)
    params = Column(JSON(), nullable=True)
    created_at = Column(DateTime(), nullable=False, default=datetime.now())
    updated_at = Column(DateTime(), nullable=True)


Base.metadata.create_all(engine)
