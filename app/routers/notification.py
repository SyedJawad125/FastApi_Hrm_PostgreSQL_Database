from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List

from .. import database, schemas, models, oauth2
from app.dependencies.permission import require
from app.utils import paginate_data

router = APIRouter(
    prefix="/notifications",
    tags=['Notifications']
)

# ✅ GET: All Notifications (Paginated)
@router.get("/", response_model=schemas.NotificationListResponse)
def get_notifications(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """Get all notifications for the current user (paginated)."""
    try:
        query = db.query(models.Notification).filter(
            models.Notification.user_id == current_user.id
        ).order_by(models.Notification.created_at.desc())

        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)

        return {
            "status": "success",
            "result": {
                "count": count,
                "data": paginated_data
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving notifications: {str(e)}")

# ✅ GET: Unread Notifications
@router.get("/unread", response_model=List[schemas.Notification])
def get_unread_notifications(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """Get unread notifications for the current user."""
    try:
        notifications = db.query(models.Notification).filter(
            models.Notification.user_id == current_user.id,
            models.Notification.is_read == False
        ).order_by(models.Notification.created_at.desc()).all()

        return notifications

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving unread notifications: {str(e)}")

# ✅ POST: Create Notification (Manual or internal use)
@router.post("/", response_model=schemas.NotificationResponse, dependencies=[require("create_notification")])
def create_notification(
    notification: schemas.NotificationCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """Create a new notification."""
    try:
        new_notification = models.Notification(
            **notification.model_dump(),
            created_by_id=current_user.id
        )
        db.add(new_notification)
        db.commit()
        db.refresh(new_notification)

        return new_notification

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating notification: {str(e)}")

# ✅ PATCH: Mark a specific notification as read
@router.patch("/{notification_id}/read", response_model=schemas.NotificationResponse)
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """Mark one notification as read."""
    try:
        notification = db.query(models.Notification).filter(
            models.Notification.id == notification_id,
            models.Notification.user_id == current_user.id
        ).first()

        if not notification:
            raise HTTPException(status_code=404, detail=f"Notification with ID {notification_id} not found.")

        notification.is_read = True
        db.commit()
        db.refresh(notification)
        return notification

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error marking notification as read: {str(e)}")

# ✅ PATCH: Mark all notifications as read
@router.patch("/mark-all-read", response_model=List[schemas.NotificationResponse])
def mark_all_notifications_as_read(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """Mark all notifications as read for the current user."""
    try:
        notifications = db.query(models.Notification).filter(
            models.Notification.user_id == current_user.id,
            models.Notification.is_read == False
        ).all()

        for notification in notifications:
            notification.is_read = True

        db.commit()
        return notifications

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error marking all notifications as read: {str(e)}")

# ✅ DELETE: Delete a notification
@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(
    notification_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """Delete a single notification for the current user."""
    try:
        notification_query = db.query(models.Notification).filter(
            models.Notification.id == notification_id,
            models.Notification.user_id == current_user.id
        )
        notification = notification_query.first()

        if not notification:
            raise HTTPException(status_code=404, detail=f"Notification with ID {notification_id} not found.")

        notification_query.delete(synchronize_session=False)
        db.commit()

        return None

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting notification: {str(e)}")
