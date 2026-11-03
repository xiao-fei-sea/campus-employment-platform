from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.resume import ResumeVisibility


class ResumeBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    visibility: ResumeVisibility = ResumeVisibility.PUBLIC
    template: str = "default"

    personal_name: Optional[str] = None
    personal_gender: Optional[str] = None
    personal_phone: Optional[str] = None
    personal_email: Optional[EmailStr] = None
    personal_age: Optional[int] = None
    personal_city: Optional[str] = None

    education_school: Optional[str] = None
    education_major: Optional[str] = None
    education_degree: Optional[str] = None
    education_start: Optional[str] = None
    education_end: Optional[str] = None

    experience_company: Optional[str] = None
    experience_position: Optional[str] = None
    experience_duration: Optional[str] = None
    experience_description: Optional[str] = None

    skill_names: Optional[str] = None
    skill_levels: Optional[str] = None

    certificate_names: Optional[str] = None

    project_name: Optional[str] = None
    project_role: Optional[str] = None
    project_description: Optional[str] = None

    self_evaluation: Optional[str] = None
    strengths: Optional[str] = None
    education_list: Optional[str] = None
    experience_list: Optional[str] = None
    certificate_list: Optional[str] = None


class ResumeCreate(ResumeBase):
    student_id: int


class ResumeUpdate(BaseModel):
    title: Optional[str] = None
    visibility: Optional[ResumeVisibility] = None
    template: Optional[str] = None
    personal_name: Optional[str] = None
    personal_gender: Optional[str] = None
    personal_phone: Optional[str] = None
    personal_email: Optional[EmailStr] = None
    personal_age: Optional[int] = None
    personal_city: Optional[str] = None
    education_school: Optional[str] = None
    education_major: Optional[str] = None
    education_degree: Optional[str] = None
    education_start: Optional[str] = None
    education_end: Optional[str] = None
    experience_company: Optional[str] = None
    experience_position: Optional[str] = None
    experience_duration: Optional[str] = None
    experience_description: Optional[str] = None
    skill_names: Optional[str] = None
    skill_levels: Optional[str] = None
    certificate_names: Optional[str] = None
    project_name: Optional[str] = None
    project_role: Optional[str] = None
    project_description: Optional[str] = None
    self_evaluation: Optional[str] = None
    strengths: Optional[str] = None
    education_list: Optional[str] = None
    experience_list: Optional[str] = None
    certificate_list: Optional[str] = None
    attachment_url: Optional[str] = None


class ResumeResponse(ResumeBase):
    id: int
    student_id: int
    is_default: bool
    education_list: Optional[str] = None
    experience_list: Optional[str] = None
    certificate_list: Optional[str] = None
    attachment_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
