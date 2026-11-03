from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)
    role: UserRole = UserRole.STUDENT


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    password: Optional[str] = Field(default=None, min_length=6, max_length=100)
    is_active: Optional[bool] = None


class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6, max_length=100)


class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str
    role: str


class PhoneLogin(BaseModel):
    phone: str = Field(..., pattern=r'^1[3-9]\d{9}$')
    password: Optional[str] = None
    code: Optional[str] = None
    login_method: str = Field(default="phone_password")


class SmsSendRequest(BaseModel):
    phone: str = Field(..., pattern=r'^1[3-9]\d{9}$')


class SmsCodeResponse(BaseModel):
    success: bool
    message: str


class WeChatQRCodeResponse(BaseModel):
    qrcode: str
    scene: str
    expire_in: int = 300


class WeChatQRStatusResponse(BaseModel):
    status: str
    token: Optional[str] = None
    user_info: Optional[dict] = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserWithProfile(UserBase):
    id: int
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    student_profile: Optional[dict] = None
    company_profile: Optional[dict] = None

    class Config:
        from_attributes = True
