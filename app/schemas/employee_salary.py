from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import date, datetime
from enum import Enum


class SalaryType(str, Enum):
    BASE = "base"
    BONUS = "bonus"
    OVERTIME = "overtime"
    ALLOWANCE = "allowance"


class EmployeeSalaryBase(BaseModel):
    basic_salary: float
    overtime_rate: float = 0.0
    bonus_amount: float = 0.0
    housing_allowance: float = 0.0
    transport_allowance: float = 0.0
    medical_allowance: float = 0.0
    tax_deduction: float = 0.0
    insurance_deduction: float = 0.0
    other_deductions: float = 0.0
    net_salary: float
    salary_month: date
    payment_date: Optional[date] = None
    payment_status: Optional[str] = "pending"
    remarks: Optional[str] = None

    employee_id: int
    rank_id: int
    department_id: int
    created_by_user_id: int


class EmployeeSalaryCreate(EmployeeSalaryBase):
    pass


class EmployeeSalaryUpdate(BaseModel):
    basic_salary: Optional[float]
    overtime_rate: Optional[float]
    bonus_amount: Optional[float]
    housing_allowance: Optional[float]
    transport_allowance: Optional[float]
    medical_allowance: Optional[float]
    tax_deduction: Optional[float]
    insurance_deduction: Optional[float]
    other_deductions: Optional[float]
    net_salary: Optional[float]
    salary_month: Optional[date]
    payment_date: Optional[date]
    payment_status: Optional[str]
    remarks: Optional[str]
    rank_id: Optional[int]
    department_id: Optional[int]


class EmployeeSalaryOut(EmployeeSalaryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class EmployeeSalaryListResponse(BaseModel):
    status: str
    result: dict[str, Any]  # Contains "count" and "data"

    class Config:
        orm_mode = True
