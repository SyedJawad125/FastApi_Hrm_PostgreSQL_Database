from pydantic import BaseModel
from typing import Optional, Any
from datetime import date, datetime
from enum import Enum


class PayslipStatus(str, Enum):
    DRAFT = "draft"
    GENERATED = "generated"
    APPROVED = "approved"
    PAID = "paid"
    CANCELLED = "cancelled"


# Base schema used for both create and response
class PayslipBase(BaseModel):
    payslip_number: str
    pay_period_start: date
    pay_period_end: date
    basic_salary: float
    overtime_pay: float = 0.0
    bonus: float = 0.0
    housing_allowance: float = 0.0
    transport_allowance: float = 0.0
    medical_allowance: float = 0.0
    other_allowances: float = 0.0
    gross_salary: float

    tax_deduction: float = 0.0
    insurance_deduction: float = 0.0
    loan_deduction: float = 0.0
    other_deductions: float = 0.0
    total_deductions: float

    net_salary: float
    payment_date: Optional[date] = None
    payment_method: Optional[str] = None
    bank_account: Optional[str] = None
    remarks: Optional[str] = None
    status: PayslipStatus = PayslipStatus.DRAFT

    employee_id: int
    # employee_salary_id: int
    department_id: int
    rank_id: int

    # Not part of creation payload, but allowed in update
    approved_by_user_id: Optional[int] = None


# Used in POST request
class PayslipCreate(PayslipBase):
    pass


# Used in PUT/PATCH request
class PayslipUpdate(BaseModel):
    payslip_number: Optional[str]
    pay_period_start: Optional[date]
    pay_period_end: Optional[date]
    basic_salary: Optional[float]
    overtime_pay: Optional[float]
    bonus: Optional[float]
    housing_allowance: Optional[float]
    transport_allowance: Optional[float]
    medical_allowance: Optional[float]
    other_allowances: Optional[float]
    gross_salary: Optional[float]

    tax_deduction: Optional[float]
    insurance_deduction: Optional[float]
    loan_deduction: Optional[float]
    other_deductions: Optional[float]
    total_deductions: Optional[float]

    net_salary: Optional[float]
    payment_date: Optional[date]
    payment_method: Optional[str]
    bank_account: Optional[str]
    remarks: Optional[str]
    status: Optional[PayslipStatus]

    approved_by_user_id: Optional[int] = None
    department_id: Optional[int]
    rank_id: Optional[int]
    
    # employee_salary_id: Optional[int]


# Used in response
class PayslipOut(PayslipBase):
    id: int
    created_by_user_id: int
    employee_salary_id: Optional[int]  # visible in response only
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
        from_attributes = True



# For paginated or structured list responses
class PayslipListResponse(BaseModel):
    status: str
    result: dict[str, Any]  # e.g. {"count": 25, "data": [PayslipOut, PayslipOut, ...]}

    class Config:
        orm_mode = True
        from_attributes = True

