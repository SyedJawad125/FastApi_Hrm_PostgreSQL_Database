from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Any

from app.dependencies.permission import permission_required, require
from app.models.attendance import Attendance
from .. import database, schemas, models, oauth2
from app.utils import paginate_data, create_response, filter_attendances
from fastapi.responses import JSONResponse
# from app.schemas import DepartmentListResponse


router = APIRouter(
    prefix="/attendances",
    tags=['Attendances']
)

# @router.get("/", response_model=List[schemas.Department])

# @router.get("/", response_model=Any)
@router.get("/", response_model=schemas.AttendanceListResponse)
def get_attendances(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    try:
        query = db.query(models.Attendance)
        query = filter_attendances(request.query_params, query)
        data = query.all()

        # You might want to paginate using the DB query itself for performance.
        paginated_data, count = paginate_data(data, request)

        serialized_data = [schemas.Attendance.from_orm(attend) for attend in paginated_data]

        return {
            "status": "SUCCESSFUL",
            "result": {
                "count": count,
                "data": serialized_data
            }
        }

    except HTTPException as http_err:
        raise http_err  # Re-raise known HTTP errors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Attendance)
# @router.post("/", status_code=status.HTTP_201_CREATED)
def create_attendance(
    attendance: schemas.AttendanceCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:

        attendance_data = attendance.dict()
        # attendance_data["created_by_user_id"] = current_user.id  # ✅ Correct field name

        new_attendance = models.Attendance(**attendance_data)
        db.add(new_attendance)
        db.commit()
        db.refresh(new_attendance)

        return new_attendance

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/{id}", response_model=schemas.Attendance)
def get_attendance(
    id: int, 
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(oauth2.get_current_user)
):
    attendance = db.query(models.Attendance).filter(models.Attendance.id == id).first()
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attendance with id {id} not found"
        )
    return attendance


@router.patch("/{id}", response_model=schemas.Attendance)
def patch_update_attendance(
    id: int,
    updated_attendance: schemas.AttendanceUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:

        attendance_instance = db.query(models.Attendance).filter(models.Attendance.id == id).first()

        if not attendance_instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Attendance with id {id} not found"
            )

        update_data = updated_attendance.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(attendance_instance, key, value)

        db.commit()
        db.refresh(attendance_instance)

        return attendance_instance

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while patching the attendance: {str(e)}"
        )


# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_attendance(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
    # _: None = Depends(permission_required(["delete_department"]))
):
    attendance_query = db.query(models.Attendance).filter(models.Attendance.id == id)
    attendance = attendance_query.first()

    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attendance with id {id} not found"
        )

    attendance_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Attendance deleted successfully"}
