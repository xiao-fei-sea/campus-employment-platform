from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.student import Student
from app.models.job import Job, JobStatus
from app.models.application import Application, ApplicationStatus
from app.models.company import Company, CompanyStatus
from app.models.resume import Resume
from app.schemas.statistics import StudentDashboardStats

router = APIRouter(tags=["学生-仪表盘"])


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


@router.get("/", response_model=StudentDashboardStats)
def get_student_dashboard(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    one_week_ago = datetime.now() - timedelta(days=7)

    new_jobs_this_week = db.query(Job).join(Company).filter(
        Job.status == JobStatus.APPROVED,
        Company.status == CompanyStatus.APPROVED,
        Job.created_at >= one_week_ago
    ).count()

    pending_applications = db.query(Application).filter(
        Application.student_id == current_student.id,
        Application.status == ApplicationStatus.PENDING
    ).count()

    interview_invitations = db.query(Application).filter(
        Application.student_id == current_student.id,
        Application.status == ApplicationStatus.PASSED
    ).count()

    offered_applications = db.query(Application).filter(
        Application.student_id == current_student.id,
        Application.status == ApplicationStatus.OFFERED
    ).count()

    resume_completion = 0.0
    resume = db.query(Resume).filter(Resume.student_id == current_student.id).first()
    if resume:
        completion = 0
        if resume.personal_name:
            completion += 20
        if resume.education_school:
            completion += 20
        if resume.experience_company:
            completion += 20
        if resume.project_name:
            completion += 20
        if resume.skill_names:
            completion += 20
        resume_completion = completion

    return StudentDashboardStats(
        new_jobs_this_week=new_jobs_this_week,
        pending_applications=pending_applications,
        interview_invitations=interview_invitations,
        offered_applications=offered_applications,
        resume_completion=resume_completion
    )