from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
import random
import qrcode
import io
import base64
import uuid

from app.core.database import get_db
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user
)
from app.core.config import settings
from app.core.rate_limit import rate_limit
from app.models.user import User, UserRole
from app.models.student import Student
from app.schemas.user import PasswordChange
from app.models.company import Company
from app.schemas.user import UserCreate, UserResponse, Token, UserLogin, UserWithProfile, PhoneLogin, SmsSendRequest, SmsCodeResponse, WeChatQRCodeResponse, WeChatQRStatusResponse
from app.models.preference import UserPreference
import json

router = APIRouter(tags=["认证"])

sms_codes_store = {}
wechat_qr_store = {}


@router.post("/register", response_model=UserResponse, dependencies=[Depends(rate_limit("register", 5, 60))])
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名或邮箱已存在"
        )

    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        role=user_data.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    if user.role == UserRole.STUDENT:
        student = Student(
            user_id=user.id,
            student_no=user_data.username,
            name="新用户"
        )
        db.add(student)
        db.commit()
    elif user.role == UserRole.COMPANY:
        company = Company(
            user_id=user.id,
            name="待完善企业"
        )
        db.add(company)
        db.commit()

    return user


@router.post("/login", response_model=Token, dependencies=[Depends(rate_limit("login", 10, 60))])
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已被禁用"
        )
    if user.role.value != user_data.role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户类型不匹配"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


from app.models.student import EmploymentStatus
from app.models.company import CompanyStatus, Company
from app.models.job import Job, JobStatus
from app.schemas.statistics import DashboardStats


@router.get("/public/stats", response_model=DashboardStats)
def get_public_stats(db: Session = Depends(get_db)):
    total_students = db.query(Student).count()
    total_companies = db.query(Company).filter(Company.status == CompanyStatus.APPROVED).count()
    total_jobs = db.query(Job).filter(Job.status == JobStatus.APPROVED).count()

    signed_count = db.query(Student).filter(
        Student.employment_status == EmploymentStatus.SIGNED
    ).count()
    offered_count = db.query(Student).filter(
        Student.employment_status == EmploymentStatus.OFFERED
    ).count()
    employed_count = signed_count + offered_count

    employment_rate = (employed_count / total_students * 100) if total_students > 0 else 0

    return DashboardStats(
        total_students=total_students,
        total_companies=total_companies,
        total_jobs=total_jobs,
        total_applications=0,
        employment_rate=round(employment_rate, 2),
        job_supply_demand_ratio=0.0,
        employed_count=employed_count,
        signed_count=signed_count,
        offered_count=offered_count,
        searching_count=0,
        further_study_count=0,
        unemployed_count=0,
        startup_count=0,
        need_help_count=0,
        avg_offer_salary=0.0,
        pending_company_count=0,
        pending_job_count=0
    )


@router.get("/wechat/qrcode", response_model=WeChatQRCodeResponse)
def get_wechat_qrcode(db: Session = Depends(get_db)):
    scene = f"wechat_login_{uuid.uuid4().hex}"
    expire_time = datetime.now().timestamp() + 300

    wechat_qr_store[scene] = {
        "status": "pending",
        "expire_time": expire_time,
        "created_at": datetime.now().timestamp()
    }

    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(scene)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#22c55e", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qrcode_base64 = base64.b64encode(buffer.getvalue()).decode()

    return {
        "qrcode": f"data:image/png;base64,{qrcode_base64}",
        "scene": scene,
        "expire_in": 300
    }


@router.get("/wechat/qrstatus/{scene}", response_model=WeChatQRStatusResponse)
def get_wechat_qrstatus(scene: str, db: Session = Depends(get_db)):
    if scene not in wechat_qr_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="二维码已过期或不存在"
        )

    qr_data = wechat_qr_store[scene]
    current_time = datetime.now().timestamp()

    if current_time > qr_data["expire_time"]:
        del wechat_qr_store[scene]
        return {"status": "expired"}

    if qr_data["status"] == "confirmed" and "user_id" in qr_data:
        user = db.query(User).filter(User.id == qr_data["user_id"]).first()
        if user:
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": str(user.id)},
                expires_delta=access_token_expires
            )
            del wechat_qr_store[scene]
            return {
                "status": "confirmed",
                "token": access_token,
                "user_info": {
                    "id": user.id,
                    "username": user.username,
                    "role": user.role.value if hasattr(user.role, 'value') else str(user.role)
                }
            }

    return {"status": qr_data["status"]}


