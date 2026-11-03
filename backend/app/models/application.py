from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class ApplicationStatus(str, enum.Enum):
    PENDING = "pending"
    VIEWED = "viewed"
    PASSED = "passed"
    FAILED = "failed"
    OFFERED = "offered"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    status = Column(SQLEnum(ApplicationStatus, native_enum=False, values_callable=lambda x: [e.value for e in x]), default=ApplicationStatus.PENDING, index=True)
    cover_letter = Column(Text)
    interview_time = Column(DateTime(timezone=True))
    interview_location = Column(String(500))
    interview_result = Column(Text)
    offer_salary = Column(Integer)
    offer_letter_url = Column(String(500))
    feedback = Column(Text)
    viewed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    student = relationship("Student", back_populates="applications")
    job = relationship("Job", back_populates="applications")
    resume = relationship("Resume", back_populates="applications")
