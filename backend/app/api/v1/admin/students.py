from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_roles, get_password_hash
from app.models.user import User, UserRole
from app.models.student import Student, EmploymentStatus
from app.models.application import Application
from app.models.company import Company
from app.models.job import Job
from app.models.resume import Resume
from app.schemas.student import StudentResponse, StudentUpdate, PaginatedStudentResponse, AdminStudentCreate

router = APIRouter(tags=["管理端-学生管理"])


@router.post("", response_model=StudentResponse, status_code=201)
@router.post("/", response_model=StudentResponse, status_code=201)
def create_student(
    data: AdminStudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.COUNSELOR))
):
    if db.query(Student).filter(Student.student_no == data.student_no).first():
        raise HTTPException(status_code=400, detail="学号已存在")

    username = data.username or data.student_no
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="登录名已存在")

    email = data.email or f"{data.student_no}@campus.edu.cn"

    user = User(
        username=username,
        email=email,
        hashed_password=get_password_hash(data.password),
        role=UserRole.STUDENT,
        is_active=True
    )
    db.add(user)
    db.flush()

    student = Student(
        user_id=user.id,
        student_no=data.student_no,
        name=data.name,
        gender=data.gender,
        phone=data.phone,
        college=data.college,
        major=data.major,
        class_name=data.class_name,
        graduation_year=data.graduation_year,
        employment_status=data.employment_status
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@router.get("", response_model=PaginatedStudentResponse)
@router.get("/", response_model=PaginatedStudentResponse)
def list_students(
    employment_status: str = None,
    college: str = None,
    major: str = None,
    education_degree: str = None,
    graduation_year: int = None,
    is_key_assistance: bool = None,
    keyword: str = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=10000),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.COUNSELOR))
):
    query = db.query(Student)

    if employment_status:
        query = query.filter(Student.employment_status == employment_status)

    if college:
        query = query.filter(Student.college.contains(college))

    if major:
        query = query.filter(Student.major.contains(major))

    if education_degree:
        query = query.join(Resume, Student.id == Resume.student_id).filter(
            Resume.education_degree == education_degree
        )

    if graduation_year:
        query = query.filter(Student.graduation_year == graduation_year)

    if is_key_assistance is not None:
        query = query.filter(Student.is_key_assistance == is_key_assistance)

    if keyword:
        query = query.filter(
            Student.name.contains(keyword) |
            Student.student_no.contains(keyword)
        )

    total = query.count()

    query = query.order_by(Student.created_at.desc())
    students = query.offset((page - 1) * page_size).limit(page_size).all()

    student_responses = []
    for s in students:
        education_degree = None
        company_name = None
        salary = None

        if s.resumes and len(s.resumes) > 0:
            education_degree = s.resumes[0].education_degree

        if s.employment_status in [EmploymentStatus.OFFERED, EmploymentStatus.SIGNED]:
            accepted_app = db.query(Application).filter(
                Application.student_id == s.id
            ).order_by(Application.updated_at.desc()).first()

            if accepted_app:
                salary = accepted_app.offer_salary
                job = db.query(Job).filter(Job.id == accepted_app.job_id).first()
                if job:
                    company = db.query(Company).filter(Company.id == job.company_id).first()
                    if company:
                        company_name = company.name

        status_value = s.employment_status.value if hasattr(s.employment_status, 'value') else s.employment_status
        student_responses.append(StudentResponse(
            id=s.id,
            user_id=s.user_id,
            student_no=s.student_no,
            name=s.name,
            gender=s.gender,
            phone=s.phone,
            major=s.major,
            college=s.college,
            class_name=s.class_name,
            graduation_year=s.graduation_year,
            employment_status=status_value,
            is_key_assistance=s.is_key_assistance,
            assistance_note=s.assistance_note,
            avatar=s.avatar,
            resume_url=s.resume_url,
            created_at=s.created_at,
            education_degree=education_degree,
            company_name=company_name,
            salary=salary
        ))

    return PaginatedStudentResponse(
        students=student_responses,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.COUNSELOR))
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="学生不存在")
    return student


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.COUNSELOR))
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="学生不存在")

    for key, value in student_data.model_dump(exclude_unset=True).items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student


@router.get("/{student_id}/employment-status/update", response_model=StudentResponse)
def update_employment_status(
    student_id: int,
    status: EmploymentStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.COUNSELOR))
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="学生不存在")

    student.employment_status = status
    db.commit()
    db.refresh(student)

    return student
