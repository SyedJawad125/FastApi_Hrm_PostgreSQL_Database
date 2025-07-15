from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.database import Base
from datetime import datetime
import enum

class PaymentFrequency(str, enum.Enum):
    MONTHLY = "monthly"
    BIWEEKLY = "biweekly"
    WEEKLY = "weekly"

class SalaryStructure(Base):
    __tablename__ = "salary_structures"

    id = Column(Integer, primary_key=True, index=True)
    base_salary = Column(Float, nullable=False)
    allowances = Column(Float, default=0.0)  # Housing, transport, etc.
    bonuses = Column(Float, default=0.0)  # Performance bonuses, etc.
    deductions = Column(Float, default=0.0)  # Tax, insurance, etc.
    payment_frequency = Column(String, default=PaymentFrequency.MONTHLY)
    effective_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # For tracking salary history
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=datetime.utcnow)

    # Foreign Keys
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    rank_id = Column(Integer, ForeignKey("ranks.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    employee = relationship("Employee", back_populates="salary_structures")
    rank = relationship("Rank", back_populates="salary_structures")
    department = relationship("Department", back_populates="salary_structures")
    creator = relationship("User", back_populates="created_salary_structures")
    salary_histories = relationship("SalaryHistory", back_populates="salary_structure") 