from pydantic import BaseModel
from typing import Optional


class Student(BaseModel):
    usn: Optional[str]
    name: Optional[str]
    branch: Optional[str]
    semester: Optional[int]
    cgpa: Optional[float]

    class ConfigDict:
        from_attributs = True


class StudentResponse(BaseModel):
    usn: str
    name: str
    branch: str
    semester: int
    cgpa: float

    class ConfigDict:
        from_attributs = True
