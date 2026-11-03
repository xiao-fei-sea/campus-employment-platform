from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, case, and_
from datetime import datetime, timedelta
from typing import Optional
import csv
import io

from app.core.database import get_db
from app.core.redis_client import get_cache, set_cache
from app.core.security import require_roles
from app.models.user import User, UserRole
from app.models.student import Student, EmploymentStatus
from app.models.company import Company, CompanyStatus
from app.models.job import Job, JobStatus
from app.models.application import Application, ApplicationStatus
from app.models.activity import CareerTalk, ActivityRegistration, ActivityStatus
from app.models.job import JobFavorite
from app.schemas.statistics import DashboardStats

router = APIRouter(tags=["管理端-数据统计"])

# 统计数据缓存时间（秒）
STATS_CACHE_TTL = 600  # 10 分钟


# ============================================
# ⚡ 聚合接口：一次返回所有 dashboard 所需数据
# 替代原来 dashboard 调 7 个独立接口的模式
# ============================================
@router.get("/all")
def get_all_dashboard_data(db: Session = Depends(get_db)):
    cache_key = "stats:all_dashboard"
    cached = get_cache(cache_key)
    if cached:
        return cached

    # 1. 核心统计
    total_students = db.query(func.count(Student.id)).scalar() or 0
    total_companies = db.query(func.count(Company.id)).filter(
        Company.status == CompanyStatus.APPROVED
    ).scalar() or 0
    total_jobs = db.query(func.count(Job.id)).filter(
        Job.status == JobStatus.APPROVED
    ).scalar() or 0
    total_applications = db.query(func.count(Application.id)).scalar() or 0

    # 2. 就业状态（一次 GROUP BY 拿到 8 个状态，原 8 次查询）
    status_rows = db.query(
        Student.employment_status,
        func.count(Student.id).label("cnt"),
    ).group_by(Student.employment_status).all()
    status_map = {(r[0].value if hasattr(r[0], "value") else str(r[0])): r.cnt for r in status_rows}

    signed_count = status_map.get(EmploymentStatus.SIGNED.value, 0)
    offered_count = status_map.get(EmploymentStatus.OFFERED.value, 0)
    employed_count = signed_count + offered_count
    searching_count = status_map.get(EmploymentStatus.SEARCHING.value, 0)
    further_study_count = status_map.get(EmploymentStatus.FURTHER_STUDY.value, 0)
    unemployed_count = status_map.get(EmploymentStatus.UNEMPLOYED.value, 0)
    startup_count = status_map.get(EmploymentStatus.STARTUP.value, 0)
    need_help_count = db.query(func.count(Student.id)).filter(
        Student.is_key_assistance == True
    ).scalar() or 0
    avg_offer = db.query(func.avg(Application.offer_salary)).filter(
        Application.status == ApplicationStatus.OFFERED,
        Application.offer_salary.isnot(None),
    ).scalar()

    employment_rate = round(employed_count / total_students * 100, 2) if total_students else 0
    avg_offer_salary = round(float(avg_offer), 0) if avg_offer else 0
    job_supply_demand_ratio = round(total_jobs / total_students, 2) if total_students else 0

    # 3. 待审核
    pending_company_count = db.query(func.count(Company.id)).filter(
        Company.status == CompanyStatus.PENDING
    ).scalar() or 0
    pending_job_count = db.query(func.count(Job.id)).filter(
        Job.status == JobStatus.PENDING
    ).scalar() or 0

    # 4. 转化漏斗（一次 GROUP BY 拿到所有状态数量）
    app_status_rows = db.query(
        Application.status,
        func.count(Application.id).label("cnt"),
    ).group_by(Application.status).all()
    app_status_map = {(r[0].value if hasattr(r[0], "value") else str(r[0])): r.cnt for r in app_status_rows}

    favorites = db.query(func.count(JobFavorite.id)).scalar() or 0
    viewed = sum(app_status_map.get(s.value, 0) for s in [
        ApplicationStatus.VIEWED, ApplicationStatus.PASSED,
        ApplicationStatus.OFFERED, ApplicationStatus.FAILED, ApplicationStatus.REJECTED,
    ])
    passed = app_status_map.get(ApplicationStatus.PASSED.value, 0) + app_status_map.get(ApplicationStatus.OFFERED.value, 0)
    offered_apps = app_status_map.get(ApplicationStatus.OFFERED.value, 0)
    funnel_steps = [
        {"name": "岗位收藏", "value": favorites},
        {"name": "简历投递", "value": total_applications},
        {"name": "简历查看", "value": viewed},
        {"name": "面试通过", "value": passed},
        {"name": "发放Offer", "value": offered_apps},
        {"name": "成功签约", "value": signed_count},
    ]
    max_val = max((s["value"] for s in funnel_steps), default=1) or 1
    for s in funnel_steps:
        s["percent"] = round(s["value"] / max_val * 100, 1) if max_val else 0

    # 5. 学院就业率
    dept_rows = db.query(
        func.coalesce(Student.college, "未知学院").label("college"),
        func.count(Student.id).label("total"),
        func.sum(case(
            (Student.employment_status.in_([EmploymentStatus.OFFERED, EmploymentStatus.SIGNED]), 1),
            else_=0,
        )).label("employed"),
    ).group_by("college").all()
    department_stats = [{
        "department": r.college,
        "total": int(r.total),
        "employed": int(r.employed or 0),
        "employment_rate": round((r.employed or 0) / r.total * 100, 1) if r.total else 0,
    } for r in dept_rows]

    # 6. 薪资分布（SQL 聚合）
    salary_ranges = [
        ("5K以下", 0, 5000),
        ("5-8K", 5000, 8000),
        ("8-10K", 8000, 10000),
        ("10-15K", 10000, 15000),
        ("15-20K", 15000, 20000),
        ("20-30K", 20000, 30000),
        ("30K以上", 30000, 999999),
    ]
    case_expr = case(
        *[(and_(Job.salary_min >= lo, Job.salary_min < hi), i) for i, (_, lo, hi) in enumerate(salary_ranges)],
        else_=-1,
    )
    salary_rows = db.query(case_expr.label("bucket"), func.count(Job.id).label("count")).filter(
        Job.status == JobStatus.APPROVED, Job.salary_min.isnot(None)
    ).group_by("bucket").all()
    count_map = {r.bucket: r.count for r in salary_rows if r.bucket >= 0}
    salary_distribution = [{"range": l, "count": count_map.get(i, 0)} for i, (l, _, _) in enumerate(salary_ranges)]

    # 7. 企业规模分布
    scale_rows = db.query(Company.scale, func.count(Company.id)).filter(
        Company.status == CompanyStatus.APPROVED
    ).group_by(Company.scale).all()
    company_scale_distribution = [{"name": _scale_label(s[0]), "value": s[1]} for s in scale_rows]

    # 8. 活动统计（一次 GROUP BY 拿到所有 status 的活动 + 一次 GROUP BY 拿到注册统计）
    talk_rows = db.query(
        CareerTalk.status,
        func.count(CareerTalk.id).label("cnt"),
    ).group_by(CareerTalk.status).all()
    talk_map = {(r[0].value if hasattr(r[0], "value") else str(r[0])): r.cnt for r in talk_rows}
    total_talks = talk_map.get(ActivityStatus.APPROVED.value, 0) + talk_map.get(ActivityStatus.ENDED.value, 0)
    pending_talks = talk_map.get(ActivityStatus.PENDING.value, 0)

    reg_rows = db.query(
        func.count(ActivityRegistration.id).label("total"),
        func.sum(case((ActivityRegistration.is_attended == True, 1), else_=0)).label("attended"),
    ).first()
    total_registrations = int(reg_rows.total or 0)
    attended = int(reg_rows.attended or 0)
    attendance_rate = round(attended / total_registrations * 100, 1) if total_registrations else 0
    activity_stats = {
        "total_talks": total_talks,
        "total_registrations": total_registrations,
        "attended_count": attended,
        "attendance_rate": attendance_rate,
        "pending_talks": pending_talks,
    }

    # 9. 地区分布（修复 N+1）
    region_rows = (
        db.query(
            Student.id.label("student_id"),
            Job.city.label("job_city"),
            Job.province.label("job_province"),
            Company.city.label("company_city"),
        )
        .join(Application, Application.student_id == Student.id)
        .join(Job, Job.id == Application.job_id)
        .outerjoin(Company, Company.id == Job.company_id)
        .filter(
            Student.employment_status.in_([EmploymentStatus.OFFERED, EmploymentStatus.SIGNED]),
            Application.status == ApplicationStatus.OFFERED,
        )
        .all()
    )
    seen = set()
    region_counts = {}
    for row in region_rows:
        if row.student_id in seen:
            continue
        seen.add(row.student_id)
        loc = row.job_city or row.company_city or row.job_province or "未知"
        region_counts[loc] = region_counts.get(loc, 0) + 1
    total_region = sum(region_counts.values())
    region_distribution = sorted(region_counts.items(), key=lambda x: x[1], reverse=True)[:15]
    region_distribution = [{
        "region": r, "count": c,
        "percentage": round(c / total_region * 100, 2) if total_region else 0,
    } for r, c in region_distribution]

    # 10. 就业趋势（30 天）
    employment_trend = _build_employment_trend(db, 30)

    # 11. 最近投递 + 热门岗位（用 JOIN 避免 N+1 懒加载）
    recent_apps_q = (
        db.query(
            Application.id,
            Application.status,
            Application.created_at,
            Student.name.label("student_name"),
            Job.title.label("job_title"),
        )
        .join(Student, Student.id == Application.student_id)
        .join(Job, Job.id == Application.job_id)
        .order_by(Application.created_at.desc())
        .limit(5)
        .all()
    )
    popular_jobs_q = (
        db.query(
            Job.id,
            Job.title,
            Job.application_count,
            Company.name.label("company_name"),
        )
        .join(Company, Company.id == Job.company_id)
        .filter(Job.status == JobStatus.APPROVED)
        .order_by(Job.application_count.desc())
        .limit(5)
        .all()
    )
    recent_applications = [{
        "id": a.id,
        "student_name": a.student_name,
        "job_title": a.job_title,
        "status": a.status.value if hasattr(a.status, "value") else a.status,
        "created_at": a.created_at.isoformat() if a.created_at else None,
    } for a in recent_apps_q]
    popular_jobs = [{
        "id": j.id,
        "title": j.title,
        "company_name": j.company_name,
        "application_count": j.application_count,
    } for j in popular_jobs_q]

    result = {
        # 基础统计
        "total_students": total_students,
        "total_companies": total_companies,
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        # 就业指标
        "employment_rate": employment_rate,
        "job_supply_demand_ratio": job_supply_demand_ratio,
        "employed_count": employed_count,
        "signed_count": signed_count,
        "offered_count": offered_count,
        "searching_count": searching_count,
        "further_study_count": further_study_count,
        "unemployed_count": unemployed_count,
        "startup_count": startup_count,
        "need_help_count": need_help_count,
        "avg_offer_salary": avg_offer_salary,
        # 待审核
        "pending_company_count": pending_company_count,
        "pending_job_count": pending_job_count,
        # 分布数据
        "department_stats": department_stats,
        "salary_distribution": salary_distribution,
        "company_scale_distribution": company_scale_distribution,
        "region_distribution": region_distribution,
        "funnel_steps": funnel_steps,
        "activity_stats": activity_stats,
        # 列表
        "recent_applications": recent_applications,
        "popular_jobs": popular_jobs,
        # 趋势
        "employment_trend": employment_trend,
    }

    set_cache(cache_key, result, expire=STATS_CACHE_TTL)
    return result

