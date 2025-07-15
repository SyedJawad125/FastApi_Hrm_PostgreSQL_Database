from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Any

from app.dependencies.permission import permission_required, require
from .. import database, schemas, models, oauth2
from app.utils import paginate_data, create_response, filter_timesheets
from fastapi.responses import JSONResponse



router = APIRouter(
    prefix="/timesheets",
    tags=['Timesheets']
)

# @router.get("/", response_model=List[schemas.Timesheet])

# @router.get("/", response_model=Any)
@router.get("/", response_model=schemas.TimesheetListResponse)
def get_timesheets(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    try:
        query = db.query(models.Timesheet)
        query = filter_timesheets(request.query_params, query)
        data = query.all()

        # Optional: You should paginate at the DB level for better performance
        paginated_data, count = paginate_data(data, request)

        # Convert ORM objects to Pydantic
        serialized_data = [schemas.Timesheet.from_orm(time) for time in paginated_data]

        return {
            "status": "SUCCESSFUL",
            "result": {
                "count": count,
                "data": serialized_data
            }
        }

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Timesheet)
# @router.post("/", status_code=status.HTTP_201_CREATED)
def create_timesheet(
    timesheet: schemas.TimesheetCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:

        timesheet_data = timesheet.dict()
        # timesheet_data["created_by_user_id"] = current_user.id  # ✅ Correct field name

        new_timesheet = models.Timesheet(**timesheet_data)
        db.add(new_timesheet)
        db.commit()
        db.refresh(new_timesheet)

        
        return new_timesheet

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/{id}", response_model=schemas.Timesheet)
def get_timesheet(id: int, db: Session = Depends(database.get_db), 
                  current_user: models.User = Depends(oauth2.get_current_user)):
    timesheet = db.query(models.Timesheet).filter(models.Timesheet.id == id).first()
    if not timesheet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"Timesheet with id {id} not found")
    return timesheet

@router.patch("/{id}", response_model=schemas.Timesheet)
def patch_update_timesheet(
    id: int,
    updated_timesheet: schemas.TimesheetUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:

        timesheet_instance = db.query(models.Timesheet).filter(models.Timesheet.id == id).first()

        if not timesheet_instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Timesheet with id {id} not found"
            )

        update_data = updated_timesheet.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(timesheet_instance, key, value)

        db.commit()
        db.refresh(timesheet_instance)

        return timesheet_instance

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while patching the timesheet: {str(e)}"
        )


# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_timesheet(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
    # _: None = Depends(permission_required(["delete_department"]))
):
    timesheet_query = db.query(models.Timesheet).filter(models.Timesheet.id == id)
    timesheet = timesheet_query.first()

    if not timesheet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Timesheet with id {id} not found"
        )

    timesheet_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Timesheet deleted successfully"}
