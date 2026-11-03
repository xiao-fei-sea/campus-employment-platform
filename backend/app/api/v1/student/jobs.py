from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
import hashlib
import json

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.redis_client import get_cache, set_cache
from app.models.user import User, UserRole
from app.models.student import Student
from app.models.job import Job, JobFavorite, JobStatus
from app.models.company import Company
from app.models.application import Application, ApplicationStatus
from app.schemas.job import JobListResponse, JobListWithTotalResponse

router = APIRouter(tags=["学生-岗位搜索"])

# 岗位列表缓存过期时间（秒）
JOB_LIST_CACHE_TTL = 300  # 5 分钟


def get_current_student(current_user: User = Depends(get_current_user)) -> Student:
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(
            status_code=403,
            detail="仅学生可以访问此功能"
        )
    student = current_user.student_profile
    if not student:
        raise HTTPException(
            status_code=404,
            detail="学生信息不存在"
        )
    return student


@router.get("/", response_model=JobListWithTotalResponse)
def search_jobs(
    keyword: Optional[str] = None,
    job_type: Optional[str] = None,
    province: Optional[str] = None,
    city: Optional[str] = None,
    salary_min: Optional[int] = None,
    salary_max: Optional[int] = None,
    industry: Optional[str] = None,
    sort: Optional[str] = Query("comprehensive", description="排序方式: comprehensive, latest, salary, views"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    # ========== 1. 组装缓存 key（基于筛选参数，与用户无关） ==========
    cache_params = {
        "keyword": keyword or "",
        "job_type": job_type or "",
        "province": province or "",
        "city": city or "",
        "salary_min": salary_min or 0,
        "salary_max": salary_max or 0,
        "industry": industry or "",
        "sort": sort,
        "page": page,
        "page_size": page_size,
    }
    cache_key = "job:list:" + hashlib.md5(
        json.dumps(cache_params, sort_keys=True).encode()
    ).hexdigest()

    # ========== 2. 尝试从 Redis 读缓存 ==========
    cached = get_cache(cache_key)
    if cached:
        # 缓存命中：直接拿到筛选+分页后的岗位列表，跳过数据库查询
        total = cached["total"]
        jobs_data = cached["jobs"]
    else:
        # 缓存未命中：查数据库
        query = db.query(Job).join(Company).filter(
            Job.status == JobStatus.APPROVED,
            Company.status == "approved"
        )

        if keyword:
            query = query.filter(
                or_(
                    Job.title.contains(keyword),
                    Company.name.contains(keyword),
                    Job.description.contains(keyword)
                )
            )

        if job_type:
            query = query.filter(Job.job_type == job_type)

        if province:
            query = query.filter(Job.province == province)

        if city:
            cities = [c.strip() for c in city.split(',')]
            city_filters = [Job.city.contains(c) for c in cities]
            query = query.filter(or_(*city_filters))

        if salary_min:
            query = query.filter(Job.salary_max >= salary_min)

        if salary_max:
            query = query.filter(Job.salary_min <= salary_max)

        if industry:
            industries = [i.strip() for i in industry.split(',')]
            industry_filters = [Company.industry == i for i in industries]
            query = query.filter(or_(*industry_filters))

        if sort == "latest":
            query = query.order_by(Job.created_at.desc())
        elif sort == "salary":
            query = query.order_by(Job.salary_max.desc())
        elif sort == "views":
            query = query.order_by(Job.view_count.desc())
        else:
            query = query.order_by(Job.is_top.desc(), Job.created_at.desc())

        total = query.count()
        jobs = query.offset((page - 1) * page_size).limit(page_size).all()

        # 把 ORM 对象转成可序列化的 dict（用于缓存）
        jobs_data = []
        for job in jobs:
            jobs_data.append({
                "id": job.id,
                "company_id": job.company_id,
                "title": job.title,
                "job_type": job.job_type,
                "status": job.status.value if hasattr(job.status, "value") else str(job.status),
                "salary_min": job.salary_min,
                "salary_max": job.salary_max,
                "salary_show": job.salary_show,
                "province": job.province,
                "city": job.city,
                "district": job.district,
                "address": job.address,
                "description": job.description,
                "requirement": job.requirement,
                "benefit": job.benefit,
                "headcount": job.headcount,
                "application_count": job.application_count,
                "view_count": job.view_count,
                "is_top": job.is_top,
                "is_highlight": job.is_highlight,
                "is_urgent": job.is_urgent,
                "is_campus_recruit": job.is_campus_recruit,
                "rejection_reason": job.rejection_reason,
                "approved_at": job.approved_at.isoformat() if job.approved_at else None,
                "created_at": job.created_at.isoformat() if job.created_at else None,
                "updated_at": job.updated_at.isoformat() if job.updated_at else None,
                "company_name": job.company.name,
                "company_logo": job.company.logo,
            })

        # ========== 3. 写入 Redis 缓存 ==========
        set_cache(cache_key, {"total": total, "jobs": jobs_data}, expire=JOB_LIST_CACHE_TTL)

    # ========== 4. 用户相关字段（不缓存，每次实时查 - 这两个查询很快） ==========
    favorite_job_ids = set(
        f.job_id for f in db.query(JobFavorite).filter(
            JobFavorite.student_id == current_student.id
        ).all()
    )

    applied_job_ids = set(
        a.job_id for a in db.query(Application).filter(
            Application.student_id == current_student.id,
            Application.status != ApplicationStatus.WITHDRAWN
        ).all()
    )

    # ========== 5. 合并用户相关字段 ==========
    result = []
    for job_dict in jobs_data:
        job_dict_copy = dict(job_dict)  # 避免修改缓存里的对象
        job_dict_copy["is_favorited"] = job_dict_copy["id"] in favorite_job_ids
        job_dict_copy["has_applied"] = job_dict_copy["id"] in applied_job_ids
        result.append(job_dict_copy)

    return JobListWithTotalResponse(
        total=total,
        page=page,
        page_size=page_size,
        data=result
    )


@router.get("/favorites")
def get_favorite_jobs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    query = db.query(JobFavorite).filter(
        JobFavorite.student_id == current_student.id
    ).join(Job).join(Company).filter(
        Job.status == JobStatus.APPROVED,
        Company.status == "approved"
    )

    total = query.count()
    favorites = query.order_by(JobFavorite.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    applied_job_ids = set(
        a.job_id for a in db.query(Application).filter(
            Application.student_id == current_student.id,
            Application.status != ApplicationStatus.WITHDRAWN
        ).all()
    )

    result = []
    for fav in favorites:
        job = fav.job
        job_dict = {
            "id": job.id,
            "company_id": job.company_id,
            "title": job.title,
            "job_type": job.job_type,
            "status": job.status,
            "salary_min": job.salary_min,
            "salary_max": job.salary_max,
            "salary_show": job.salary_show,
            "province": job.province,
            "city": job.city,
            "district": job.district,
            "address": job.address,
            "description": job.description,
            "requirement": job.requirement,
            "benefit": job.benefit,
            "headcount": job.headcount,
            "application_count": job.application_count,
            "view_count": job.view_count,
            "is_top": job.is_top,
            "is_highlight": job.is_highlight,
            "is_urgent": job.is_urgent,
            "is_campus_recruit": job.is_campus_recruit,
            "is_favorited": True,
            "has_applied": job.id in applied_job_ids,
            "rejection_reason": job.rejection_reason,
            "approved_at": job.approved_at,
            "created_at": job.created_at,
            "updated_at": job.updated_at,
            "company_name": job.company.name,
            "company_logo": job.company.logo,
            "favorited_at": fav.created_at
        }
        result.append(job_dict)

    return {
        "data": result,
        "total": total
    }


@router.post("/{job_id}/collect")
def collect_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="岗位不存在")

    existing = db.query(JobFavorite).filter(
        JobFavorite.student_id == current_student.id,
        JobFavorite.job_id == job_id
    ).first()

    if existing:
        return {"message": "已收藏过该岗位"}

    favorite = JobFavorite(student_id=current_student.id, job_id=job_id)
    db.add(favorite)
    db.commit()

    return {"message": "收藏成功"}


@router.delete("/{job_id}/collect")
def cancel_collect_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    favorite = db.query(JobFavorite).filter(
        JobFavorite.student_id == current_student.id,
        JobFavorite.job_id == job_id
    ).first()

    if not favorite:
        raise HTTPException(status_code=404, detail="未收藏该岗位")

    db.delete(favorite)
    db.commit()

    return {"message": "取消收藏成功"}


@router.get("/{job_id}", response_model=JobListResponse)
def get_job_detail(
    job_id: int,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    job = db.query(Job).join(Company).filter(
        Job.id == job_id,
        Job.status == JobStatus.APPROVED
    ).first()

    if not job:
        raise HTTPException(status_code=404, detail="岗位不存在或未通过审核")

    job.view_count += 1
    db.commit()

    is_favorited = db.query(JobFavorite).filter(
        JobFavorite.student_id == current_student.id,
        JobFavorite.job_id == job_id
    ).first() is not None

    has_applied = db.query(Application).filter(
        Application.student_id == current_student.id,
        Application.job_id == job_id,
        Application.status != ApplicationStatus.WITHDRAWN
    ).first() is not None

    return {
        "id": job.id,
        "company_id": job.company_id,
        "title": job.title,
        "job_type": job.job_type,
        "status": job.status,
        "salary_min": job.salary_min,
        "salary_max": job.salary_max,
        "salary_show": job.salary_show,
        "province": job.province,
        "city": job.city,
        "district": job.district,
        "address": job.address,
        "description": job.description,
        "requirement": job.requirement,
        "benefit": job.benefit,
        "skills": job.skills,
        "headcount": job.headcount,
        "application_count": job.application_count,
        "view_count": job.view_count,
        "is_top": job.is_top,
        "is_highlight": job.is_highlight,
        "is_urgent": job.is_urgent,
        "is_campus_recruit": job.is_campus_recruit,
        "is_favorited": is_favorited,
        "has_applied": has_applied,
        "rejection_reason": job.rejection_reason,
        "approved_at": job.approved_at,
        "created_at": job.created_at,
        "updated_at": job.updated_at,
        "company_name": job.company.name,
        "company_logo": job.company.logo,
        "company_short_name": job.company.short_name,
        "company_scale": job.company.scale,
        "company_industry": job.company.industry,
        "company_description": job.company.description,
        "company_website": job.company.website,
        "company_province": job.company.province,
        "company_city": job.company.city,
        "company_district": job.company.district,
        "company_address": job.company.address,
        "similar_jobs": [
            {
                "id": j.id,
                "title": j.title,
                "company_name": j.company.name,
                "salary": j.salary_show or (f"{j.salary_min/1000}-{j.salary_max/1000}K" if j.salary_min and j.salary_max else "薪资面议")
            }
            for j in db.query(Job).join(Company).filter(
                Job.id != job_id
            ).limit(3).all()
        ]
    }


@router.post("/{job_id}/apply")
def apply_for_job(
    job_id: int,
    resume_id: Optional[int] = Body(default=None),
    cover_letter: Optional[str] = Body(default=None),
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    from app.models.resume import Resume

    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="岗位不存在")

    if job.status != JobStatus.APPROVED:
        raise HTTPException(status_code=400, detail="岗位暂不可投递")

    existing = db.query(Application).filter(
        Application.student_id == current_student.id,
        Application.job_id == job_id
    ).first()
    if existing:
        if existing.status not in [ApplicationStatus.REJECTED, ApplicationStatus.WITHDRAWN]:
            raise HTTPException(status_code=400, detail="您已投递过此岗位")
        existing.status = ApplicationStatus.PENDING
        existing.cover_letter = cover_letter
        existing.updated_at = func.now()
        db.commit()
        return {"message": "投递成功", "application_id": existing.id}

    if resume_id:
        resume = db.query(Resume).filter(
            Resume.id == resume_id,
            Resume.student_id == current_student.id
        ).first()
        if not resume:
            raise HTTPException(status_code=404, detail="简历不存在")
    else:
        resume = db.query(Resume).filter(
            Resume.student_id == current_student.id,
            Resume.is_default == True
        ).first()
        if not resume:
            resume = db.query(Resume).filter(
                Resume.student_id == current_student.id
            ).order_by(Resume.updated_at.desc()).first()
        if not resume:
            raise HTTPException(status_code=404, detail="请先创建简历")

    application = Application(
        job_id=job_id,
        student_id=current_student.id,
        resume_id=resume.id,
        cover_letter=cover_letter
    )
    db.add(application)

    job.application_count += 1
    db.commit()
    db.refresh(application)

    return {"message": "投递成功", "application_id": application.id}
