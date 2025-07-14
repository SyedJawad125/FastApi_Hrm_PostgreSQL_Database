from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Time, Date, Boolean, Float
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, default=datetime.now().date())
    check_in = Column(Time, nullable=True)
    check_out = Column(Time, nullable=True)
    is_present = Column(Boolean, default=False)
    
    # Foreign Keys
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    
    # Relationships
    employee = relationship("Employee", back_populates="attendances")
    timesheet = relationship("Timesheet", back_populates="attendance", uselist=False)

