from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.core.security import require_roles
from app.models.user import User, UserRole
from app.models.company import Company, CompanyStatus
from app.models.job import Job
from app.schemas.company import CompanyResponse, PaginatedCompanyResponse

router = APIRouter(tags=["管理端-企业管理"])


@router.get("", response_model=PaginatedCompanyResponse)
@router.get("/", response_model=PaginatedCompanyResponse)
def list_companies(
    status: str = None,
    keyword: str = None,
    industry: str = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    query = db.query(Company)

    if status:
        query = query.filter(Company.status == status)

    if keyword:
        query = query.filter(
            Company.name.contains(keyword) |
            Company.short_name.contains(keyword)
        )

    if industry:
        query = query.filter(Company.industry == industry)

    total = query.count()

    query = query.order_by(Company.created_at.desc())
    companies = query.offset((page - 1) * page_size).limit(page_size).all()

    company_responses = []
    for c in companies:
        jobs = db.query(Job).filter(Job.company_id == c.id).all()
        job_titles = [job.title for job in jobs]
        company_data = CompanyResponse(
            id=c.id,
            user_id=c.user_id,
            name=c.name,
            short_name=c.short_name,
            logo=c.logo,
            scale=c.scale,
            industry=c.industry,
            status=c.status,
            license_no=c.license_no,
            license_url=c.license_url,
            contact_name=c.contact_name,
            contact_phone=c.contact_phone,
            contact_email=c.contact_email,
            province=c.province,
            city=c.city,
            district=c.district,
            address=c.address,
            description=c.description,
            website=c.website,
            verified_at=c.verified_at,
            rejection_reason=c.rejection_reason,
            created_at=c.created_at,
            join_time=c.created_at.strftime("%Y-%m-%d") if c.created_at else "",
            job_count=len(jobs),
            job_titles=job_titles
        )
        company_responses.append(company_data)

    return PaginatedCompanyResponse(
        companies=company_responses,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="企业不存在")
    return company


@router.post("/{company_id}/approve")
def approve_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="企业不存在")

    company.status = CompanyStatus.APPROVED
    company.verified_at = datetime.now()
    company.verified_by = current_user.id

    db.commit()

    return {"message": "审核完成"}


@router.post("/{company_id}/reject")
def reject_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="企业不存在")

    company.status = CompanyStatus.REJECTED
    company.rejection_reason = "不符合入驻条件"
    db.commit()

    return {"message": "已拒绝"}


@router.post("/{company_id}/blacklist")
def blacklist_company(
    company_id: int,
    reason: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="企业不存在")

    company.status = CompanyStatus.BLACKLISTED
    company.rejection_reason = reason
    db.commit()

    return {"message": "已加入黑名单"}


@router.delete("/{company_id}/remove-blacklist")
def remove_from_blacklist(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="企业不存在")

    company.status = CompanyStatus.APPROVED
    db.commit()

    return {"message": "已移出黑名单"}