INDUSTRY_MAPPING = {
    "it": "互联网/IT",
    "finance": "金融",
    "manufacturing": "制造业",
    "education": "教育",
    "healthcare": "医疗健康",
    "real_estate": "房地产",
    "retail": "零售/贸易",
    "other": "其他",
}

SCALE_MAPPING = {
    "small": "小型企业",
    "medium": "中型企业",
    "large": "大型企业",
    "super_large": "超大型企业",
}


def _industry_label(val) -> str:
    key = val.value if hasattr(val, "value") else str(val).split(".")[-1].lower()
    return INDUSTRY_MAPPING.get(key, str(val))


def _scale_label(val) -> str:
    key = val.value if hasattr(val, "value") else str(val).split(".")[-1].lower()
    return SCALE_MAPPING.get(key, str(val))


def _build_employment_trend(db: Session, days: int = 30) -> list:
    """
    一次 GROUP BY 拿到 30 天投递/签约趋势
    原实现：30 天 × 2 = 60 次 SQL；现：2 次
    """
    start_date = (datetime.now() - timedelta(days=days - 1)).date()

    # 1) 按 created_at 分组的投递数
    app_rows = db.query(
        func.date(Application.created_at).label("d"),
        func.count(Application.id).label("cnt"),
    ).filter(
        func.date(Application.created_at) >= start_date
    ).group_by("d").all()
    app_map = {str(r.d): r.cnt for r in app_rows}

    # 2) 按 updated_at 分组的当日新增签约数（避免一次 count 漏掉没变化的）
    sign_rows = db.query(
        func.date(Student.updated_at).label("d"),
        func.count(Student.id).label("cnt"),
    ).filter(
        Student.employment_status == EmploymentStatus.SIGNED,
        func.date(Student.updated_at) >= start_date,
    ).group_by("d").all()
    sign_map = {str(r.d): r.cnt for r in sign_rows}

    trend = []
    for i in range(days - 1, -1, -1):
        date = (datetime.now() - timedelta(days=i)).date()
        d_str = date.strftime("%Y-%m-%d")
        trend.append({
            "date": d_str,
            "applications": app_map.get(d_str, 0),
            "signed": sign_map.get(d_str, 0),
        })
    return trend


