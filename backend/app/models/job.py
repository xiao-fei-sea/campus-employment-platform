from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class JobStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CLOSED = "closed"


class JobType(str, enum.Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    INTERNSHIP = "internship"
    PRACTICE = "practice"


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False, index=True)
    job_type = Column(SQLEnum(JobType, native_enum=False, values_callable=lambda x: [e.value for e in x]), default=JobType.FULL_TIME)
    status = Column(SQLEnum(JobStatus, native_enum=False, values_callable=lambda x: [e.value for e in x]), default=JobStatus.PENDING, index=True)
    salary_min = Column(Integer, index=True)
    salary_max = Column(Integer)
    salary_show = Column(String(50))
    province = Column(String(50))
    city = Column(String(50))
    district = Column(String(50))
    address = Column(String(500))
    description = Column(Text)
    requirement = Column(Text)
    benefit = Column(Text)
    skills = Column(Text)
    headcount = Column(Integer, default=1)
    experience = Column(String(100))
    education = Column(String(50))
    application_count = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    is_top = Column(Boolean, default=False)
    is_highlight = Column(Boolean, default=False)
    is_urgent = Column(Boolean, default=False)
    is_campus_recruit = Column(Boolean, default=False)
    rejection_reason = Column(Text)
    approved_at = Column(DateTime(timezone=True))
    approved_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    expired_at = Column(DateTime(timezone=True))

    company = relationship("Company", back_populates="jobs")
    applications = relationship("Application", back_populates="job")
    favorites = relationship("JobFavorite", back_populates="job", cascade="all, delete-orphan")


class JobFavorite(Base):
    __tablename__ = "job_favorites"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    job = relationship("Job", back_populates="favorites")
    student = relationship("Student", back_populates="favorites")
