from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.job import JobStatus, JobType


class JobBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    job_type: JobType = JobType.FULL_TIME
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_show: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    requirement: Optional[str] = None
    benefit: Optional[str] = None
    skills: Optional[str] = None
    headcount: int = 1
    experience: Optional[str] = None
    education: Optional[str] = None


class JobCreate(JobBase):
    expired_at: Optional[datetime] = None


class JobUpdate(BaseModel):
    title: Optional[str] = None
    job_type: Optional[JobType] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_show: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    requirement: Optional[str] = None
    benefit: Optional[str] = None
    skills: Optional[str] = None
    headcount: Optional[int] = None
    expired_at: Optional[datetime] = None
    status: Optional[str] = None


class JobResponse(JobBase):
    id: int
    company_id: int
    status: JobStatus
    application_count: int
    view_count: int
    is_top: bool
    is_highlight: bool
    rejection_reason: Optional[str] = None
    approved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    company_name: Optional[str] = None
    company_logo: Optional[str] = None
    industry: Optional[str] = None

    class Config:
        from_attributes = True


class JobListResponse(JobResponse):
    company_name: Optional[str] = None
    company_logo: Optional[str] = None
    is_favorited: Optional[bool] = False
    has_applied: Optional[bool] = False
    is_urgent: Optional[bool] = False
    is_campus_recruit: Optional[bool] = False
    favorited_at: Optional[datetime] = None


class PaginatedJobResponse(BaseModel):
    jobs: List[JobResponse]
    total: int
    page: int
    page_size: int


class JobListWithTotalResponse(BaseModel):
    total: int
    page: int
    page_size: int
    data: List[JobListResponse]


class JobApprove(BaseModel):
    status: JobStatus
    comment: Optional[str] = None
