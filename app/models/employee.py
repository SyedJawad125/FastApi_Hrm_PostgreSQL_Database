from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models import User

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone_number = Column(String(20))
    hire_date = Column(Date, nullable=False)
    job_title = Column(String(100), nullable=False)
    salary = Column(Float, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    
    department = relationship("Department", back_populates="employees")
    # ✅ Foreign key column
    rank_id = Column(Integer, ForeignKey("ranks.id"))

    # ✅ Relationship back to Rank
    rank = relationship("Rank", back_populates="employees")
    
    # Add relationships for attendance and timesheet
    attendances = relationship("Attendance", back_populates="employee")
    timesheets = relationship("Timesheet", back_populates="employee")