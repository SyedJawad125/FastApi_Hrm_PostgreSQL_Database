from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum

class LeaveStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class LeaveType(str, Enum):
    ANNUAL = "annual"
    SICK = "sick"
    MATERNITY = "maternity"
    PATERNITY = "paternity"
    UNPAID = "unpaid"
    OTHER = "other"

class LeaveBase(BaseModel):
    start_date: datetime
    end_date: datetime
    leave_type: LeaveType
    reason: str

class LeaveCreate(LeaveBase):
    pass

class LeaveUpdate(BaseModel):
    status: LeaveStatus
    approved_by_id: Optional[int] = None


class CreateLeaveResponse(LeaveBase):
    id: int
    status: LeaveStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    employee_id: int
   

    class Config:
        from_attributes = True
class Role1(BaseModel):
    id: int
    name: str  # adjust this field based on your actual Role model

    class Config:
        from_attributes = True

class Approver1(BaseModel):
    id: int
    username: str
    role: Optional[Role1] = None  # ✅ Nested role object

    class Config:
        from_attributes = True

class LeaveResponse(LeaveBase):
    id: int
    status: LeaveStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    employee_id: int
    # approved_by_id: Optional[int] = None
    approved_by: Optional[Approver1] = None  # Nested object

    class Config:
        from_attributes = True


class Role(BaseModel):
    id: int
    name: str  # adjust this field based on your actual Role model

    class Config:
        from_attributes = True

class Approver(BaseModel):
    id: int
    username: str  # Or "name", depending on your User model
    role: Optional[Role] = None  # ✅ Nested role object


    class Config:
        from_attributes = True

class LeaveList(BaseModel):
    id: int
    start_date: datetime
    end_date: datetime
    leave_type: LeaveType
    status: LeaveStatus
    employee_id: int
    # approved_by_id: Optional[int] = None
    approved_by: Optional[Approver] = None  # ✅ Add this line to show approver's name

    class Config:
        from_attributes = True

class GetAllLeaveListResponse(BaseModel):
    count: int
    data: list[LeaveList]


class LeaveListResult(BaseModel):
    count: int
    data: list[LeaveList]

    class Config:
        from_attributes = True


class MyLeaveListResponse(BaseModel):
    status: str
    result: LeaveListResult
