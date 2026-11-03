from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from app.models.company import CompanyStatus, CompanyScale, CompanyIndustry


class CompanyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    short_name: Optional[str] = None
    scale: CompanyScale = CompanyScale.MEDIUM
    industry: CompanyIndustry = CompanyIndustry.OTHER
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    province: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None


class CompanyUpdate(BaseModel):
    short_name: Optional[str] = None
    logo: Optional[str] = None
    scale: Optional[CompanyScale] = None
    industry: Optional[CompanyIndustry] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    province: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None


class CompanyResponse(CompanyBase):
    id: int
    user_id: int
    logo: Optional[str] = None
    status: CompanyStatus
    license_no: Optional[str] = None
    license_url: Optional[str] = None
    verified_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    created_at: datetime
    join_time: Optional[str] = None
    job_count: Optional[int] = 0
    job_titles: Optional[List[str]] = []

    class Config:
        from_attributes = True


class CompanyApprove(BaseModel):
    status: CompanyStatus
    comment: Optional[str] = None


class PaginatedCompanyResponse(BaseModel):
    companies: List[CompanyResponse]
    total: int
    page: int
    page_size: int
