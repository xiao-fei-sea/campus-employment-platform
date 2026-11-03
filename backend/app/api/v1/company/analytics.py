from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from pydantic import BaseModel
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.company import Company
from app.models.job import Job
from app.models.application import Application, ApplicationStatus
from app.models.resume import Resume
from app.models.student import Student
from app.models.activity import CareerTalk, ActivityStatus
from app.services.analytics_helpers import calc_period_growth, build_time_series

router = APIRouter(tags=["企业-数据统计"])

GROWTH_DAYS = 30


def _count_company_applications(db: Session, company_id: int, start: datetime, end: datetime) -> int:
    return db.query(func.count(Application.id)).join(
        Job, Application.job_id == Job.id
    ).filter(
        Job.company_id == company_id,
        Application.created_at >= start,
        Application.created_at < end,
    ).scalar() or 0


def _count_company_interviews(db: Session, company_id: int, start: datetime, end: datetime) -> int:
    return db.query(func.count(Application.id)).join(
        Job, Application.job_id == Job.id
    ).filter(
        Job.company_id == company_id,
        Application.interview_time.isnot(None),
        Application.interview_time >= start,
        Application.interview_time < end,
    ).scalar() or 0


def _application_growth(db: Session, company_id: int, days: int = GROWTH_DAYS) -> float:
    now = datetime.now()
    cur_start = now - timedelta(days=days)
    prev_start = now - timedelta(days=days * 2)
    current = _count_company_applications(db, company_id, cur_start, now)
    previous = _count_company_applications(db, company_id, prev_start, cur_start)
    return calc_period_growth(current, previous)


def get_current_company_user(current_user: User = Depends(get_current_user)) -> Company:
    if current_user.role != UserRole.COMPANY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="仅企业可以访问此功能"
        )
    company = current_user.company_profile
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业信息不存在"
        )
    return company


class DashboardStatsResponse(BaseModel):
    job_views: int
    job_views_growth: float
    received_resumes: int
    received_resumes_growth: float
    pending_resumes: int
    interview_invitations: int
    pending_interviews: int
    offers_extended: int
    pending_offers: int


class FunnelDataItem(BaseModel):
    name: str
    value: int
    percent: float


class JobStatsItem(BaseModel):
    id: int
    title: str
    status: str
    status_text: str
    urgent: bool
    views: int
    applications: int
    interviews: int
    location: Optional[str] = None
    salary: Optional[str] = None
    education: Optional[str] = None


class TodoItem(BaseModel):
    id: int
    text: str
    desc: str
    count: int


class RecentApplicationItem(BaseModel):
    id: int
    name: str
    student_no: str
    school: str
    major: str
    avatar: Optional[str]
    status: str
    status_text: str


class CompanyDashboardResponse(BaseModel):
    stats: DashboardStatsResponse
    funnel: list[FunnelDataItem]
    jobs: list[JobStatsItem]
    todos: list[TodoItem]
    recent_applications: list[RecentApplicationItem]