@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    # ========== 1. 尝试从 Redis 读缓存 ==========
    cache_key = "stats:dashboard"
    cached = get_cache(cache_key)
    if cached:
        return DashboardStats(**cached)

    # ========== 2. 缓存未命中，执行 15+ 个聚合查询 ==========
    total_students = db.query(Student).count()
    total_companies = db.query(Company).filter(Company.status == CompanyStatus.APPROVED).count()
    total_jobs = db.query(Job).filter(Job.status == JobStatus.APPROVED).count()
    total_applications = db.query(Application).count()

    signed_count = db.query(Student).filter(
        Student.employment_status == EmploymentStatus.SIGNED
    ).count()
    offered_count = db.query(Student).filter(
        Student.employment_status == EmploymentStatus.OFFERED
    ).count()
    employed_count = signed_count + offered_count

    searching_count = db.query(Student).filter(
        Student.employment_status == EmploymentStatus.SEARCHING
    ).count()
    further_study_count = db.query(Student).filter(
        Student.employment_status == EmploymentStatus.FURTHER_STUDY
    ).count()
    unemployed_count = db.query(Student).filter(
        Student.employment_status == EmploymentStatus.UNEMPLOYED
    ).count()
    startup_count = db.query(Student).filter(
        Student.employment_status == EmploymentStatus.STARTUP
    ).count()
    need_help_count = db.query(Student).filter(Student.is_key_assistance == True).count()

    employment_rate = (employed_count / total_students * 100) if total_students > 0 else 0
    job_supply_demand_ratio = (total_jobs / total_students) if total_students > 0 else 0

    avg_offer = db.query(func.avg(Application.offer_salary)).filter(
        Application.status == ApplicationStatus.OFFERED,
        Application.offer_salary.isnot(None),
    ).scalar()
    avg_offer_salary = round(float(avg_offer), 0) if avg_offer else 0.0

    pending_company_count = db.query(Company).filter(
        Company.status == CompanyStatus.PENDING
    ).count()
    pending_job_count = db.query(Job).filter(Job.status == JobStatus.PENDING).count()

    recent_applications = db.query(Application).order_by(
        Application.created_at.desc()
    ).limit(5).all()

    popular_jobs = db.query(Job).filter(
        Job.status == JobStatus.APPROVED
    ).order_by(Job.application_count.desc()).limit(5).all()

    company_industry_stats = db.query(
        Company.industry,
        func.count(Company.id).label("count"),
    ).filter(Company.status == CompanyStatus.APPROVED).group_by(Company.industry).all()

    result = DashboardStats(
        total_students=total_students,
        total_companies=total_companies,
        total_jobs=total_jobs,
        total_applications=total_applications,
        employment_rate=round(employment_rate, 2),
        job_supply_demand_ratio=round(job_supply_demand_ratio, 2),
        employed_count=employed_count,
        signed_count=signed_count,
        offered_count=offered_count,
        searching_count=searching_count,
        further_study_count=further_study_count,
        unemployed_count=unemployed_count,
        startup_count=startup_count,
        need_help_count=need_help_count,
        avg_offer_salary=avg_offer_salary,
        pending_company_count=pending_company_count,
        pending_job_count=pending_job_count,
        recent_applications=[{
            "id": app.id,
            "student_name": app.student.name if app.student else None,
            "job_title": app.job.title if app.job else None,
            "status": app.status.value if hasattr(app.status, "value") else app.status,
            "created_at": app.created_at.isoformat() if app.created_at else None,
        } for app in recent_applications],
        popular_jobs=[{
            "id": job.id,
            "title": job.title,
            "company_name": job.company.name if job.company else None,
            "application_count": job.application_count,
        } for job in popular_jobs],
        company_industry_distribution=[{
            "industry": _industry_label(stat[0]),
            "count": stat[1],
        } for stat in company_industry_stats],
        employment_trend=_build_employment_trend(db, 30),
    )

    # ========== 3. 写入 Redis 缓存 ==========
    set_cache(cache_key, result.dict(), expire=STATS_CACHE_TTL)

    return result


