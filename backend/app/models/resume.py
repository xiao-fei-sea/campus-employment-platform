from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class ResumeVisibility(str, enum.Enum):
    PUBLIC = "public"
    PROTECTED = "protected"
    PRIVATE = "private"


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    title = Column(String(100), nullable=False)
    is_default = Column(Boolean, default=False)
    visibility = Column(SQLEnum(ResumeVisibility, native_enum=False, values_callable=lambda x: [e.value for e in x]), default=ResumeVisibility.PUBLIC)
    template = Column(String(50), default="default")

    personal_name = Column(String(50))
    personal_gender = Column(String(10))
    personal_phone = Column(String(20))
    personal_email = Column(String(100))
    personal_age = Column(Integer)
    personal_city = Column(String(50))

    education_school = Column(String(100))
    education_major = Column(String(100))
    education_degree = Column(String(20))
    education_start = Column(String(20))
    education_end = Column(String(20))

    experience_company = Column(String(100))
    experience_position = Column(String(100))
    experience_duration = Column(String(50))
    experience_description = Column(Text)

    skill_names = Column(Text)
    skill_levels = Column(Text)

    certificate_names = Column(Text)

    project_name = Column(String(100))
    project_role = Column(String(50))
    project_description = Column(Text)

    self_evaluation = Column(Text)
    strengths = Column(Text)

    education_list = Column(Text)
    experience_list = Column(Text)
    certificate_list = Column(Text)

    attachment_url = Column(String(500))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    student = relationship("Student", back_populates="resumes")
    applications = relationship("Application", back_populates="resume")
