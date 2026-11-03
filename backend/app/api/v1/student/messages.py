from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.message import Message
from app.models.user import User
from app.schemas.message import MessageResponse, MessageListResponse

router = APIRouter(tags=["学生-消息"])


@router.get("/", response_model=MessageListResponse)
def list_messages(
    type: Optional[str] = Query(None),
    is_read: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Message).filter(Message.user_id == current_user.id)
    if type:
        query = query.filter(Message.type == type)
    if is_read is not None:
        query = query.filter(Message.is_read == is_read)

    total = query.count()
    messages = query.order_by(Message.created_at.desc()).offset(
        (page - 1) * page_size
    ).limit(page_size).all()

    return {"total": total, "page": page, "page_size": page_size, "data": messages}


@router.get("/unread-count")
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    count = db.query(Message).filter(
        Message.user_id == current_user.id,
        Message.is_read == False
    ).count()
    return {"count": count}


@router.post("/read-all")
def mark_all_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db.query(Message).filter(
        Message.user_id == current_user.id,
        Message.is_read == False
    ).update({"is_read": True}, synchronize_session=False)
    db.commit()
    return {"message": "全部标为已读"}


@router.post("/{message_id}/read")
def mark_read(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    message = db.query(Message).filter(
        Message.id == message_id,
        Message.user_id == current_user.id
    ).first()
    if not message:
        raise HTTPException(status_code=404, detail="消息不存在")

    message.is_read = True
    db.commit()
    return {"message": "已读"}


@router.delete("/{message_id}")
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    message = db.query(Message).filter(
        Message.id == message_id,
        Message.user_id == current_user.id
    ).first()
    if not message:
        raise HTTPException(status_code=404, detail="消息不存在")

    db.delete(message)
    db.commit()
    return {"message": "删除成功"}