@router.get("/employment-trend")
def get_employment_trend(
    days: int = Query(30, ge=7, le=365),
    db: Session = Depends(get_db),
):
    cache_key = f"stats:employment_trend:{days}"
    cached = get_cache(cache_key)
    if cached:
        return cached
    result = _build_employment_trend(db, days)
    set_cache(cache_key, result, expire=STATS_CACHE_TTL)
    return result


@router.get("/employment-status-distribution")
def get_employment_status_distribution(db: Session = Depends(get_db)):
    total = db.query(Student).count()
    status_mapping = {
        EmploymentStatus.SIGNED: "已签约",
        EmploymentStatus.SEARCHING: "求职中",
        EmploymentStatus.FURTHER_STUDY: "升学深造",
        EmploymentStatus.OFFERED: "已录取",
        EmploymentStatus.UNEMPLOYED: "未就业",
        EmploymentStatus.STARTUP: "创业",
    }
    result = []
    for status in EmploymentStatus:
        count = db.query(Student).filter(Student.employment_status == status).count()
        if count > 0:
            result.append({
                "name": status_mapping.get(status, status.value),
                "value": count,
                "percentage": round(count / total * 100, 2) if total > 0 else 0,
            })
    return result


@router.get("/region-distribution")
def get_region_distribution(db: Session = Depends(get_db)):
    cache_key = "stats:region_distribution"
    cached = get_cache(cache_key)
    if cached:
        return cached

    # ✅ 修复 N+1：用 1 个 JOIN 查询代替原来 1 + N 次查询
    # 原逻辑：先查所有就业学生，然后每个学生再查一次 Application（循环 N 次）
    # 优化后：1 个 JOIN 直接拿到 (学生 ID, 城市) 的关系
    rows = (
        db.query(
            Student.id.label("student_id"),
            Job.city.label("job_city"),
            Job.province.label("job_province"),
            Company.city.label("company_city"),
        )
        .join(Application, Application.student_id == Student.id)
        .join(Job, Job.id == Application.job_id)
        .outerjoin(Company, Company.id == Job.company_id)
        .filter(
            Student.employment_status.in_([EmploymentStatus.OFFERED, EmploymentStatus.SIGNED]),
            Application.status == ApplicationStatus.OFFERED,
        )
        .all()
    )

    # 去重：每个学生只算一次（可能有多条 offer 记录）
    seen_students = set()
    region_counts = {}
    for row in rows:
        if row.student_id in seen_students:
            continue
        seen_students.add(row.student_id)
        location = row.job_city or row.company_city or row.job_province or "未知"
        region_counts[location] = region_counts.get(location, 0) + 1

    if not region_counts:
        return []

    total = sum(region_counts.values())
    sorted_regions = sorted(region_counts.items(), key=lambda x: x[1], reverse=True)
    result = [{
        "region": region,
        "count": count,
        "percentage": round(count / total * 100, 2) if total > 0 else 0,
    } for region, count in sorted_regions[:15]]

    set_cache(cache_key, result, expire=STATS_CACHE_TTL)
    return result


