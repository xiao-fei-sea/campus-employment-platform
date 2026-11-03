from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.company import Company
from app.schemas.company import CompanyUpdate, CompanyResponse
import os
import uuid
import shutil

router = APIRouter(tags=["企业-企业信息"])


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


@router.get("/", response_model=CompanyResponse)
def get_company_profile(
    current_company: Company = Depends(get_current_company)
):
    return current_company


@router.put("/", response_model=CompanyResponse)
def update_company_profile(
    profile_data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    for key, value in profile_data.model_dump(exclude_unset=True).items():
        setattr(current_company, key, value)

    db.commit()
    db.refresh(current_company)
    return current_company


@router.post("/logo", status_code=status.HTTP_200_OK)
def upload_company_logo(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只能上传图片文件"
        )

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    uploads_dir = os.path.join(base_dir, "uploads", "logos")
    os.makedirs(uploads_dir, exist_ok=True)

    file_ext = os.path.splitext(file.filename)[1] if file.filename else ".png"
    file_name = f"{uuid.uuid4().hex}{file_ext}"
    file_path = os.path.join(uploads_dir, file_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    logo_url = f"/uploads/logos/{file_name}"
    current_company.logo = logo_url
    db.commit()
    db.refresh(current_company)

    return {"url": logo_url}
