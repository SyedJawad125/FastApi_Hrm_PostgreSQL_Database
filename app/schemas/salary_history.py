from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from enum import Enum


# ✅ Enum for change_type
class ChangeType(str, Enum):
    PROMOTION = "promotion"
    ANNUAL_RAISE = "annual_raise"
    PERFORMANCE_RAISE = "performance_raise"
    ADJUSTMENT = "adjustment"
    DEMOTION = "demotion"
    OTHER = "other"


# ✅ Minimal user schema for creator info
class UserOut(BaseModel):
    id: int
    username: str  # Adjust if you're using "email" or "name" instead

    class Config:
        orm_mode = True


# ✅ Shared base class
class SalaryHistoryBase(BaseModel):
    previous_salary: float
    new_salary: float
    change_percentage: float
    change_type: ChangeType
    change_reason: Optional[str] = None
    effective_date: date

    employee_id: int
    previous_rank_id: int
    new_rank_id: int
    department_id: int
    salary_structure_id: Optional[int] = None
    employee_salary_id: Optional[int] = None


# ✅ Create schema
class SalaryHistoryCreate(SalaryHistoryBase):
    pass


# ✅ Update schema
class SalaryHistoryUpdate(BaseModel):
    previous_salary: Optional[float]
    new_salary: Optional[float]
    change_percentage: Optional[float]
    change_type: Optional[ChangeType]
    change_reason: Optional[str]
    effective_date: Optional[date]
    previous_rank_id: Optional[int]
    new_rank_id: Optional[int]
    department_id: Optional[int]
    salary_structure_id: Optional[int]
    employee_salary_id: Optional[int]

    class Config:
        orm_mode = True


# ✅ Output schema for GET (includes creator info)
class SalaryHistoryOut(SalaryHistoryBase):
    id: int
    created_at: datetime
    creator: Optional[UserOut]  # 👈 Include creator info

    class Config:
        orm_mode = True


# ✅ List wrapper for paginated response
class SalaryHistoryListResponse(BaseModel):
    status: str
    result: Dict[str, Any]  # includes "count" and "data" keys

    class Config:
        orm_mode = True
