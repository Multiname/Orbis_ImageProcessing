from app import app, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime


Base = declarative_base()


class FileInfo(Base):
    __tablename__ = "files_info"

    id = Column(Integer(), primary_key=True)
    name = Column(String(255), nullable=False)
    extension = Column(String(10), nullable=False)
    size = Column(Integer(), nullable=False)
    path = Column(String(), nullable=False)
    created_at = Column(DateTime(), nullable=False, default=datetime.now)
    updated_at = Column(DateTime(), nullable=True)
    comment = Column(String(300), nullable=True)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.name)


Base.metadata.create_all(engine)
