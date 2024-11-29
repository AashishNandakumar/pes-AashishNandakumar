from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime

Base = declarative_base()


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)
    last_modified = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )  # for conflict resolution
