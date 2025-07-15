from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.database import Base
from datetime import datetime
import enum

class SalaryType(str, enum.Enum):
    BASE = "base"
    BONUS = "bonus"
    OVERTIME = "overtime"
    ALLOWANCE = "allowance"

class EmployeeSalary(Base):
    __tablename__ = "employee_salaries"

    id = Column(Integer, primary_key=True, index=True)
    basic_salary = Column(Float, nullable=False)
    overtime_rate = Column(Float, default=0.0)
    bonus_amount = Column(Float, default=0.0)
    housing_allowance = Column(Float, default=0.0)
    transport_allowance = Column(Float, default=0.0)
    medical_allowance = Column(Float, default=0.0)
    tax_deduction = Column(Float, default=0.0)
    insurance_deduction = Column(Float, default=0.0)
    other_deductions = Column(Float, default=0.0)
    net_salary = Column(Float, nullable=False)
    salary_month = Column(Date, nullable=False)  # For which month this salary is
    payment_date = Column(Date, nullable=True)  # When the salary was paid
    payment_status = Column(String, default="pending")  # pending, paid, cancelled
    remarks = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=datetime.utcnow)

    # Foreign Keys
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    rank_id = Column(Integer, ForeignKey("ranks.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    employee = relationship("Employee", back_populates="salaries")
    rank = relationship("Rank", back_populates="employee_salaries")
    department = relationship("Department", back_populates="employee_salaries")
    creator = relationship("User", back_populates="created_employee_salaries")
    payslips = relationship("Payslip", back_populates="employee_salary")
    salary_histories = relationship("SalaryHistory", back_populates="employee_salary") 