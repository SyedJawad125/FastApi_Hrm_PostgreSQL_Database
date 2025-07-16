# from pydantic import BaseModel
# from typing import Optional, List, Any
# from datetime import date, datetime
# from enum import Enum


# class SalaryType(str, Enum):
#     BASE = "base"
#     BONUS = "bonus"
#     OVERTIME = "overtime"
#     ALLOWANCE = "allowance"


# # ✅ Base schema for creation
# class EmployeeSalaryBase(BaseModel):
#     basic_salary: float
#     overtime_rate: float = 0.0
#     bonus_amount: float = 0.0
#     housing_allowance: float = 0.0
#     transport_allowance: float = 0.0
#     medical_allowance: float = 0.0
#     tax_deduction: float = 0.0
#     insurance_deduction: float = 0.0
#     other_deductions: float = 0.0

#     salary_month: date
#     payment_date: Optional[date] = None
#     payment_status: Optional[str] = "pending"
#     remarks: Optional[str] = None

#     employee_id: int
#     rank_id: int
#     department_id: int
#     created_by_user_id: int


# # ✅ Create schema
# class EmployeeSalaryCreate(EmployeeSalaryBase):
#     pass


# # ✅ Update schema (partial)
# class EmployeeSalaryUpdate(BaseModel):
#     basic_salary: Optional[float]
#     overtime_rate: Optional[float]
#     bonus_amount: Optional[float]
#     housing_allowance: Optional[float]
#     transport_allowance: Optional[float]
#     medical_allowance: Optional[float]
#     tax_deduction: Optional[float]
#     insurance_deduction: Optional[float]
#     other_deductions: Optional[float]
#     net_salary: Optional[float]  # still allowed in PATCH in case of manual override
#     salary_month: Optional[date]
#     payment_date: Optional[date]
#     payment_status: Optional[str]
#     remarks: Optional[str]
#     rank_id: Optional[int]
#     department_id: Optional[int]


# # ✅ Output schema (includes net_salary)
# class EmployeeSalaryOut(EmployeeSalaryBase):
#     id: int
#     net_salary: float  # include in response only
#     created_at: datetime
#     updated_at: Optional[datetime]

#     class Config:
#         orm_mode = True


# # ✅ List response wrapper
# class EmployeeSalaryListResponse(BaseModel):
#     status: str
#     result: dict[str, Any]  # contains "count" and "data"

#     class Config:
#         orm_mode = True



from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import date, datetime
from enum import Enum


class SalaryType(str, Enum):
    BASE = "base"
    BONUS = "bonus"
    OVERTIME = "overtime"
    ALLOWANCE = "allowance"


# ✅ Base schema (shared fields for creation & response)
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

    salary_month: date
    payment_date: Optional[date] = None
    payment_status: Optional[str] = "pending"
    remarks: Optional[str] = None

    employee_id: int
    rank_id: int
    department_id: int


# ✅ Schema for creation (POST)
class EmployeeSalaryCreate(EmployeeSalaryBase):
    pass


# ✅ Schema for update (PATCH)
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
    net_salary: Optional[float]  # ✅ Optional for override in PATCH
    salary_month: Optional[date]
    payment_date: Optional[date]
    payment_status: Optional[str]
    remarks: Optional[str]
    rank_id: Optional[int]
    department_id: Optional[int]

    class Config:
        from_attributes = True

# ✅ Minimal user schema for creator info
class UserOut(BaseModel):
    id: int
    username: str  # Adjust if you're using "email" or "name" instead

    class Config:
        orm_mode = True


# ✅ Schema for response (GET/POST/PATCH response)
class EmployeeSalaryOut(EmployeeSalaryBase):
    id: int
    net_salary: float  # ✅ Always shown in response
    creator: Optional[UserOut]  # 👈 Include creator info
    # created_by_user_id: int  # ✅ Included in response only
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ✅ List response schema
class EmployeeSalaryListResponse(BaseModel):
    status: str
    result: dict[str, Any]  # contains {"count": int, "data": [...]}

    class Config:
        from_attributes = True
