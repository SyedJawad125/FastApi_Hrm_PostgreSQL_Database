from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# Base schema
class NotificationBase(BaseModel):
    title: str
    message: str
    user_id: int
    leave_id: Optional[int] = None

# For creation
class NotificationCreate(NotificationBase):
    pass

# For marking as read
class NotificationUpdate(BaseModel):
    is_read: bool

# Full notification structure (used in responses)
class Notification(NotificationBase):
    id: int
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Important for ORM serialization

# API response schema
class NotificationResponse(Notification):
    pass

# Paginated list response
class PaginatedNotifications(BaseModel):
    count: int
    data: List[Notification]

class NotificationListResponse(BaseModel):
    status: str = "success"
    result: PaginatedNotifications
