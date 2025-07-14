from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Time, Date, Boolean, Float
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class Timesheet(Base):
    __tablename__ = "timesheets"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    hours_worked = Column(Float, nullable=False)
    overtime_hours = Column(Float, default=0.0)
    notes = Column(String, nullable=True)
    
    # Foreign Keys
    attendance_id = Column(Integer, ForeignKey("attendances.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    
    # Relationships
    attendance = relationship("Attendance", back_populates="timesheet")
    employee = relationship("Employee", back_populates="timesheets") 