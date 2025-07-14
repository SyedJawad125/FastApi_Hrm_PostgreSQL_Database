from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any

from app.dependencies.permission import permission_required, require
from .. import database, schemas, models, oauth2
from app.utils import paginate_data, filter_leave
from app.schemas.leave import LeaveList, LeaveStatus,MyLeaveListResponse, GetAllLeaveListResponse, LeaveType, CreateLeaveResponse
from datetime import datetime
router = APIRouter(
    prefix="/leaves",
    tags=['Leaves']
)


from sqlalchemy.orm import joinedload

@router.get("/", response_model=schemas.GetAllLeaveListResponse, dependencies=[require("read_leave")])
def get_leaves(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    try:
        # ✅ Load approved_by and their role in one query
        query = db.query(models.Leave).options(
            joinedload(models.Leave.approved_by).joinedload(models.User.role)
        )

        # Apply filters
        query = filter_leave(dict(request.query_params), query)

        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)

        # Serialize using Pydantic
        serialized_data = [schemas.LeaveList.from_orm(leave) for leave in paginated_data]

        return {
            "count": count,
            "data": serialized_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ POST: Create Leave
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CreateLeaveResponse, dependencies=[require("create_leave")])
def create_leave(
    leave_data: schemas.LeaveCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        if leave_data.start_date >= leave_data.end_date:
            raise HTTPException(status_code=400, detail="End date must be after start date")

        new_leave = models.Leave(
            **leave_data.model_dump(),
            employee_id=current_user.id
        )

        db.add(new_leave)
        db.commit()
        db.refresh(new_leave)

        return new_leave

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/my-leaves", response_model=MyLeaveListResponse, dependencies=[require("read_leave")])
def get_my_leaves(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.Leave).filter(models.Leave.employee_id == current_user.id)
        query = filter_leave(dict(request.query_params), query)


        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)

        serialized_data = [schemas.LeaveList.model_validate(leave) for leave in paginated_data]

        return {
            "status": "SUCCESSFUL",
            "result": {
                "count": count,
                "data": serialized_data
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ GET: Single Leave by ID
@router.get("/{id}", response_model=schemas.LeaveResponse, dependencies=[require("read_leave")])
def get_leave(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    leave = db.query(models.Leave).filter(models.Leave.id == id).first()

    if not leave:
        raise HTTPException(status_code=404, detail=f"Leave with id {id} not found")

    return leave


# from fastapi import BackgroundTasks
# from app.utils import send_email_notification
# import os

# @router.patch("/{id}", response_model=schemas.LeaveResponse, dependencies=[require("update_leave")])
# def update_leave(
#     id: int,
#     updated_data: schemas.LeaveUpdate,
#     background_tasks: BackgroundTasks,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user),
# ):
#     try:
#         leave = db.query(models.Leave).filter(models.Leave.id == id).first()

#         if not leave:
#             raise HTTPException(status_code=404, detail=f"Leave with ID {id} not found")

#         if LeaveStatus(leave.status) != LeaveStatus.PENDING:
#             raise HTTPException(status_code=400, detail="Only pending leaves can be updated")

#         update_values = updated_data.model_dump(exclude_unset=True)
#         update_values['approved_by_id'] = current_user.id
#         update_values['updated_at'] = datetime.utcnow()

#         for key, value in update_values.items():
#             setattr(leave, key, value)

#         # Create notification for the employee
#         employee_notification = models.Notification(
#             title="Leave Request Updated",
#             message=f"Your leave request has been {leave.status.upper()}.",
#             user_id=leave.employee_id,
#             leave_id=leave.id,
#             created_by_id=current_user.id
#         )
#         db.add(employee_notification)

        
#         admin_users = db.query(models.User).join(
#             models.Role,
#             models.User.role_id == models.Role.id
#         ).filter(
#             models.Role.name.in_(["HR Manager", "Admin", "Super Admin"])
#         ).all()


#         for admin in admin_users:
#             admin_notification = models.Notification(
#                 title="Leave Request Review",
#                 message=(
#                     f"Manager {current_user.username} has {leave.status.upper()} a leave request.\n"
#                     f"Employee ID: {leave.employee_id}\n"
#                     f"Leave Type: {leave.leave_type}\n"
#                     f"From: {leave.start_date.strftime('%Y-%m-%d')} To: {leave.end_date.strftime('%Y-%m-%d')}"
#                 ),
#                 user_id=admin.id,
#                 leave_id=leave.id,
#                 created_by_id=current_user.id
#             )
#             db.add(admin_notification)

#         db.commit()
#         db.refresh(leave)

#         # Send email notifications in background
#         if leave.employee and leave.employee.email:
#             background_tasks.add_task(
#                 send_email_notification,
#                 to_email=leave.employee.email,
#                 subject="Leave Request Status Updated",
#                 message=f"Your leave request has been {leave.status.upper()}."
#             )

#         # Notify admin or HR (email from env or hardcoded)
#         admin_email = os.getenv("ADMIN_EMAIL", "admin_hr@example.com")
#         admin_message = (
#             f"Manager {current_user.username} has {leave.status.upper()} a leave request.\n"
#             f"Employee ID: {leave.employee_id}\n"
#             f"Leave Type: {leave.leave_type}\n"
#             f"From: {leave.start_date.strftime('%Y-%m-%d')} To: {leave.end_date.strftime('%Y-%m-%d')}"
#         )

#         background_tasks.add_task(
#             send_email_notification,
#             to_email=admin_email,
#             subject="Leave Request Reviewed",
#             message=admin_message
#         )

#         return leave

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error updating leave: {str(e)}")


from fastapi import HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app import models, schemas, database, oauth2
from app.utils import send_email_notification
from app.schemas.leave import LeaveStatus
from app.dependencies.permission import require
from app.utils import log_action  # ✅ NEW
from datetime import datetime
import os

@router.patch("/{id}", response_model=schemas.LeaveResponse, dependencies=[require("update_leave")])
def update_leave(
    id: int,
    updated_data: schemas.LeaveUpdate,
    background_tasks: BackgroundTasks,  # Add this back
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    try:
        leave = db.query(models.Leave).filter(models.Leave.id == id).first()

        if not leave:
            raise HTTPException(status_code=404, detail=f"Leave with ID {id} not found")

        if LeaveStatus(leave.status) != LeaveStatus.PENDING:
            raise HTTPException(status_code=400, detail="Only pending leaves can be updated")

        update_values = updated_data.model_dump(exclude_unset=True)
        update_values['approved_by_id'] = current_user.id
        update_values['updated_at'] = datetime.utcnow()

        for key, value in update_values.items():
            setattr(leave, key, value)

        # Add notifications
        db.add(models.Notification(
            title="Leave Request Updated",
            message=f"Your leave request has been {leave.status.upper()}.",
            user_id=leave.employee_id,
            leave_id=leave.id,
            created_by_id=current_user.id
        ))

        admin_users = db.query(models.User).join(
            models.Role, models.User.role_id == models.Role.id
        ).filter(
            models.Role.name.in_(["HR Manager", "Admin", "Super Admin"])
        ).all()

        for admin in admin_users:
            db.add(models.Notification(
                title="Leave Request Reviewed",
                message=(
                    f"{current_user.username} has {leave.status.upper()} a leave request.\n"
                    f"Employee ID: {leave.employee_id}\n"
                    f"Leave Type: {leave.leave_type}\n"
                    f"From: {leave.start_date.strftime('%Y-%m-%d')} To: {leave.end_date.strftime('%Y-%m-%d')}"
                ),
                user_id=admin.id,
                leave_id=leave.id,
                created_by_id=current_user.id
            ))

        db.commit()
        db.refresh(leave)

        # Send email notifications in background
        if leave.employee and leave.employee.email:
            background_tasks.add_task(
                send_email_notification,
                to_email=leave.employee.email,
                subject="Leave Request Status Updated",
                message=f"Your leave request has been {leave.status.upper()}."
            )

        admin_email = os.getenv("ADMIN_EMAIL", "admin_hr@example.com")
        admin_message = (
            f"Manager {current_user.username} has {leave.status.upper()} a leave request.\n"
            f"Employee ID: {leave.employee_id}\n"
            f"Leave Type: {leave.leave_type}\n"
            f"From: {leave.start_date.strftime('%Y-%m-%d')} To: {leave.end_date.strftime('%Y-%m-%d')}"
        )
        
        background_tasks.add_task(
            send_email_notification,
            to_email=admin_email,
            subject="Leave Request Reviewed",
            message=admin_message
        )
        # ✅ Logging in background
        log_msg = (
            f"User {current_user.username} ({current_user.id}) "
            f"{leave.status.upper()} leave ID {leave.id} for employee {leave.employee_id}"
        )
        background_tasks.add_task(log_action, log_msg)


        return leave
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating leave: {str(e)}")



# ✅ DELETE: Delete Leave
@router.delete("/{id}", status_code=200, dependencies=[require("delete_leave")])
def delete_leave(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    leave_query = db.query(models.Leave).filter(models.Leave.id == id)
    leave = leave_query.first()

    if not leave:
        raise HTTPException(status_code=404, detail=f"Leave with id {id} not found")

    if LeaveStatus(leave.status) != LeaveStatus.PENDING:
            raise HTTPException(status_code=400, detail="Only pending leaves can be deleted")
    leave_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Leave request deleted successfully"}


# Patch Api code for send Email to Employee Only

# from fastapi import BackgroundTasks
# from app.utils import send_email_notification

# @router.patch("/{id}", response_model=schemas.LeaveResponse, dependencies=[require("update_leave")])
# def update_leave(
#     id: int,
#     updated_data: schemas.LeaveUpdate,
#     background_tasks: BackgroundTasks,  # ✅ FIXED: Added missing comma
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user),
# ):
#     try:
#         leave = db.query(models.Leave).filter(models.Leave.id == id).first()

#         if not leave:
#             raise HTTPException(status_code=404, detail=f"Leave with ID {id} not found")

#         if LeaveStatus(leave.status) != LeaveStatus.PENDING:
#             raise HTTPException(status_code=400, detail="Only pending leaves can be updated")

#         update_values = updated_data.model_dump(exclude_unset=True)
#         update_values['approved_by_id'] = current_user.id
#         update_values['updated_at'] = datetime.utcnow()

#         for key, value in update_values.items():
#             setattr(leave, key, value)

#         db.commit()
#         db.refresh(leave)

#         # ✅ Send email notification in background
#         if leave.employee and leave.employee.email:
#             background_tasks.add_task(
#                 send_email_notification,
#                 to_email=leave.employee.email,
#                 subject="Leave Request Status Updated",
#                 message=f"Your leave request has been {leave.status.upper()}."
#             )

#         return leave

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error updating leave: {str(e)}")


# ✅ GET: All Leaves (with filtering & pagination)

# @router.get("/", response_model=schemas.LeaveListResponse, dependencies=[require("read_leave")])
# @router.get("/", response_model=schemas.LeaveListResponse, dependencies=[require("read_leave")])
# def get_leaves(
#     request: Request,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user),
# ):
#     try:
#         query = db.query(models.Leave)
#         # query = filter_leave(request.query_params, query)
#         query = filter_leave(dict(request.query_params), query)

#         all_data = query.all()
#         paginated_data, count = paginate_data(all_data, request)

#         # ✅ Use Pydantic model for serialization
#         serialized_data = [schemas.LeaveList.from_orm(leave) for leave in paginated_data]

       

#         return {
#             "count": count,
#             "data": serialized_data
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List
# from app.database import get_db
# from app.models import leave, user
# from app.schemas import leave as leave_schema
# from app.dependencies.get_current_user import get_current_user
# from app.dependencies.permission import has_permission
# from datetime import datetime

# router = APIRouter(
#     prefix="/leaves",
#     tags=["Leave Management"]
# )

# @router.post("/", response_model=leave_schema.LeaveResponse)
# def create_leave(
#     leave_request: leave_schema.LeaveCreate,
#     db: Session = Depends(get_db),
#     current_user: user.User = Depends(get_current_user)
# ):
#     # Validate dates
#     if leave_request.start_date >= leave_request.end_date:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="End date must be after start date"
#         )
    
#     if leave_request.start_date < datetime.now():
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Cannot create leave request for past dates"
#         )

#     new_leave = leave.Leave(
#         **leave_request.model_dump(),
#         employee_id=current_user.id
#     )
    
#     db.add(new_leave)
#     db.commit()
#     db.refresh(new_leave)
#     return new_leave

# @router.get("/", response_model=List[leave_schema.LeaveList])
# def get_leaves(
#     db: Session = Depends(get_db),
#     current_user: user.User = Depends(get_current_user),
#     _: bool = Depends(has_permission(["view_all_leaves"]))
# ):
#     leaves = db.query(leave.Leave).all()
#     return leaves

# @router.get("/my-leaves", response_model=List[leave_schema.LeaveList])
# def get_my_leaves(
#     db: Session = Depends(get_db),
#     current_user: user.User = Depends(get_current_user)
# ):
#     leaves = db.query(leave.Leave).filter(leave.Leave.employee_id == current_user.id).all()
#     return leaves

# @router.get("/{leave_id}", response_model=leave_schema.LeaveResponse)
# def get_leave(
#     leave_id: int,
#     db: Session = Depends(get_db),
#     current_user: user.User = Depends(get_current_user)
# ):
#     leave_request = db.query(leave.Leave).filter(leave.Leave.id == leave_id).first()
#     if not leave_request:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Leave with id {leave_id} not found"
#         )
    
#     # Check if user has permission to view this leave
#     if leave_request.employee_id != current_user.id and not any(perm.name == "view_all_leaves" for perm in current_user.permissions):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Not authorized to view this leave request"
#         )
    
#     return leave_request

# @router.patch("/{leave_id}/approve", response_model=leave_schema.LeaveResponse)
# def approve_leave(
#     leave_id: int,
#     leave_update: leave_schema.LeaveUpdate,
#     db: Session = Depends(get_db),
#     current_user: user.User = Depends(get_current_user),
#     _: bool = Depends(has_permission(["approve_leaves"]))
# ):
#     leave_request = db.query(leave.Leave).filter(leave.Leave.id == leave_id).first()
#     if not leave_request:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Leave with id {leave_id} not found"
#         )
    
#     if leave_request.status != "pending":
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Can only update pending leave requests"
#         )
    
#     for key, value in leave_update.model_dump(exclude_unset=True).items():
#         setattr(leave_request, key, value)
    
#     leave_request.approved_by_id = current_user.id
#     db.commit()
#     db.refresh(leave_request)
#     return leave_request

# @router.delete("/{leave_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_leave(
#     leave_id: int,
#     db: Session = Depends(get_db),
#     current_user: user.User = Depends(get_current_user)
# ):
#     leave_query = db.query(leave.Leave).filter(leave.Leave.id == leave_id)
#     leave_request = leave_query.first()
    
#     if not leave_request:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Leave with id {leave_id} not found"
#         )
    
#     if leave_request.employee_id != current_user.id:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Not authorized to delete this leave request"
#         )
    
#     if leave_request.status != "pending":
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Can only delete pending leave requests"
#         )
    
#     leave_query.delete(synchronize_session=False)
#     db.commit()
#     return None 