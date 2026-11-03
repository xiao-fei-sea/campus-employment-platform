from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.activity import ActivityStatus, ActivityType


class CareerTalkBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    speaker_name: Optional[str] = None
    speaker_title: Optional[str] = None
    activity_type: ActivityType = ActivityType.CAREER_TALK
    start_time: datetime
    end_time: datetime
    location: str = Field(..., min_length=1, max_length=200)
    max_attendees: Optional[int] = None
    description: Optional[str] = None
    agenda: Optional[str] = None
    is_online: bool = False
    online_url: Optional[str] = None


class CareerTalkCreate(CareerTalkBase):
    pass


class AdminCareerTalkCreate(CareerTalkCreate):
    company_id: int
    status: ActivityStatus = ActivityStatus.APPROVED


class CareerTalkUpdate(BaseModel):
    title: Optional[str] = None
    speaker_name: Optional[str] = None
    speaker_title: Optional[str] = None
    activity_type: Optional[ActivityType] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    max_attendees: Optional[int] = None
    description: Optional[str] = None
    agenda: Optional[str] = None
    is_online: Optional[bool] = None
    online_url: Optional[str] = None


class CareerTalkResponse(CareerTalkBase):
    id: int
    company_id: int
    status: str
    activity_type: str
    current_attendees: int
    poster_url: Optional[str] = None
    speaker_avatar: Optional[str] = None
    approval_comment: Optional[str] = None
    approved_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CareerTalkListResponse(CareerTalkResponse):
    company_name: Optional[str] = None
    company_logo: Optional[str] = None
    is_registered: bool = False


class CareerTalkApprove(BaseModel):
    status: ActivityStatus
    comment: Optional[str] = None


class PaginatedCareerTalkResponse(BaseModel):
    activities: List[CareerTalkListResponse]
    total: int
    page: int
    page_size: int


class ActivityRegistrationBase(BaseModel):
    career_talk_id: int


class ActivityRegistrationResponse(ActivityRegistrationBase):
    id: int
    student_id: int
    status: str
    is_attended: bool
    signed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ActivityRegistrationWithDetail(ActivityRegistrationResponse):
    career_talk_title: Optional[str] = None
    student_name: Optional[str] = None
