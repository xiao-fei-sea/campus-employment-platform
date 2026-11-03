from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class ActivityStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    ENDED = "ended"


class ActivityType(str, enum.Enum):
    CAREER_TALK = "career_talk"
    JOB_FAIR = "job_fair"
    RECRUITMENT = "recruitment"


class CareerTalk(Base):
    __tablename__ = "career_talks"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    title = Column(String(200), nullable=False)
    speaker_name = Column(String(50))
    speaker_title = Column(String(100))
    speaker_avatar = Column(String(500))
    status = Column(SQLEnum(ActivityStatus, native_enum=False, values_callable=lambda x: [e.value for e in x]), default=ActivityStatus.PENDING)
    activity_type = Column(SQLEnum(ActivityType, native_enum=False, values_callable=lambda x: [e.value for e in x]), default=ActivityType.CAREER_TALK)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    location = Column(String(200), nullable=False)
    max_attendees = Column(Integer)
    current_attendees = Column(Integer, default=0)
    description = Column(Text)
    agenda = Column(Text)
    poster_url = Column(String(500))
    is_online = Column(Boolean, default=False)
    online_url = Column(String(500))
    approval_comment = Column(Text)
    approved_at = Column(DateTime(timezone=True))
    approved_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    company = relationship("Company", back_populates="career_talks")
    registrations = relationship("ActivityRegistration", back_populates="career_talk")


class ActivityRegistration(Base):
    __tablename__ = "activity_registrations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    career_talk_id = Column(Integer, ForeignKey("career_talks.id"), nullable=False)
    status = Column(String(20), default="registered")
    is_attended = Column(Boolean, default=False)
    signed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="activity_registrations")
    career_talk = relationship("CareerTalk", back_populates="registrations")