@router.post("/login/json", response_model=Token, dependencies=[Depends(rate_limit("login", 10, 60))])
def login_json(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已被禁用"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/password")
def change_password(
    data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="原密码错误")
    if data.old_password == data.new_password:
        raise HTTPException(status_code=400, detail="新密码不能与原密码相同")

    current_user.hashed_password = get_password_hash(data.new_password)
    db.commit()
    return {"message": "密码修改成功"}


@router.get("/preferences")
def get_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    preference = db.query(UserPreference).filter(
        UserPreference.user_id == current_user.id
    ).first()
    if not preference:
        return {}
    try:
        return json.loads(preference.data)
    except json.JSONDecodeError:
        return {}


@router.put("/preferences")
def save_preferences(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    preference = db.query(UserPreference).filter(
        UserPreference.user_id == current_user.id
    ).first()
    if not preference:
        preference = UserPreference(user_id=current_user.id)
        db.add(preference)

    preference.data = json.dumps(data, ensure_ascii=False)
    db.commit()
    return data


@router.get("/me", response_model=UserWithProfile)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    user_data = {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role),
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified,
        "created_at": current_user.created_at,
        "student_profile": None,
        "company_profile": None
    }

    if current_user.role == UserRole.STUDENT and current_user.student_profile:
        user_data["student_profile"] = {
            "id": current_user.student_profile.id,
            "name": current_user.student_profile.name,
            "student_no": current_user.student_profile.student_no,
            "major": current_user.student_profile.major,
            "class_name": current_user.student_profile.class_name,
            "avatar": current_user.student_profile.avatar,
            "phone": current_user.student_profile.phone,
            "gender": current_user.student_profile.gender,
            "graduation_year": current_user.student_profile.graduation_year,
            "employment_status": current_user.student_profile.employment_status.value if current_user.student_profile.employment_status else None
        }

    if current_user.role == UserRole.COMPANY and current_user.company_profile:
        user_data["company_profile"] = {
            "id": current_user.company_profile.id,
            "name": current_user.company_profile.name,
            "industry": current_user.company_profile.industry.value if current_user.company_profile.industry else None,
            "scale": current_user.company_profile.scale.value if current_user.company_profile.scale else None,
            "logo": current_user.company_profile.logo,
            "contact_phone": current_user.company_profile.contact_phone,
            "description": current_user.company_profile.description
        }

    return user_data


@router.post("/sms/send", response_model=SmsCodeResponse, dependencies=[Depends(rate_limit("sms", 3, 60))])
def send_sms_code(request: SmsSendRequest, db: Session = Depends(get_db)):
    phone = request.phone

    student = db.query(Student).filter(Student.phone == phone).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="该手机号未注册"
        )

    code = str(random.randint(100000, 999999))
    sms_codes_store[phone] = code

    print(f"[SMS] 验证码已发送至 {phone}: {code}")

    return {"success": True, "message": "验证码已发送"}


@router.post("/phone/login", response_model=Token, dependencies=[Depends(rate_limit("phone_login", 10, 60))])
def phone_login(request: PhoneLogin, db: Session = Depends(get_db)):
    phone = request.phone

    student = db.query(Student).filter(Student.phone == phone).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="该手机号未注册"
        )

    user = student.user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    if request.login_method == "phone_password":
        if not request.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="请输入密码"
            )
        if not verify_password(request.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="密码错误"
            )
    else:
        if not request.code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="请输入验证码"
            )
        stored_code = sms_codes_store.get(phone)
        if not stored_code or stored_code != request.code:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="验证码错误"
            )
        del sms_codes_store[phone]

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已被禁用"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