@router.get("/department-stats")
def get_department_stats(db: Session = Depends(get_db)):
    cache_key = "stats:department"
    cached = get_cache(cache_key)
    if cached:
        return cached

    rows = db.query(
        func.coalesce(Student.college, "未知学院").label("college"),
        func.count(Student.id).label("total"),
        func.sum(
            case(
                (Student.employment_status.in_([EmploymentStatus.OFFERED, EmploymentStatus.SIGNED]), 1),
                else_=0,
            )
        ).label("employed"),
    ).group_by("college").all()

    result = [{
        "department": row.college,
        "total": int(row.total),
        "employed": int(row.employed or 0),
        "employment_rate": round((row.employed or 0) / row.total * 100, 1) if row.total else 0,
    } for row in rows]

    set_cache(cache_key, result, expire=STATS_CACHE_TTL)
    return result


@router.get("/major-stats")
def get_major_stats(
    college: Optional[str] = Query(None),
    graduation_year: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(
        func.coalesce(Student.college, "未知学院").label("college"),
        func.coalesce(Student.major, "未知专业").label("major"),
        func.count(Student.id).label("total"),
        func.sum(
            case(
                (Student.employment_status.in_([EmploymentStatus.OFFERED, EmploymentStatus.SIGNED]), 1),
                else_=0,
            )
        ).label("employed"),
    )
    if college:
        q = q.filter(Student.college == college)
    if graduation_year:
        q = q.filter(Student.graduation_year == graduation_year)
    rows = q.group_by("college", "major").all()

    return [{
        "college": row.college,
        "major": row.major,
        "department": row.college,
        "total": int(row.total),
        "employed": int(row.employed or 0),
        "employment_rate": round((row.employed or 0) / row.total * 100, 1) if row.total else 0,
    } for row in rows]


@router.get("/salary-distribution")
def get_salary_distribution(db: Session = Depends(get_db)):
    cache_key = "stats:salary"
    cached = get_cache(cache_key)
    if cached:
        return cached

    # ✅ 优化：原版把所有 job 加载到内存再 Python 循环
    # 改为：用 SQL CASE WHEN 一次性聚合
    ranges = [
        ("5K以下", 0, 5000),
        ("5-8K", 5000, 8000),
        ("8-10K", 8000, 10000),
        ("10-15K", 10000, 15000),
        ("15-20K", 15000, 20000),
        ("20-30K", 20000, 30000),
        ("30K以上", 30000, 999999),
    ]
    # 用 SQL 一次算完
    case_expr = case(
        *[(and_(Job.salary_min >= lo, Job.salary_min < hi), i) for i, (_, lo, hi) in enumerate(ranges)],
        else_=-1,
    )
    rows = (
        db.query(case_expr.label("bucket"), func.count(Job.id).label("count"))
        .filter(Job.status == JobStatus.APPROVED, Job.salary_min.isnot(None))
        .group_by("bucket")
        .all()
    )
    count_map = {row.bucket: row.count for row in rows if row.bucket >= 0}

    result = []
    for i, (label, _, _) in enumerate(ranges):
        result.append({
            "range": label,
            "count": count_map.get(i, 0),
        })

    set_cache(cache_key, result, expire=STATS_CACHE_TTL)
    return result


@router.get("/conversion-funnel")
def get_conversion_funnel(db: Session = Depends(get_db)):
    cache_key = "stats:conversion_funnel"
    cached = get_cache(cache_key)
    if cached:
        return cached

    favorites = db.query(func.count(JobFavorite.id)).scalar() or 0
    total_apps = db.query(func.count(Application.id)).scalar() or 0
    viewed = db.query(func.count(Application.id)).filter(
        Application.status.in_([
            ApplicationStatus.VIEWED,
            ApplicationStatus.PASSED,
            ApplicationStatus.OFFERED,
            ApplicationStatus.FAILED,
            ApplicationStatus.REJECTED,
        ])
    ).scalar() or 0
    passed = db.query(func.count(Application.id)).filter(
        Application.status.in_([ApplicationStatus.PASSED, ApplicationStatus.OFFERED])
    ).scalar() or 0
    offered = db.query(func.count(Application.id)).filter(
        Application.status == ApplicationStatus.OFFERED
    ).scalar() or 0
    signed_students = db.query(Student).filter(
        Student.employment_status == EmploymentStatus.SIGNED
    ).count()

    steps = [
        {"name": "岗位收藏", "value": favorites},
        {"name": "简历投递", "value": total_apps},
        {"name": "简历查看", "value": viewed},
        {"name": "面试通过", "value": passed},
        {"name": "发放Offer", "value": offered},
        {"name": "成功签约", "value": signed_students},
    ]
    max_val = max((s["value"] for s in steps), default=1) or 1
    for s in steps:
        s["percent"] = round(s["value"] / max_val * 100, 1) if max_val else 0

    set_cache(cache_key, steps, expire=STATS_CACHE_TTL)
    return steps


@router.get("/company-scale-distribution")
def get_company_scale_distribution(db: Session = Depends(get_db)):
    cache_key = "stats:company_scale"
    cached = get_cache(cache_key)
    if cached:
        return cached

    rows = db.query(
        Company.scale,
        func.count(Company.id).label("count"),
    ).filter(Company.status == CompanyStatus.APPROVED).group_by(Company.scale).all()

    result = [{
        "name": _scale_label(stat[0]),
        "value": stat[1],
    } for stat in rows]

    set_cache(cache_key, result, expire=STATS_CACHE_TTL)
    return result


@router.get("/activity-stats")
def get_activity_stats(db: Session = Depends(get_db)):
    cache_key = "stats:activity"
    cached = get_cache(cache_key)
    if cached:
        return cached

    total_talks = db.query(CareerTalk).filter(
        CareerTalk.status.in_([ActivityStatus.APPROVED, ActivityStatus.ENDED])
    ).count()
    total_registrations = db.query(ActivityRegistration).count()
    attended = db.query(ActivityRegistration).filter(
        ActivityRegistration.is_attended == True
    ).count()
    attendance_rate = round(attended / total_registrations * 100, 1) if total_registrations else 0

    result = {
        "total_talks": total_talks,
        "total_registrations": total_registrations,
        "attended_count": attended,
        "attendance_rate": attendance_rate,
        "pending_talks": db.query(CareerTalk).filter(
            CareerTalk.status == ActivityStatus.PENDING
        ).count(),
    }

    set_cache(cache_key, result, expire=STATS_CACHE_TTL)
    return result


@router.get("/export")
def export_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.COUNSELOR))
):
    students = db.query(Student).order_by(Student.id).all()

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["学号", "姓名", "学院", "专业", "班级", "毕业年份", "就业状态", "重点帮扶"])
    for s in students:
        status = s.employment_status.value if hasattr(s.employment_status, "value") else s.employment_status
        writer.writerow([
            s.student_no or "",
            s.name or "",
            s.college or "",
            s.major or "",
            s.class_name or "",
            s.graduation_year or "",
            status or "",
            "是" if s.is_key_assistance else "否",
        ])

    content = buffer.getvalue()
    buffer.close()
    filename = f"students_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return StreamingResponse(
        iter([content]),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )
