from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import date, datetime
from enum import Enum


class ChangeType(str, Enum):
    PROMOTION = "promotion"
    ANNUAL_RAISE = "annual_raise"
    PERFORMANCE_RAISE = "performance_raise"
    ADJUSTMENT = "adjustment"
    DEMOTION = "demotion"
    OTHER = "other"


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
    created_by_user_id: int
    salary_structure_id: Optional[int] = None
    employee_salary_id: Optional[int] = None


class SalaryHistoryCreate(SalaryHistoryBase):
    pass


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


class SalaryHistoryOut(SalaryHistoryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class SalaryHistoryListResponse(BaseModel):
    status: str
    result: dict[str, Any]

    class Config:
        orm_mode = True
