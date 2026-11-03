from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.core.security import require_roles
from app.models.user import User, UserRole
from app.models.job import Job, JobStatus
from app.models.company import Company
from app.schemas.job import JobResponse, JobApprove, PaginatedJobResponse

router = APIRouter(tags=["管理端-岗位管理"])


@router.get("", response_model=PaginatedJobResponse)
@router.get("/", response_model=PaginatedJobResponse)
def list_all_jobs(
    status: str = None,
    keyword: str = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=10000),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    query = db.query(Job).join(Company, Job.company_id == Company.id)

    if status:
        query = query.filter(Job.status == status)

    if keyword:
        query = query.filter(
            Job.title.contains(keyword) |
            Job.description.contains(keyword)
        )

    total = query.count()

    query = query.order_by(Job.created_at.desc())
    jobs = query.offset((page - 1) * page_size).limit(page_size).all()

    job_responses = []
    for job in jobs:
        job_dict = {
            "id": job.id,
            "company_id": job.company_id,
            "title": job.title,
            "job_type": job.job_type,
            "salary_min": job.salary_min,
            "salary_max": job.salary_max,
            "salary_show": job.salary_show,
            "province": job.province,
            "city": job.city,
            "district": job.district,
            "address": job.address,
            "description": job.description,
            "requirement": job.requirement,
            "benefit": job.benefit,
            "skills": job.skills,
            "headcount": job.headcount,
            "experience": job.experience,
            "education": job.education,
            "expired_at": job.expired_at,
            "status": job.status,
            "application_count": job.application_count,
            "view_count": job.view_count,
            "is_top": job.is_top,
            "is_highlight": job.is_highlight,
            "rejection_reason": job.rejection_reason,
            "approved_at": job.approved_at,
            "created_at": job.created_at,
            "updated_at": job.updated_at,
            "company_name": job.company.name if job.company else None,
            "company_logo": job.company.logo if job.company else None,
            "industry": job.company.industry.value if job.company and job.company.industry else None,
        }
        job_responses.append(job_dict)

    return PaginatedJobResponse(
        jobs=job_responses,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="岗位不存在")
    return job


@router.post("/{job_id}/approve")
def approve_job(
    job_id: int,
    approval_data: JobApprove,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="岗位不存在")

    job.status = approval_data.status
    if approval_data.status == JobStatus.APPROVED:
        job.approved_at = datetime.now()
        job.approved_by = current_user.id
    elif approval_data.status == JobStatus.REJECTED:
        job.rejection_reason = approval_data.comment

    db.commit()

    return {"message": "审核完成"}


@router.post("/{job_id}/top")
def top_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="岗位不存在")

    job.is_top = not job.is_top
    db.commit()

    return {"message": "置顶成功" if job.is_top else "取消置顶成功"}


@router.post("/{job_id}/highlight")
def highlight_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="岗位不存在")

    job.is_highlight = not job.is_highlight
    db.commit()

    return {"message": "优选成功" if job.is_highlight else "取消优选成功"}
