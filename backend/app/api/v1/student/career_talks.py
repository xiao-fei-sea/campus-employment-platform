from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List
import logging

from app.core.database import get_db
from app.core.security import get_current_user, get_optional_user
from app.models.user import User, UserRole
from app.models.student import Student
from app.models.activity import CareerTalk, ActivityRegistration, ActivityStatus
from app.schemas.activity import (
    CareerTalkListResponse,
    ActivityRegistrationResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["学生-宣讲会"])


def get_optional_student(current_user: User = Depends(get_optional_user)) -> Student:
    try:
        if current_user is None:
            return None
        if current_user.role != UserRole.STUDENT:
            return None
        student = current_user.student_profile
        return student
    except:
        return None


def get_current_student(current_user: User = Depends(get_current_user)) -> Student:
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="仅学生可以访问此功能"
        )
    student = current_user.student_profile
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生信息不存在"
        )
    return student


@router.get("/", response_model=List[CareerTalkListResponse])
def list_career_talks(
    status: str = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_optional_student)
):
    query = db.query(CareerTalk).filter(CareerTalk.status == ActivityStatus.APPROVED)

    if status:
        query = query.filter(CareerTalk.status == status)

    query = query.order_by(CareerTalk.start_time.desc())

    talks = query.offset((page - 1) * page_size).limit(page_size).all()

    registered_talk_ids = set()
    if current_student:
        registrations = db.query(ActivityRegistration).filter(
            ActivityRegistration.student_id == current_student.id
        ).all()
        registered_talk_ids = {r.career_talk_id for r in registrations}

    result = []
    for talk in talks:
        result.append({
            "id": talk.id,
            "company_id": talk.company_id,
            "title": talk.title,
            "speaker_name": talk.speaker_name,
            "speaker_title": talk.speaker_title,
            "activity_type": talk.activity_type,
            "start_time": talk.start_time,
            "end_time": talk.end_time,
            "location": talk.location,
            "max_attendees": talk.max_attendees,
            "current_attendees": talk.current_attendees,
            "description": talk.description,
            "agenda": talk.agenda,
            "is_online": talk.is_online,
            "online_url": talk.online_url,
            "status": talk.status,
            "poster_url": talk.poster_url,
            "approval_comment": talk.approval_comment,
            "approved_at": talk.approved_at,
            "created_at": talk.created_at,
            "company_name": talk.company.name if talk.company else None,
            "company_logo": talk.company.logo if talk.company else None,
            "is_registered": talk.id in registered_talk_ids
        })

    return result


@router.get("/{talk_id}", response_model=CareerTalkListResponse)
def get_career_talk(
    talk_id: int,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_optional_student)
):
    talk = db.query(CareerTalk).filter(CareerTalk.id == talk_id).first()
    if not talk:
        raise HTTPException(status_code=404, detail="宣讲会不存在")

    is_registered = False
    if current_student:
        is_registered = db.query(ActivityRegistration).filter(
            ActivityRegistration.student_id == current_student.id,
            ActivityRegistration.career_talk_id == talk_id
        ).first() is not None

    return {
        "id": talk.id,
        "company_id": talk.company_id,
        "title": talk.title,
        "speaker_name": talk.speaker_name,
        "speaker_title": talk.speaker_title,
        "activity_type": talk.activity_type,
        "start_time": talk.start_time,
        "end_time": talk.end_time,
        "location": talk.location,
        "max_attendees": talk.max_attendees,
        "current_attendees": talk.current_attendees,
        "description": talk.description,
        "agenda": talk.agenda,
        "is_online": talk.is_online,
        "online_url": talk.online_url,
        "status": talk.status,
        "poster_url": talk.poster_url,
        "approval_comment": talk.approval_comment,
        "approved_at": talk.approved_at,
        "created_at": talk.created_at,
        "company_name": talk.company.name if talk.company else None,
        "company_logo": talk.company.logo if talk.company else None,
        "is_registered": is_registered
    }


@router.post("/{talk_id}/register", response_model=ActivityRegistrationResponse)
def register_career_talk(
    talk_id: int,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    logger.info(f"学生 {current_student.id} 尝试报名宣讲会 {talk_id}")

    talk = db.query(CareerTalk).filter(CareerTalk.id == talk_id).first()
    if not talk:
        logger.warning(f"宣讲会 {talk_id} 不存在")
        raise HTTPException(status_code=404, detail="宣讲会不存在")
    if talk.status != ActivityStatus.APPROVED:
        logger.warning(f"宣讲会 {talk_id} 状态不可报名: {talk.status}")
        raise HTTPException(status_code=400, detail="宣讲会暂不可报名")

    existing = db.query(ActivityRegistration).filter(
        ActivityRegistration.student_id == current_student.id,
        ActivityRegistration.career_talk_id == talk_id
    ).first()
    if existing:
        logger.warning(f"学生 {current_student.id} 已报名过宣讲会 {talk_id}")
        raise HTTPException(status_code=400, detail="您已报名过此宣讲会")

    if talk.max_attendees and talk.current_attendees >= talk.max_attendees:
        logger.warning(f"宣讲会 {talk_id} 报名人数已满")
        raise HTTPException(status_code=400, detail="报名人数已满")

    registration = ActivityRegistration(
        student_id=current_student.id,
        career_talk_id=talk_id
    )
    db.add(registration)

    talk.current_attendees += 1
    db.commit()
    db.refresh(registration)

    logger.info(f"学生 {current_student.id} 成功报名宣讲会 {talk_id}")
    return registration


@router.delete("/{talk_id}/cancel")
def cancel_registration(
    talk_id: int,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    logger.info(f"学生 {current_student.id} 尝试取消宣讲会 {talk_id} 的报名")

    registration = db.query(ActivityRegistration).filter(
        ActivityRegistration.student_id == current_student.id,
        ActivityRegistration.career_talk_id == talk_id
    ).first()

    if not registration:
        logger.warning(f"学生 {current_student.id} 的报名记录不存在，宣讲会ID: {talk_id}")
        raise HTTPException(status_code=404, detail="报名记录不存在")

    talk = db.query(CareerTalk).filter(CareerTalk.id == talk_id).first()
    if talk:
        logger.info(f"宣讲会 {talk_id} 当前报名人数: {talk.current_attendees}")
        talk.current_attendees = max(0, talk.current_attendees - 1)
        logger.info(f"宣讲会 {talk_id} 取消后报名人数: {talk.current_attendees}")

    db.delete(registration)
    db.commit()
    logger.info(f"学生 {current_student.id} 成功取消宣讲会 {talk_id} 的报名")

    return {"message": "取消成功"}


@router.get("/my-registrations", response_model=List[ActivityRegistrationResponse])
def my_registrations(
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    registrations = db.query(ActivityRegistration).filter(
        ActivityRegistration.student_id == current_student.id
    ).order_by(ActivityRegistration.created_at.desc()).all()

    return registrations
