from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models.student import EmploymentStatus


class StudentBase(BaseModel):
    student_no: str = Field(..., min_length=5, max_length=20)
    name: Optional[str] = Field(default="", max_length=50)
    gender: Optional[str] = None
    phone: Optional[str] = None
    major: Optional[str] = None
    college: Optional[str] = None
    class_name: Optional[str] = None
    graduation_year: Optional[int] = None


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    major: Optional[str] = None
    college: Optional[str] = None
    class_name: Optional[str] = None
    graduation_year: Optional[int] = None
    employment_status: Optional[EmploymentStatus] = None
    is_key_assistance: Optional[bool] = None
    assistance_note: Optional[str] = None
    resume_url: Optional[str] = None


class AdminStudentCreate(BaseModel):
    student_no: str = Field(..., min_length=1, max_length=20)
    name: str = Field(..., min_length=1, max_length=50)
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str = Field(default="123456", min_length=6, max_length=100)
    gender: Optional[str] = None
    phone: Optional[str] = None
    college: Optional[str] = None
    major: Optional[str] = None
    class_name: Optional[str] = None
    graduation_year: Optional[int] = None
    employment_status: EmploymentStatus = EmploymentStatus.SEARCHING


class StudentResponse(StudentBase):
    id: int
    user_id: int
    employment_status: str
    is_key_assistance: bool
    avatar: Optional[str] = None
    created_at: datetime
    education_degree: Optional[str] = None
    company_name: Optional[str] = None
    salary: Optional[int] = None

    class Config:
        from_attributes = True


class PaginatedStudentResponse(BaseModel):
    students: List[StudentResponse]
    total: int
    page: int
    page_size: int
