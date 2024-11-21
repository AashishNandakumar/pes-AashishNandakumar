from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from ..db_config import get_db
from ..models import models
from ..schemas import schemas


def insert_record(request: schemas.Student, db: Session = Depends(get_db)):
    try:
        new_record = models.Student(**request.dict())
        # print(new_record)

        db.add(new_record)
        db.commit()
        db.refresh(new_record)

        return new_record
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"error: {e}",
        )


def read_single_record(usn: str, db: Session = Depends(get_db)):
    try:
        record = db.query(models.Student).filter(models.Student.usn == usn).first()
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"record with usn `{usn}` not found!",
            )

        return record
    except Exception as e:
        raise e


def read_all_records(db: Session = Depends(get_db)):
    try:
        records = db.query(models.Student).all()
        if not records:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="no records found",
            )

        return records
    except Exception as e:
        raise e


def update_single_record(
    usn: str,
    request: schemas.Student,
    db: Session = Depends(get_db),
):
    try:
        record = db.query(models.Student).filter(models.Student.usn == usn).first()
        # print(record)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"record with usn `{usn}` not found!",
            )
        # record.update(dict(request))
        for key, value in request.dict().items():
            setattr(record, key, value)

        db.commit()
        db.refresh(record)
        return record
    except Exception as e:
        raise e


def update_single_record_partial(  # not proper implementation
    usn: str, request: schemas.Student, db: Session = Depends(get_db)
):
    try:
        record = db.query(models.Student).filter(models.Student.usn == usn).first()
        # print(record)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"record with usn `{usn}` not found!",
            )
        # record.update(dict(request))
        for key, value in request.dict().items():
            if value:
                setattr(record, key, value)

        db.commit()
        db.refresh(record)
        return record
    except Exception as e:
        raise e


def delete_single_record(usn: str, db: Session = Depends(get_db)):
    try:
        record = db.query(models.Student).filter(models.Student.usn == usn)
        print("to be deleted: ", record)
        if not record.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"record with usn `{usn}` not found!",
            )
        record.delete(synchronize_session=False)
        db.commit()
        return "succesfully deleted"
    except Exception as e:
        raise e
