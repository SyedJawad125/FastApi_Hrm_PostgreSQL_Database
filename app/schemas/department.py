from typing import Optional, List
from pydantic import BaseModel

# (Already defined)
class DepartmentBase(BaseModel):
    name: str
    location: Optional[str] = None  # Add location if needed

class DepartmentCreate(DepartmentBase):
    class Config:
        extra = "forbid"

class Department(DepartmentBase):
    id: int
    created_by_user_id: Optional[int] = None

    class Config:
        from_attributes = True

# ✅ Add this for paginated data
class PaginatedDepartments(BaseModel):
    count: int
    data: List[Department]

# ✅ Add this for final API response
class DepartmentListResponse(BaseModel):
    status: str
    result: PaginatedDepartments

# schemas/department.py

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None

    class Config:
        extra = "forbid"
