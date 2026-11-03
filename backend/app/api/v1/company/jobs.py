from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.company import Company
from app.models.job import Job, JobStatus
from app.schemas.job import JobCreate, JobUpdate, JobResponse

router = APIRouter(tags=["企业-岗位管理"])


class JobListPaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    data: List[JobResponse]


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


@router.get("/", response_model=JobListPaginatedResponse)
def list_company_jobs(
    status: str = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    query = db.query(Job).filter(Job.company_id == current_company.id)

    if status:
        query = query.filter(Job.status == status)

    total = query.count()
    query = query.order_by(Job.created_at.desc())
    jobs = query.offset((page - 1) * page_size).limit(page_size).all()

    return JobListPaginatedResponse(
        total=total,
        page=page,
        page_size=page_size,
        data=jobs
    )


@router.get("/{job_id}", response_model=JobResponse)
def get_company_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.company_id == current_company.id
    ).first()
    if not job:
        raise HTTPException(status_code=404, detail="岗位不存在")
    return job


@router.post("/", response_model=JobResponse)
def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    job = Job(**job_data.model_dump(exclude={'company_id'}), company_id=current_company.id)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_data: JobUpdate,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.company_id == current_company.id
    ).first()
    if not job:
        raise HTTPException(status_code=404, detail="岗位不存在")

    for key, value in job_data.model_dump(exclude_unset=True).items():
        if key == 'status' and value:
            setattr(job, key, JobStatus(value))
        else:
            setattr(job, key, value)

    db.commit()
    db.refresh(job)
    return job


@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.company_id == current_company.id
    ).first()
    if not job:
        raise HTTPException(status_code=404, detail="岗位不存在")

    job.status = JobStatus.CLOSED
    db.commit()

    return {"message": "岗位已关闭"}


@router.post("/{job_id}/refresh")
def refresh_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.company_id == current_company.id
    ).first()
    if not job:
        raise HTTPException(status_code=404, detail="岗位不存在")

    job.created_at = db.query(Job).filter(Job.id == job_id).first().created_at
    db.commit()

    return {"message": "刷新成功"}
