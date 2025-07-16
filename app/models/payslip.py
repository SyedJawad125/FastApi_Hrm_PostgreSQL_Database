from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.database import Base
from datetime import datetime
import enum

class PayslipStatus(str, enum.Enum):
    DRAFT = "draft"
    GENERATED = "generated"
    APPROVED = "approved"
    PAID = "paid"
    CANCELLED = "cancelled"

class Payslip(Base):
    __tablename__ = "payslips"

    id = Column(Integer, primary_key=True, index=True)
    payslip_number = Column(String, unique=True, nullable=False)  # Unique identifier for the payslip
    pay_period_start = Column(Date, nullable=False)  # Start date of pay period
    pay_period_end = Column(Date, nullable=False)  # End date of pay period
    basic_salary = Column(Float, nullable=False)
    overtime_pay = Column(Float, default=0.0)
    bonus = Column(Float, default=0.0)
    housing_allowance = Column(Float, default=0.0)
    transport_allowance = Column(Float, default=0.0)
    medical_allowance = Column(Float, default=0.0)
    other_allowances = Column(Float, default=0.0)
    gross_salary = Column(Float, nullable=False)
    
    # Deductions
    tax_deduction = Column(Float, default=0.0)
    insurance_deduction = Column(Float, default=0.0)
    loan_deduction = Column(Float, default=0.0)
    other_deductions = Column(Float, default=0.0)
    total_deductions = Column(Float, nullable=False)
    
    net_salary = Column(Float, nullable=False)
    payment_date = Column(Date, nullable=True)
    payment_method = Column(String, nullable=True)  # Bank transfer, cash, etc.
    bank_account = Column(String, nullable=True)
    remarks = Column(Text, nullable=True)
    status = Column(String, default=PayslipStatus.DRAFT)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=datetime.utcnow)

    # Foreign Keys
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    employee_salary_id = Column(Integer, ForeignKey("employee_salaries.id"), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    rank_id = Column(Integer, ForeignKey("ranks.id"), nullable=False)
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    approved_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    employee = relationship("Employee", back_populates="payslips")
    employee_salary = relationship("EmployeeSalary", back_populates="payslips")
    department = relationship("Department", back_populates="payslips")
    rank = relationship("Rank", back_populates="payslips")
    creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_payslips")
    approver = relationship("User", foreign_keys=[approved_by_user_id], back_populates="approved_payslips") 