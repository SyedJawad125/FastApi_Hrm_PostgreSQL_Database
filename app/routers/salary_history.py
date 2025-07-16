from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any
from .. import database, schemas, models, oauth2
from app.utils import filter_salary_histories, paginate_data, get_object_or_404
from fastapi import Body


router = APIRouter(
    prefix="/salary-histories",
    tags=["Salary History"]
)

# ✅ GET ALL
@router.get("/", response_model=schemas.SalaryHistoryListResponse)
def get_salary_histories(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    try:
        query = db.query(models.SalaryHistory)

        # ✅ Apply filtering from query params (e.g., ?employee_id=1&department_id=2)
        query = filter_salary_histories(request.query_params, query)

        data = query.all()
        paginated_data, count = paginate_data(data, request)

        serialized_data = [schemas.SalaryHistoryOut.from_orm(item) for item in paginated_data]

        return {
            "status": "SUCCESSFUL",
            "result": {
                "count": count,
                "data": serialized_data
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving salary histories: {str(e)}")



# ✅ CREATE
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.SalaryHistoryOut)
def create_salary_history(
    salary_history: schemas.SalaryHistoryCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        # Extract input data
        data = salary_history.dict()

        # Auto-calculate change_percentage if not provided
        previous = data["previous_salary"]
        new = data["new_salary"]

        if previous == 0:
            raise HTTPException(status_code=400, detail="Previous salary cannot be zero.")

        data["change_percentage"] = round(((new - previous) / previous) * 100, 2)

        # Add creator ID from authenticated user
        data["created_by_user_id"] = current_user.id

        # Create and store the record
        new_history = models.SalaryHistory(**data)
        db.add(new_history)
        db.commit()
        db.refresh(new_history)

        return new_history

    except HTTPException:
        raise  # Reraise expected exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating salary history: {str(e)}")


# ✅ GET BY ID
@router.get("/{id}", response_model=schemas.SalaryHistoryOut)
def get_salary_history(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    history = get_object_or_404(db.query(models.SalaryHistory), id, "SalaryHistory")
    return history


# ✅ PATCH UPDATE
@router.patch("/{id}", response_model=schemas.SalaryHistoryOut)
def update_salary_history(
    id: int,
    update_data: schemas.SalaryHistoryUpdate = Body(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        history = get_object_or_404(db.query(models.SalaryHistory), id, "SalaryHistory")

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
    query = db.query(models.SalaryHistory)
    history = get_object_or_404(query, id, "SalaryHistory")

    query.filter_by(id=id).delete(synchronize_session=False)
    db.commit()

    return {"message": "Salary history deleted successfully"}
