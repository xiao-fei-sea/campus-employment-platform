from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.student import Student
from app.models.resume import Resume
from app.schemas.resume import ResumeCreate, ResumeUpdate, ResumeResponse

router = APIRouter(tags=["学生-简历管理"])


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


@router.get("/", response_model=List[ResumeResponse])
def list_resumes(
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    resumes = db.query(Resume).filter(Resume.student_id == current_student.id).all()
    return resumes


@router.get("/{resume_id}", response_model=ResumeResponse)
def get_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.student_id == current_student.id
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="简历不存在")
    return resume


@router.post("/{resume_id}/suggestions")
async def get_resume_suggestions(
    resume_id: int,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    from app.services.llm_service import llm_service

    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.student_id == current_student.id
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="简历不存在")

    resume_data = {
        'name': resume.personal_name or '',
        'phone': resume.personal_phone or '',
        'email': resume.personal_email or '',
        'educationList': [],
        'experienceList': [],
        'skillList': [],
        'certificateList': [],
        'strengths': resume.strengths or ''
    }

    if resume.education_list:
        try:
            resume_data['educationList'] = eval(resume.education_list)
        except:
            pass

    if resume.experience_list:
        try:
            resume_data['experienceList'] = eval(resume.experience_list)
        except:
            pass

    if resume.skill_names:
        resume_data['skillList'] = [s.strip() for s in resume.skill_names.split(',')]

    if resume.certificate_list:
        try:
            certs = eval(resume.certificate_list)
            if isinstance(certs, list):
                resume_data['certificateList'] = certs
        except:
            pass

    suggestions = await llm_service.generate_resume_suggestions(resume_data)

    if not suggestions:
        return {
            "suggestions": [
                "建议完善教育经历信息",
                "建议添加实习或项目经验",
                "建议补充专业技能证书",
                "建议填写个人优势展示"
            ]
        }

    return {"suggestions": suggestions}


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    resume_id: int = None,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_user)
):
    import os
    import uuid

    if not file:
        raise HTTPException(status_code=400, detail="请选择文件")

    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="仅支持 PDF 格式")

    if file.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="文件大小不能超过 10MB")

    upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "uploads", "resumes")
    os.makedirs(upload_dir, exist_ok=True)

    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4().hex}{file_ext}"
    file_path = os.path.join(upload_dir, unique_filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    file_url = f"/uploads/resumes/{unique_filename}"

    if resume_id:
        resume = db.query(Resume).filter(
            Resume.id == resume_id,
            Resume.student_id == current_student.id
        ).first()
        if resume:
            resume.attachment_url = file_url
            db.commit()

    return {"url": file_url, "filename": unique_filename}


@router.post("/", response_model=ResumeResponse)
def create_resume(
    resume_data: ResumeCreate,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    resume = Resume(**resume_data.model_dump(), student_id=current_student.id)
    db.add(resume)

    is_first = db.query(Resume).filter(Resume.student_id == current_student.id).count() == 0
    if is_first:
        resume.is_default = True

    db.commit()
    db.refresh(resume)
    return resume


@router.put("/{resume_id}", response_model=ResumeResponse)
def update_resume(
    resume_id: int,
    resume_data: ResumeUpdate,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.student_id == current_student.id
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="简历不存在")

    for key, value in resume_data.model_dump(exclude_unset=True).items():
        setattr(resume, key, value)

    db.commit()
    db.refresh(resume)
    return resume


@router.delete("/{resume_id}")
def delete_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.student_id == current_student.id
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="简历不存在")

    was_default = resume.is_default
    db.delete(resume)
    db.commit()

    if was_default:
        first_resume = db.query(Resume).filter(
            Resume.student_id == current_student.id
        ).first()
        if first_resume:
            first_resume.is_default = True
            db.commit()

    return {"message": "删除成功"}


@router.post("/{resume_id}/set-default")
def set_default_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.student_id == current_student.id
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="简历不存在")

    db.query(Resume).filter(Resume.student_id == current_student.id).update({"is_default": False})
    resume.is_default = True
    db.commit()

    return {"message": "设置成功"}
