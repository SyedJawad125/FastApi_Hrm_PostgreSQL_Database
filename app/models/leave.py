from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import enum

class LeaveStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class LeaveType(str, enum.Enum):
    ANNUAL = "annual"
    SICK = "sick"
    MATERNITY = "maternity"
    PATERNITY = "paternity"
    UNPAID = "unpaid"
    OTHER = "other"

class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    leave_type = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    status = Column(String, default=LeaveStatus.PENDING)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=datetime.utcnow)

    # Foreign Keys
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    approved_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    employee = relationship("User", foreign_keys=[employee_id], backref="leaves_requested")
    approved_by = relationship("User", foreign_keys=[approved_by_id], backref="leaves_approved")
    
    # Add notifications relationship
    notifications = relationship("Notification", back_populates="leave") 

    

