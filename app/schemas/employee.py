from pydantic import BaseModel, EmailStr
from datetime import date
from typing import List, Optional

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    hire_date: date
    job_title: str
    salary: float
    department_id: int
    rank_id: Optional[int] = None  # ✅ Allow rank_id to be nullable

class EmployeeCreate(EmployeeBase):
   class Config:
        extra = "forbid"


class Employee(EmployeeBase):
    id: int
    
    class Config:
        from_attributes = True  # Previously called orm_mode in Pydantic v1

class PaginatedEmployees(BaseModel):
    count: int
    data: List[Employee]

# ✅ Add this for final API response
class EmployeeListResponse(BaseModel):
    status: str
    result: PaginatedEmployees

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    hire_date: Optional[date] = None
    job_title: Optional[str] = None
    salary: Optional[float] = None
    department_id: Optional[int] = None
    rank_id: Optional[int] = None

    class Config:
        extra = "forbid"