from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.student.resume import router as student_resume_router
from app.api.v1.student.jobs import router as student_jobs_router
from app.api.v1.student.applications import router as student_applications_router
from app.api.v1.student.career_talks import router as student_career_talks_router
from app.api.v1.student.profile import router as student_profile_router
from app.api.v1.student.dashboard import router as student_dashboard_router
from app.api.v1.company.jobs import router as company_jobs_router
from app.api.v1.company.resumes import router as company_resumes_router
from app.api.v1.company.career_talks import router as company_career_talks_router
from app.api.v1.company.profile import router as company_profile_router
from app.api.v1.company.analytics import router as company_analytics_router
from app.api.v1.admin.statistics import router as admin_statistics_router
from app.api.v1.admin.students import router as admin_students_router
from app.api.v1.admin.companies import router as admin_companies_router
from app.api.v1.admin.jobs import router as admin_jobs_router
from app.api.v1.admin.activities import router as admin_activities_router
from app.api.v1.admin.system import router as admin_system_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["认证"])
api_router.include_router(student_resume_router, prefix="/student/resumes", tags=["学生-简历"])
api_router.include_router(student_jobs_router, prefix="/student/jobs", tags=["学生-岗位"])
api_router.include_router(student_applications_router, prefix="/student/applications", tags=["学生-投递"])
api_router.include_router(student_career_talks_router, prefix="/student/career-talks", tags=["学生-宣讲会"])
api_router.include_router(student_profile_router, prefix="/student/profile", tags=["学生-个人信息"])
api_router.include_router(student_dashboard_router, prefix="/student/dashboard", tags=["学生-仪表盘"])
api_router.include_router(company_jobs_router, prefix="/company/jobs", tags=["企业-岗位"])
api_router.include_router(company_resumes_router, prefix="/company/resumes", tags=["企业-简历"])
api_router.include_router(company_career_talks_router, prefix="/company/career-talks", tags=["企业-宣讲会"])
api_router.include_router(company_profile_router, prefix="/company/profile", tags=["企业-信息"])
api_router.include_router(company_analytics_router, prefix="/company", tags=["企业-数据统计"])
api_router.include_router(admin_statistics_router, prefix="/admin/statistics", tags=["管理端-统计"])
api_router.include_router(admin_students_router, prefix="/admin/students", tags=["管理端-学生"])
api_router.include_router(admin_companies_router, prefix="/admin/companies", tags=["管理端-企业"])
api_router.include_router(admin_jobs_router, prefix="/admin/jobs", tags=["管理端-岗位"])
api_router.include_router(admin_activities_router, prefix="/admin/activities", tags=["管理端-活动"])
api_router.include_router(admin_system_router, prefix="/admin/system", tags=["管理端-系统"])
