from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class EmploymentStatus(str, enum.Enum):
    UNEMPLOYED = "unemployed"
    SEARCHING = "searching"
    OFFERED = "offered"
    SIGNED = "signed"
    FURTHER_STUDY = "further_study"
    STARTUP = "startup"


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    student_no = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(50), nullable=False, index=True)
    gender = Column(String(10))
    phone = Column(String(20), index=True)
    avatar = Column(String(500))
    major = Column(String(100), index=True)
    college = Column(String(100), index=True)
    class_name = Column(String(50))
    graduation_year = Column(Integer, index=True)
    employment_status = Column(SQLEnum(EmploymentStatus, native_enum=False, values_callable=lambda x: [e.value for e in x]), default=EmploymentStatus.SEARCHING, index=True)
    is_key_assistance = Column(Boolean, default=False)
    assistance_note = Column(Text)
    resume_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="student_profile")
    resumes = relationship("Resume", back_populates="student")
    applications = relationship("Application", back_populates="student")
    activity_registrations = relationship("ActivityRegistration", back_populates="student")
    favorites = relationship("JobFavorite", back_populates="student", cascade="all, delete-orphan")
