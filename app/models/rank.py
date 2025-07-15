from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Rank(Base):
    __tablename__ = "ranks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    salary_range_min = Column(Float)
    salary_range_max = Column(Float)
    department_id = Column(Integer, ForeignKey("departments.id"))
    created_by_user_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    department = relationship("Department", back_populates="ranks")
    employees = relationship("Employee", back_populates="rank")
    creator = relationship("User", back_populates="created_ranks")
    employee_salaries = relationship("EmployeeSalary", back_populates="rank")
    salary_structures = relationship("SalaryStructure", back_populates="rank")
    payslips = relationship("Payslip", back_populates="rank") 