@router.get("/dashboard/", response_model=CompanyDashboardResponse)
def get_company_dashboard(
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company_user)
):
    company_id = current_company.id

    job_views = db.query(func.coalesce(func.sum(Job.view_count), 0)).filter(
        Job.company_id == company_id
    ).scalar() or 0

    received_resumes = db.query(func.count(Application.id)).join(
        Job, Application.job_id == Job.id
    ).filter(Job.company_id == company_id).scalar() or 0

    pending_resumes = db.query(func.count(Application.id)).join(
        Job, Application.job_id == Job.id
    ).filter(
        Job.company_id == company_id,
        Application.status == ApplicationStatus.PENDING
    ).scalar() or 0

    interview_invitations = db.query(func.count(Application.id)).join(
        Job, Application.job_id == Job.id
    ).filter(
        Job.company_id == company_id,
        Application.status.in_([ApplicationStatus.PASSED, ApplicationStatus.OFFERED])
    ).scalar() or 0

    pending_interviews = db.query(func.count(Application.id)).join(
        Job, Application.job_id == Job.id
    ).filter(
        Job.company_id == company_id,
        Application.status == ApplicationStatus.PASSED,
        Application.interview_time.isnot(None)
    ).scalar() or 0

    offers_extended = db.query(func.count(Application.id)).join(
        Job, Application.job_id == Job.id
    ).filter(
        Job.company_id == company_id,
        Application.status == ApplicationStatus.OFFERED
    ).scalar() or 0

    pending_offers = db.query(func.count(Application.id)).join(
        Job, Application.job_id == Job.id
    ).filter(
        Job.company_id == company_id,
        Application.status == ApplicationStatus.OFFERED,
        Application.offer_letter_url.is_(None)
    ).scalar() or 0

    growth = _application_growth(db, company_id)
    stats = DashboardStatsResponse(
        job_views=job_views,
        job_views_growth=growth,
        received_resumes=received_resumes,
        received_resumes_growth=growth,
        pending_resumes=pending_resumes,
        interview_invitations=interview_invitations,
        pending_interviews=pending_interviews,
        offers_extended=offers_extended,
        pending_offers=pending_offers
    )

    funnel = [
        {"name": "简历投递", "value": received_resumes, "percent": 100},
        {"name": "简历筛选", "value": received_resumes - pending_resumes, "percent": round((received_resumes - pending_resumes) / received_resumes * 100, 1) if received_resumes > 0 else 0},
        {"name": "笔试", "value": interview_invitations, "percent": round(interview_invitations / received_resumes * 100, 1) if received_resumes > 0 else 0},
        {"name": "面试", "value": pending_interviews, "percent": round(pending_interviews / received_resumes * 100, 1) if received_resumes > 0 else 0},
        {"name": "录用", "value": offers_extended, "percent": round(offers_extended / received_resumes * 100, 1) if received_resumes > 0 else 0}
    ]

    jobs = db.query(Job).filter(Job.company_id == company_id).limit(10).all()
    job_stats = []
    for job in jobs:
        applications_count = db.query(func.count(Application.id)).filter(
            Application.job_id == job.id
        ).scalar() or 0
        interviews_count = db.query(func.count(Application.id)).filter(
            Application.job_id == job.id,
            Application.status.in_([ApplicationStatus.PASSED, ApplicationStatus.OFFERED])
        ).scalar() or 0

        location = ''
        if job.province:
            location = job.province
        if job.city:
            location += ('/' + job.city)
        if job.district:
            location += ('/' + job.district)
        if job.address:
            location += (' ' + job.address)
        location = location.strip('/') or None

        salary = job.salary_show
        if not salary and (job.salary_min or job.salary_max):
            if job.salary_min and job.salary_max:
                salary = f"{job.salary_min/1000:.0f}k-{job.salary_max/1000:.0f}k"
            elif job.salary_min:
                salary = f"{job.salary_min/1000:.0f}k以上"
            elif job.salary_max:
                salary = f"{job.salary_max/1000:.0f}k以下"

        job_stats.append(JobStatsItem(
            id=job.id,
            title=job.title,
            status=job.status.value if hasattr(job.status, 'value') else job.status,
            status_text="招聘中" if job.status.value == "active" else "暂停",
            urgent=job.is_urgent,
            views=job.view_count,
            applications=applications_count,
            interviews=interviews_count,
            location=location,
            salary=salary,
            education=job.education
        ))

    pending_talks = db.query(CareerTalk).filter(
        CareerTalk.company_id == company_id,
        CareerTalk.status == ActivityStatus.PENDING,
    ).count()

    todos = [
        TodoItem(id=1, text="待筛选简历", desc=f"{pending_resumes} 份新简历需要处理", count=pending_resumes),
        TodoItem(id=2, text="待确认面试", desc=f"{pending_interviews} 场面试需要确认", count=pending_interviews),
        TodoItem(id=3, text="宣讲会待审核", desc=f"{pending_talks} 场宣讲会待审核", count=pending_talks),
        TodoItem(id=4, text="待签约", desc=f"{pending_offers} 个offer待学生签约", count=pending_offers),
    ]

    recent_apps = db.query(Application).join(Job, Application.job_id == Job.id).join(
        Student, Application.student_id == Student.id
    ).filter(
        Job.company_id == company_id
    ).order_by(Application.created_at.desc()).limit(5).all()

    recent_applications = []
    status_map = {
        ApplicationStatus.PENDING: ("待筛选", "pending"),
        ApplicationStatus.VIEWED: ("已查看", "viewed"),
        ApplicationStatus.PASSED: ("已通过", "passed"),
        ApplicationStatus.FAILED: ("未通过", "failed"),
        ApplicationStatus.OFFERED: ("待签约", "offered"),
        ApplicationStatus.REJECTED: ("已拒绝", "rejected"),
        ApplicationStatus.WITHDRAWN: ("已撤回", "withdrawn")
    }

    for app in recent_apps:
        student = app.student
        status_text, status_key = status_map.get(app.status, ("未知", "unknown"))
        recent_applications.append(RecentApplicationItem(
            id=app.id,
            name=student.name,
            student_no=student.student_no,
            school=student.college or "未知学院",
            major=student.major or "未知专业",
            avatar=student.avatar,
            status=status_key,
            status_text=status_text
        ))

    return CompanyDashboardResponse(
        stats=stats,
        funnel=funnel,
        jobs=job_stats,
        todos=todos,
        recent_applications=recent_applications
    )


