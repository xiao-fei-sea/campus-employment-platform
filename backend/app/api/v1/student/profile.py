from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
import os
import uuid

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.student import Student
from app.schemas.student import StudentUpdate, StudentResponse

router = APIRouter(tags=["学生-个人信息"])


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


@router.get("/")
def get_profile(
    current_student: Student = Depends(get_current_student),
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_student.id,
        "user_id": current_student.user_id,
        "student_no": current_student.student_no,
        "name": current_student.name,
        "gender": current_student.gender,
        "phone": current_student.phone,
        "avatar": current_student.avatar,
        "major": current_student.major,
        "class_name": current_student.class_name,
        "graduation_year": current_student.graduation_year,
        "employment_status": current_student.employment_status,
        "is_key_assistance": current_student.is_key_assistance,
        "created_at": current_student.created_at,
        "email": current_user.email
    }


@router.put("/", response_model=StudentResponse)
def update_profile(
    profile_data: StudentUpdate,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    for key, value in profile_data.model_dump(exclude_unset=True).items():
        setattr(current_student, key, value)

    db.commit()
    db.refresh(current_student)
    return current_student


@router.post("/avatar", status_code=status.HTTP_200_OK)
async def upload_avatar(
    file: UploadFile = File(...),
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="只能上传图片文件")

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    avatars_dir = os.path.join(base_dir, "uploads", "avatars")
    os.makedirs(avatars_dir, exist_ok=True)

    file_ext = os.path.splitext(file.filename)[1] if file.filename else '.jpg'
    file_name = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(avatars_dir, file_name)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    avatar_url = f"/uploads/avatars/{file_name}"
    current_student.avatar = avatar_url
    db.commit()

    return {"url": avatar_url}
