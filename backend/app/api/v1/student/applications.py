from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.student import Student
from app.models.job import Job
from app.models.resume import Resume
from app.models.application import Application, ApplicationStatus
from app.schemas.application import ApplicationCreate, ApplicationListResponse

router = APIRouter(tags=["学生-投递管理"])


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


@router.get("/", response_model=List[ApplicationListResponse])
def list_applications(
    status: str = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    query = db.query(Application).filter(
        Application.student_id == current_student.id,
        Application.status != ApplicationStatus.WITHDRAWN
    )

    if status:
        try:
            status_enum = ApplicationStatus(status)
            query = query.filter(Application.status == status_enum)
        except ValueError:
            pass

    query = query.order_by(Application.created_at.desc())

    applications = query.offset((page - 1) * page_size).limit(page_size).all()

    result = []
    for app in applications:
        job = app.job
        company = job.company if job else None
        salary_show = job.salary_show if job and job.salary_show else None
        if not salary_show and job and job.salary_min and job.salary_max:
            salary_show = f"{job.salary_min // 1000}-{job.salary_max // 1000}K"
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
            "job_title": job.title if job else None,
            "company_name": company.name if company else None,
            "company_logo": company.logo if company else None,
            "city": job.city if job else None,
            "province": job.province if job else None,
            "salary_show": salary_show,
            "student_name": current_student.name,
            "resume_title": app.resume.title if app.resume else None
        })

    return result


@router.post("/", response_model=ApplicationListResponse)
def create_application(
    application_data: ApplicationCreate,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    existing = db.query(Application).filter(
        Application.student_id == current_student.id,
        Application.job_id == application_data.job_id,
        Application.status.notin_([ApplicationStatus.REJECTED, ApplicationStatus.WITHDRAWN])
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="您已投递过此岗位")

    job = db.query(Job).filter(Job.id == application_data.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="岗位不存在")
    if job.status != "approved":
        raise HTTPException(status_code=400, detail="岗位暂不可投递")

    resume = db.query(Resume).filter(
        Resume.id == application_data.resume_id,
        Resume.student_id == current_student.id
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="简历不存在")

    application = Application(
        **application_data.model_dump(),
        student_id=current_student.id
    )
    db.add(application)

    job.application_count += 1
    db.commit()
    db.refresh(application)

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
        "job_title": job.title,
        "company_name": job.company.name if job.company else None,
        "company_logo": job.company.logo if job.company else None,
        "city": job.city,
        "province": job.province,
        "salary_show": job.salary_show if job.salary_show else f"{job.salary_min // 1000}-{job.salary_max // 1000}K" if job.salary_min and job.salary_max else None,
        "student_name": current_student.name,
        "resume_title": resume.title
    }


@router.post("/{application_id}/withdraw")
def withdraw_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.student_id == current_student.id
    ).first()
    if not application:
        raise HTTPException(status_code=404, detail="投递记录不存在")

    if application.status not in [ApplicationStatus.PENDING, ApplicationStatus.VIEWED]:
        raise HTTPException(status_code=400, detail="当前状态无法撤回")

    application.status = ApplicationStatus.WITHDRAWN
    db.commit()

    return {"message": "撤回成功"}
