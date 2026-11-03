from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.company import Company
from app.models.job import Job
from app.models.resume import Resume
from app.models.application import Application, ApplicationStatus
from app.models.student import Student
from app.schemas.application import ApplicationListResponse

router = APIRouter(tags=["企业-简历管理"])


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


@router.get("/applications/", response_model=List[ApplicationListResponse])
def list_received_applications(
    job_id: int = None,
    status: str = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    query = db.query(Application).options(
        joinedload(Application.student),
        joinedload(Application.job),
        joinedload(Application.resume)
    ).join(Job).filter(
        Job.company_id == current_company.id
    )

    if job_id:
        query = query.filter(Application.job_id == job_id)

    if status:
        query = query.filter(Application.status == status)

    query = query.order_by(Application.created_at.desc())

    applications = query.offset((page - 1) * page_size).limit(page_size).all()

    result = []
    for app in applications:
        student = app.student
        resume = app.resume
        result.append({
            "id": app.id,
            "student_id": app.student_id,
            "job_id": app.job_id,
            "resume_id": app.resume_id,
            "cover_letter": app.cover_letter,
            "status": app.status,
            "interview_time": app.interview_time,
            "interview_location": app.interview_location,
            "offer_salary": app.offer_salary,
            "created_at": app.created_at,
            "updated_at": app.updated_at,
            "job_title": app.job.title if app.job else None,
            "company_name": current_company.name,
            "student_name": student.name if student else None,
            "avatar": student.avatar if student else None,
            "school": resume.education_school if resume else None,
            "major": resume.education_major if resume else None,
            "education": resume.education_degree if resume else None,
            "resume_title": resume.title if resume else None
        })

    return result


@router.get("/applications/{application_id}", response_model=ApplicationListResponse)
def get_application_detail(
    application_id: int,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    application = db.query(Application).join(Job).filter(
        Application.id == application_id,
        Job.company_id == current_company.id
    ).first()

    if not application:
        raise HTTPException(status_code=404, detail="投递记录不存在")

    if not application.viewed_at:
        application.viewed_at = db.query(Application).filter(
            Application.id == application_id
        ).first().viewed_at
        if application.status == ApplicationStatus.PENDING:
            application.status = ApplicationStatus.VIEWED
        db.commit()

    student = application.student
    resume = application.resume

    return {
        "id": application.id,
        "student_id": application.student_id,
        "job_id": application.job_id,
        "resume_id": application.resume_id,
        "cover_letter": application.cover_letter,
        "status": application.status,
        "interview_time": application.interview_time,
        "interview_location": application.interview_location,
        "offer_salary": application.offer_salary,
        "created_at": application.created_at,
        "updated_at": application.updated_at,
        "job_title": application.job.title if application.job else None,
        "company_name": current_company.name,
        "student_name": student.name if student else None,
        "avatar": student.avatar if student else None,
        "school": resume.education_school if resume else None,
        "major": resume.education_major if resume else None,
        "education": resume.education_degree if resume else None,
        "resume_title": resume.title if resume else None
    }


class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus
    feedback: Optional[str] = None
    interview_time: Optional[str] = None
    interview_location: Optional[str] = None
    offer_salary: Optional[int] = None


@router.put("/applications/{application_id}/status")
def update_application_status(
    application_id: int,
    data: ApplicationStatusUpdate,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    application = db.query(Application).join(Job).filter(
        Application.id == application_id,
        Job.company_id == current_company.id
    ).first()

    if not application:
        raise HTTPException(status_code=404, detail="投递记录不存在")

    application.status = data.status
    if data.feedback:
        application.feedback = data.feedback
    if data.interview_time:
        application.interview_time = data.interview_time
    if data.interview_location:
        application.interview_location = data.interview_location
    if data.offer_salary:
        application.offer_salary = data.offer_salary

    db.commit()

    return {"message": "更新成功"}


@router.get("/talent-pool/")
def get_talent_pool(
    keyword: str = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    query = db.query(Resume).join(Student).filter(
        Resume.visibility != "private"
    )

    if keyword:
        query = query.filter(
            Resume.personal_name.contains(keyword) |
            Resume.education_major.contains(keyword) |
            Resume.skill_names.contains(keyword)
        )

    query = query.order_by(Resume.updated_at.desc())

    resumes = query.offset((page - 1) * page_size).limit(page_size).all()

    return resumes
