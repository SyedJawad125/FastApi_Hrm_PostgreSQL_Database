from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String)
    created_by_user_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="created_departments")
    employees = relationship("Employee", back_populates="department")
    ranks = relationship("Rank", back_populates="department")
    employee_salaries = relationship("EmployeeSalary", back_populates="department")
    salary_structures = relationship("SalaryStructure", back_populates="department")
    salary_histories = relationship("SalaryHistory", back_populates="department")
    payslips = relationship("Payslip", back_populates="department")