class AnalyticsResponse(BaseModel):
    total_applications: int
    applications_growth: float
    pass_rate: float
    pass_rate_growth: float
    total_interviews: int
    interviews_growth: float
    total_offers: int
    offers_growth: float
    funnel: list
    funnel_max: int
    trend_labels: list
    applications_trend: list
    interviews_trend: list
    job_distribution: list
    school_labels: list
    school_data: list
    education_distribution: list
    job_rankings: list


@router.get("/analytics/", response_model=AnalyticsResponse)
def get_company_analytics(
    days: int = Query(30, ge=7, le=365),
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company_user),
):
    company_id = current_company.id
    start_date = datetime.now() - timedelta(days=days)
    growth = _application_growth(db, company_id, days)

    total_applications = db.query(func.count(Application.id)).join(
        Job, Application.job_id == Job.id
    ).filter(
        Job.company_id == company_id,
        Application.created_at >= start_date
    ).scalar() or 0

    total_passed = db.query(func.count(Application.id)).join(
        Job, Application.job_id == Job.id
    ).filter(
        Job.company_id == company_id,
        Application.status.in_([ApplicationStatus.PASSED, ApplicationStatus.OFFERED]),
        Application.created_at >= start_date
    ).scalar() or 0

    pass_rate = round(total_passed / total_applications * 100, 1) if total_applications > 0 else 0

    total_interviews = db.query(func.count(Application.id)).join(
        Job, Application.job_id == Job.id
    ).filter(
        Job.company_id == company_id,
        Application.status == ApplicationStatus.PASSED,
        Application.interview_time.isnot(None),
        Application.created_at >= start_date
    ).scalar() or 0

    total_offers = db.query(func.count(Application.id)).join(
        Job, Application.job_id == Job.id
    ).filter(
        Job.company_id == company_id,
        Application.status == ApplicationStatus.OFFERED,
        Application.created_at >= start_date
    ).scalar() or 0

    received_resumes = db.query(func.count(Application.id)).join(
        Job, Application.job_id == Job.id
    ).filter(Job.company_id == company_id).scalar() or 0

    pending_resumes = db.query(func.count(Application.id)).join(
        Job, Application.job_id == Job.id
    ).filter(
        Job.company_id == company_id,
        Application.status == ApplicationStatus.PENDING
    ).scalar() or 0

    funnel = [
        {"value": received_resumes, "name": "简历投递"},
        {"value": received_resumes - pending_resumes, "name": "简历筛选"},
        {"value": total_interviews, "name": "面试"},
        {"value": total_offers, "name": "发放Offer"}
    ]

    def apps_in_range(start, end):
        return _count_company_applications(db, company_id, start, end)

    def interviews_in_range(start, end):
        return _count_company_interviews(db, company_id, start, end)

    trend_labels, applications_trend = build_time_series(db, apps_in_range, days)
    _, interviews_trend = build_time_series(db, interviews_in_range, days)

    jobs = db.query(Job).filter(Job.company_id == company_id).all()
    job_distribution = []
    job_rankings = []

    for job in jobs[:5]:
        app_count = db.query(func.count(Application.id)).filter(
            Application.job_id == job.id
        ).scalar() or 0
        job_distribution.append({
            "value": app_count,
            "name": job.title[:6],
            "itemStyle": {"color": "#8b5cf6"}
        })
        job_rankings.append({
            "id": job.id,
            "title": job.title,
            "applications": app_count,
            "views": job.view_count,
            "conversion": round(app_count / job.view_count * 100, 1) if job.view_count > 0 else 0,
            "status": job.status.value if hasattr(job.status, 'value') else job.status
        })

    school_dist = db.query(
        Resume.education_school,
        func.count(Application.id).label('count')
    ).join(
        Application, Application.resume_id == Resume.id
    ).join(
        Job, Application.job_id == Job.id
    ).filter(
        Job.company_id == company_id,
        Resume.education_school.isnot(None)
    ).group_by(
        Resume.education_school
    ).order_by(
        func.count(Application.id).desc()
    ).limit(10).all()

    school_labels = [row.education_school or "未知" for row in school_dist]
    school_data = [row.count for row in school_dist]

    edu_dist = db.query(
        Resume.education_degree,
        func.count(Application.id).label('count')
    ).join(
        Application, Application.resume_id == Resume.id
    ).join(
        Job, Application.job_id == Job.id
    ).filter(
        Job.company_id == company_id,
        Resume.education_degree.isnot(None)
    ).group_by(
        Resume.education_degree
    ).all()

    edu_colors = {
        '专科': '#8b5cf6',
        '本科': '#3b82f6',
        '硕士': '#10b981',
        '博士': '#f59e0b',
        '其他': '#6b7280'
    }
    education_distribution = [
        {
            "value": row.count,
            "name": row.education_degree or "其他",
            "itemStyle": {"color": edu_colors.get(row.education_degree, "#6b7280")},
        }
        for row in edu_dist
    ]

    now = datetime.now()
    prev_start = now - timedelta(days=days * 2)
    mid = now - timedelta(days=days)
    prev_apps = _count_company_applications(db, company_id, prev_start, mid)
    prev_passed = db.query(func.count(Application.id)).join(
        Job, Application.job_id == Job.id
    ).filter(
        Job.company_id == company_id,
        Application.status.in_([ApplicationStatus.PASSED, ApplicationStatus.OFFERED]),
        Application.created_at >= prev_start,
        Application.created_at < mid,
    ).scalar() or 0
    prev_pass_rate = round(prev_passed / prev_apps * 100, 1) if prev_apps > 0 else 0
    pass_rate_growth = round(pass_rate - prev_pass_rate, 1)

    prev_interviews = _count_company_interviews(db, company_id, prev_start, mid)
    interviews_growth = calc_period_growth(total_interviews, prev_interviews)

    prev_offers = db.query(func.count(Application.id)).join(
        Job, Application.job_id == Job.id
    ).filter(
        Job.company_id == company_id,
        Application.status == ApplicationStatus.OFFERED,
        Application.created_at >= prev_start,
        Application.created_at < mid,
    ).scalar() or 0
    offers_growth = calc_period_growth(total_offers, prev_offers)

    return AnalyticsResponse(
        total_applications=total_applications,
        applications_growth=growth,
        pass_rate=pass_rate,
        pass_rate_growth=pass_rate_growth,
        total_interviews=total_interviews,
        interviews_growth=interviews_growth,
        total_offers=total_offers,
        offers_growth=offers_growth,
        funnel=funnel,
        funnel_max=received_resumes if received_resumes > 0 else 100,
        trend_labels=trend_labels,
        applications_trend=applications_trend,
        interviews_trend=interviews_trend,
        job_distribution=job_distribution,
        school_labels=school_labels,
        school_data=school_data,
        education_distribution=education_distribution,
        job_rankings=job_rankings
    )
