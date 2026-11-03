from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.application import ApplicationStatus


class ApplicationBase(BaseModel):
    job_id: int
    resume_id: int
    cover_letter: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    student_id: int


class ApplicationResponse(ApplicationBase):
    id: int
    student_id: int
    status: ApplicationStatus
    interview_time: Optional[datetime] = None
    interview_location: Optional[str] = None
    offer_salary: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ApplicationListResponse(ApplicationResponse):
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    company_logo: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    salary_show: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    student_name: Optional[str] = None
    avatar: Optional[str] = None
    school: Optional[str] = None
    major: Optional[str] = None
    education: Optional[str] = None
    resume_title: Optional[str] = None
