from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.company import Company
from app.models.activity import CareerTalk, ActivityRegistration, ActivityStatus
from app.schemas.activity import (
    CareerTalkCreate,
    CareerTalkUpdate,
    CareerTalkResponse,
    ActivityRegistrationWithDetail
)

router = APIRouter(tags=["企业-宣讲会"])


def get_current_company(current_user: User = Depends(get_current_user)) -> Company:
    if current_user.role != UserRole.COMPANY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="仅企业可以访问此功能"
        )
    company = current_user.company_profile
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业信息不存在"
        )
    return company


@router.get("/", response_model=List[CareerTalkResponse])
def list_company_career_talks(
    status: str = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    query = db.query(CareerTalk).filter(CareerTalk.company_id == current_company.id)

    if status:
        query = query.filter(CareerTalk.status == status)

    query = query.order_by(CareerTalk.start_time.desc())

    talks = query.offset((page - 1) * page_size).limit(page_size).all()
    return talks


@router.get("/{talk_id}", response_model=CareerTalkResponse)
def get_company_career_talk(
    talk_id: int,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    talk = db.query(CareerTalk).filter(
        CareerTalk.id == talk_id,
        CareerTalk.company_id == current_company.id
    ).first()
    if not talk:
        raise HTTPException(status_code=404, detail="宣讲会不存在")
    return talk


@router.post("/", response_model=CareerTalkResponse)
def create_career_talk(
    talk_data: CareerTalkCreate,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    talk = CareerTalk(**talk_data.model_dump(), company_id=current_company.id)
    db.add(talk)
    db.commit()
    db.refresh(talk)
    return talk


@router.put("/{talk_id}", response_model=CareerTalkResponse)
def update_career_talk(
    talk_id: int,
    talk_data: CareerTalkUpdate,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    talk = db.query(CareerTalk).filter(
        CareerTalk.id == talk_id,
        CareerTalk.company_id == current_company.id
    ).first()
    if not talk:
        raise HTTPException(status_code=404, detail="宣讲会不存在")

    for key, value in talk_data.model_dump(exclude_unset=True).items():
        setattr(talk, key, value)

    if talk.status == ActivityStatus.APPROVED:
        talk.status = ActivityStatus.PENDING

    db.commit()
    db.refresh(talk)
    return talk


@router.delete("/{talk_id}")
def delete_career_talk(
    talk_id: int,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    talk = db.query(CareerTalk).filter(
        CareerTalk.id == talk_id,
        CareerTalk.company_id == current_company.id
    ).first()
    if not talk:
        raise HTTPException(status_code=404, detail="宣讲会不存在")

    talk.status = ActivityStatus.CANCELLED
    db.commit()

    return {"message": "宣讲会已取消"}


@router.get("/{talk_id}/registrations", response_model=List[ActivityRegistrationWithDetail])
def list_talk_registrations(
    talk_id: int,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    talk = db.query(CareerTalk).filter(
        CareerTalk.id == talk_id,
        CareerTalk.company_id == current_company.id
    ).first()
    if not talk:
        raise HTTPException(status_code=404, detail="宣讲会不存在")

    registrations = db.query(ActivityRegistration).filter(
        ActivityRegistration.career_talk_id == talk_id
    ).order_by(ActivityRegistration.created_at.desc()).all()

    result = []
    for reg in registrations:
        result.append({
            "id": reg.id,
            "student_id": reg.student_id,
            "career_talk_id": reg.career_talk_id,
            "status": reg.status,
            "is_attended": reg.is_attended,
            "signed_at": reg.signed_at,
            "created_at": reg.created_at,
            "career_talk_title": talk.title,
            "student_name": reg.student.name if reg.student else None
        })

    return result
