from fastapi import APIRouter, status, Depends
from googleapiclient import schema
from ..schemas import schemas
from ..repositories import database
from sqlalchemy.orm import Session
from ..db_config import get_db
from typing import List
import sched

router = APIRouter(tags=["Database"], prefix="/database")


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.StudentResponse,
)
def create_record(request: schemas.Student, db: Session = Depends(get_db)):
    return database.insert_record(request, db)


@router.get(
    "/read/{usn}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.StudentResponse,
)
def read_record(usn: str, db: Session = Depends(get_db)):
    return database.read_single_record(usn, db)


@router.get(
    "/readall",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Student],
)
def read_database(db: Session = Depends(get_db)):
    return database.read_all_records(db)


@router.put(
    "/update/{usn}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.Student,
)
def update_record(
    usn: str,
    request: schemas.Student,
    db: Session = Depends(get_db),
):
    return database.update_single_record(usn, request, db)


@router.patch(
    "/updatepartial/{usn}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.Student,
)
def update_record_partial(
    usn: str, request: schemas.Student, db: Session = Depends(get_db)
):
    return database.update_single_record_partial(usn, request, db)


@router.delete(
    "/delete/{usn}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_record(usn: str, db: Session = Depends(get_db)):
    return database.delete_single_record(usn, db)
