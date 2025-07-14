from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # The user who receives the notification
    leave_id = Column(Integer, ForeignKey("leaves.id"), nullable=True)  # Optional: If notification is about a leave
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # The user who triggered the notification
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="notifications")
    leave = relationship("Leave", back_populates="notifications")
    created_by = relationship("User", foreign_keys=[created_by_id], backref="notifications_created") 