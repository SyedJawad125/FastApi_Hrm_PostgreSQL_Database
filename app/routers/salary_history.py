from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any
from .. import database, schemas, models, oauth2
from app.utils import paginate_data

router = APIRouter(
    prefix="/salary-histories",
    tags=["Salary History"]
)

# ✅ GET ALL
@router.get("/", response_model=schemas.SalaryHistoryListResponse)
def get_salary_histories(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.SalaryHistory)
        data = query.all()
        paginated_data, count = paginate_data(data, request)
        serialized_data = [schemas.SalaryHistoryOut.from_orm(item) for item in paginated_data]

        return {
            "status": "SUCCESSFUL",
            "result": {"count": count, "data": serialized_data}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ CREATE
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.SalaryHistoryOut)
def create_salary_history(
    salary_history: schemas.SalaryHistoryCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        data = salary_history.dict()
        data["created_by_user_id"] = current_user.id

        new_history = models.SalaryHistory(**data)
        db.add(new_history)
        db.commit()
        db.refresh(new_history)

        return new_history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ GET BY ID
@router.get("/{id}", response_model=schemas.SalaryHistoryOut)
def get_salary_history(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    history = db.query(models.SalaryHistory).filter(models.SalaryHistory.id == id).first()
    if not history:
        raise HTTPException(status_code=404, detail=f"SalaryHistory with id {id} not found")
    return history


# ✅ PATCH UPDATE
@router.patch("/{id}", response_model=schemas.SalaryHistoryOut)
def update_salary_history(
    id: int,
    update_data: schemas.SalaryHistoryUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        history = db.query(models.SalaryHistory).filter(models.SalaryHistory.id == id).first()
        if not history:
            raise HTTPException(status_code=404, detail=f"SalaryHistory with id {id} not found")

        updates = update_data.dict(exclude_unset=True)
        for key, value in updates.items():
            setattr(history, key, value)

        db.commit()
        db.refresh(history)

        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")


# ✅ DELETE
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_salary_history(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    query = db.query(models.SalaryHistory).filter(models.SalaryHistory.id == id)
    record = query.first()

    if not record:
        raise HTTPException(status_code=404, detail=f"SalaryHistory with id {id} not found")

    query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Salary history deleted successfully"}
