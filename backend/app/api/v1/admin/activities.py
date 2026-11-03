from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.core.security import require_roles
from app.models.user import User, UserRole
from app.models.activity import CareerTalk, ActivityRegistration, ActivityStatus
from app.models.company import Company
from app.schemas.activity import CareerTalkResponse, CareerTalkApprove, PaginatedCareerTalkResponse, CareerTalkListResponse

router = APIRouter(tags=["管理端-活动管理"])


@router.get("/career-talks", response_model=PaginatedCareerTalkResponse)
def list_all_career_talks(
    status: str = None,
    keyword: str = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    query = db.query(CareerTalk)

    if status:
        query = query.filter(CareerTalk.status == status)

    if keyword and keyword.strip():
        keyword_filter = f"%{keyword.strip()}%"
        query = query.outerjoin(Company, CareerTalk.company_id == Company.id)
        query = query.filter(
            or_(
                CareerTalk.title.ilike(keyword_filter),
                Company.name.ilike(keyword_filter)
            )
        )

    total = query.count()

    query = query.order_by(CareerTalk.start_time.desc())
    talks = query.offset((page - 1) * page_size).limit(page_size).all()

    activities = []
    for talk in talks:
        company = db.query(Company).filter(Company.id == talk.company_id).first() if talk.company_id else None
        activity_type_value = talk.activity_type.value if hasattr(talk.activity_type, 'value') else talk.activity_type
        status_value = talk.status.value if hasattr(talk.status, 'value') else talk.status
        activities.append(CareerTalkListResponse(
            id=talk.id,
            company_id=talk.company_id,
            title=talk.title,
            speaker_name=talk.speaker_name,
            speaker_title=talk.speaker_title,
            speaker_avatar=talk.speaker_avatar,
            status=status_value,
            activity_type=activity_type_value,
            start_time=talk.start_time,
            end_time=talk.end_time,
            location=talk.location,
            max_attendees=talk.max_attendees,
            current_attendees=talk.current_attendees,
            description=talk.description,
            poster_url=talk.poster_url,
            approval_comment=talk.approval_comment,
            approved_at=talk.approved_at,
            created_at=talk.created_at,
            company_name=company.name if company else None,
            company_logo=company.logo if company else None,
            is_registered=False
        ))

    return PaginatedCareerTalkResponse(
        activities=activities,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/career-talks/{talk_id}", response_model=CareerTalkResponse)
def get_career_talk(
    talk_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    talk = db.query(CareerTalk).filter(CareerTalk.id == talk_id).first()
    if not talk:
        raise HTTPException(status_code=404, detail="宣讲会不存在")
    return talk


@router.post("/career-talks/{talk_id}/approve")
def approve_career_talk(
    talk_id: int,
    approval_data: CareerTalkApprove,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    talk = db.query(CareerTalk).filter(CareerTalk.id == talk_id).first()
    if not talk:
        raise HTTPException(status_code=404, detail="宣讲会不存在")

    talk.status = approval_data.status
    if approval_data.status == ActivityStatus.APPROVED:
        talk.approved_at = datetime.now()
        talk.approved_by = current_user.id
        talk.approval_comment = approval_data.comment
    elif approval_data.status == ActivityStatus.REJECTED:
        talk.approval_comment = approval_data.comment

    db.commit()

    return {"message": "审核完成"}


@router.delete("/career-talks/{talk_id}")
def delete_career_talk(
    talk_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    talk = db.query(CareerTalk).filter(CareerTalk.id == talk_id).first()
    if not talk:
        raise HTTPException(status_code=404, detail="宣讲会不存在")

    ActivityRegistration.query.filter(
        ActivityRegistration.career_talk_id == talk_id
    ).delete(synchronize_session=False)

    db.delete(talk)
    db.commit()

    return {"message": "删除成功"}


@router.put("/career-talks/{talk_id}")
def update_career_talk(
    talk_id: int,
    update_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    talk = db.query(CareerTalk).filter(CareerTalk.id == talk_id).first()
    if not talk:
        raise HTTPException(status_code=404, detail="宣讲会不存在")

    if 'title' in update_data:
        talk.title = update_data['title']
    if 'start_time' in update_data:
        if update_data['start_time']:
            talk.start_time = datetime.fromisoformat(update_data['start_time'].replace('Z', '+00:00'))
    if 'end_time' in update_data:
        if update_data['end_time']:
            talk.end_time = datetime.fromisoformat(update_data['end_time'].replace('Z', '+00:00'))
    if 'location' in update_data:
        talk.location = update_data['location']
    if 'max_attendees' in update_data:
        talk.max_attendees = update_data['max_attendees']
    if 'description' in update_data:
        talk.description = update_data['description']

    db.commit()

    return {"message": "更新成功"}


@router.get("/career-talks/{talk_id}/registrations", response_model=List)
def get_talk_registrations(
    talk_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    talk = db.query(CareerTalk).filter(CareerTalk.id == talk_id).first()
    if not talk:
        raise HTTPException(status_code=404, detail="宣讲会不存在")

    registrations = db.query(ActivityRegistration).filter(
        ActivityRegistration.career_talk_id == talk_id
    ).all()

    return [{
        "id": reg.id,
        "student_id": reg.student_id,
        "student_name": reg.student.name if reg.student else None,
        "status": reg.status,
        "is_attended": reg.is_attended,
        "signed_at": reg.signed_at,
        "created_at": reg.created_at
    } for reg in registrations]


@router.post("/registrations/{registration_id}/sign-in")
def sign_in_registration(
    registration_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    registration = db.query(ActivityRegistration).filter(
        ActivityRegistration.id == registration_id
    ).first()
    if not registration:
        raise HTTPException(status_code=404, detail="报名记录不存在")

    registration.is_attended = True
    registration.signed_at = datetime.now()
    db.commit()

    return {"message": "签到成功"}
