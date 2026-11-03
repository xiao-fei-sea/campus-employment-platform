from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class CompanyStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    BLACKLISTED = "blacklisted"


class CompanyScale(str, enum.Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    SUPER_LARGE = "super_large"


class CompanyIndustry(str, enum.Enum):
    IT = "it"
    FINANCE = "finance"
    MANUFACTURING = "manufacturing"
    EDUCATION = "education"
    HEALTHCARE = "healthcare"
    REAL_ESTATE = "real_estate"
    RETAIL = "retail"
    OTHER = "other"


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    name = Column(String(200), nullable=False, index=True)
    short_name = Column(String(50))
    logo = Column(String(500))
    scale = Column(SQLEnum(CompanyScale, native_enum=False, values_callable=lambda x: [e.value for e in x]), default=CompanyScale.MEDIUM, index=True)
    industry = Column(SQLEnum(CompanyIndustry, native_enum=False, values_callable=lambda x: [e.value for e in x]), default=CompanyIndustry.OTHER, index=True)
    status = Column(SQLEnum(CompanyStatus, native_enum=False, values_callable=lambda x: [e.value for e in x]), default=CompanyStatus.PENDING, index=True)
    license_no = Column(String(50))
    license_url = Column(String(500))
    contact_name = Column(String(50))
    contact_phone = Column(String(20))
    contact_email = Column(String(100))
    province = Column(String(50))
    city = Column(String(50))
    district = Column(String(50))
    address = Column(String(500))
    description = Column(Text)
    website = Column(String(200))
    verified_at = Column(DateTime(timezone=True))
    verified_by = Column(Integer, ForeignKey("users.id"))
    rejection_reason = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    jobs = relationship("Job", back_populates="company")
    career_talks = relationship("CareerTalk", back_populates="company")
    user = relationship("User", back_populates="company_profile", foreign_keys=[user_id])
