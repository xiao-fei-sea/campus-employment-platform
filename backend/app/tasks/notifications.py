from app.celery_app import celery_app


@celery_app.task
def send_notification(user_id: int, title: str, content: str):
    from app.core.database import SessionLocal
    from app.models.message import Notification

    db = SessionLocal()
    try:
        notification = Notification(
            user_id=user_id,
            title=title,
            content=content,
            type="info"
        )
        db.add(notification)
        db.commit()
        return {"status": "success", "notification_id": notification.id}
    finally:
        db.close()


@celery_app.task
def send_bulk_notifications(user_ids: list, title: str, content: str):
    from app.core.database import SessionLocal
    from app.models.message import Notification

    db = SessionLocal()
    try:
        notifications = [
            Notification(user_id=user_id, title=title, content=content, type="info")
            for user_id in user_ids
        ]
        db.add_all(notifications)
        db.commit()
        return {"status": "success", "count": len(notifications)}
    finally:
        db.close()
