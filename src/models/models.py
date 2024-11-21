from ..db_config import Base
from sqlalchemy import Column, Integer, String, Float


class Student(Base):
    __tablename__ = "students"

    usn = Column(String, primary_key=True, index=True)
    name = Column(String)
    branch = Column(String)
    semester = Column(Integer)
    cgpa = Column(Float)
