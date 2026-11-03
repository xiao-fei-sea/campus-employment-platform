from pydantic import BaseModel
from typing import List, Dict


class DashboardStats(BaseModel):
    total_students: int
    total_companies: int
    total_jobs: int
    total_applications: int
    employment_rate: float
    job_supply_demand_ratio: float
    employed_count: int = 0
    signed_count: int = 0
    offered_count: int = 0
    searching_count: int = 0
    further_study_count: int = 0
    unemployed_count: int = 0
    startup_count: int = 0
    need_help_count: int = 0
    avg_offer_salary: float = 0.0
    pending_company_count: int = 0
    pending_job_count: int = 0
    recent_applications: List[Dict] = []
    popular_jobs: List[Dict] = []
    company_industry_distribution: List[Dict] = []
    employment_trend: List[Dict] = []


class StudentDashboardStats(BaseModel):
    new_jobs_this_week: int = 0
    pending_applications: int = 0
    interview_invitations: int = 0
    offered_applications: int = 0
    resume_completion: float = 0.0
