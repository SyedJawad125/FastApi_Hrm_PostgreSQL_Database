from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.database import Base
from datetime import datetime
import enum

class ChangeType(str, enum.Enum):
    PROMOTION = "promotion"
    ANNUAL_RAISE = "annual_raise"
    PERFORMANCE_RAISE = "performance_raise"
    ADJUSTMENT = "adjustment"
    DEMOTION = "demotion"
    OTHER = "other"

class SalaryHistory(Base):
    __tablename__ = "salary_histories"

    id = Column(Integer, primary_key=True, index=True)
    previous_salary = Column(Float, nullable=False)
    new_salary = Column(Float, nullable=False)
    change_percentage = Column(Float, nullable=False)  # Calculated field for salary change percentage
    change_type = Column(String, nullable=False)  # Uses ChangeType enum
    change_reason = Column(Text, nullable=True)  # Detailed explanation for the change
    effective_date = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)

    # Foreign Keys
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    previous_rank_id = Column(Integer, ForeignKey("ranks.id"), nullable=False)
    new_rank_id = Column(Integer, ForeignKey("ranks.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    salary_structure_id = Column(Integer, ForeignKey("salary_structures.id"), nullable=True)
    employee_salary_id = Column(Integer, ForeignKey("employee_salaries.id"), nullable=True)

    # Relationships
    employee = relationship("Employee", back_populates="salary_histories")
    previous_rank = relationship("Rank", foreign_keys=[previous_rank_id])
    new_rank = relationship("Rank", foreign_keys=[new_rank_id])
    department = relationship("Department", back_populates="salary_histories")
    creator = relationship("User", back_populates="created_salary_histories")
    salary_structure = relationship("SalaryStructure", back_populates="salary_histories")
    employee_salary = relationship("EmployeeSalary", back_populates="salary_histories") 