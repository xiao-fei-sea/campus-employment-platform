-- ============================================
-- 数据库索引优化脚本
-- ============================================
-- 目的：为常用查询字段添加索引，加速所有统计查询
-- 注意：idempotent（IF NOT EXISTS），可重复执行
-- MySQL 5.7+ / 8.0+
-- ============================================

-- ---------- applications 表 ----------
CREATE INDEX idx_app_student_id ON applications(student_id);
CREATE INDEX idx_app_job_id ON applications(job_id);
CREATE INDEX idx_app_status ON applications(status);
CREATE INDEX idx_app_student_status ON applications(student_id, status);
CREATE INDEX idx_app_job_status ON applications(job_id, status);
CREATE INDEX idx_app_created_at ON applications(created_at);

-- ---------- students 表 ----------
CREATE INDEX idx_stu_college ON students(college);
CREATE INDEX idx_stu_major ON students(major);
CREATE INDEX idx_stu_graduation_year ON students(graduation_year);
CREATE INDEX idx_stu_employment_status ON students(employment_status);
CREATE INDEX idx_stu_college_status ON students(college, employment_status);

-- ---------- jobs 表 ----------
CREATE INDEX idx_job_company_id ON jobs(company_id);
CREATE INDEX idx_job_status ON jobs(status);
CREATE INDEX idx_job_status_created ON jobs(status, created_at);
CREATE INDEX idx_job_salary_min ON jobs(salary_min);
CREATE INDEX idx_job_status_salary ON jobs(status, salary_min);

-- ---------- companies 表 ----------
CREATE INDEX idx_comp_status ON companies(status);
CREATE INDEX idx_comp_scale ON companies(scale);
CREATE INDEX idx_comp_industry ON companies(industry);

-- ---------- job_favorites 表 ----------
CREATE INDEX idx_fav_student_id ON job_favorites(student_id);
CREATE INDEX idx_fav_job_id ON job_favorites(job_id);
CREATE INDEX idx_fav_student_created ON job_favorites(student_id, created_at);

-- ---------- career_talks 表 ----------
CREATE INDEX idx_talk_status ON career_talks(status);
CREATE INDEX idx_talk_company_id ON career_talks(company_id);
CREATE INDEX idx_talk_start_time ON career_talks(start_time);

-- ---------- activity_registrations 表 ----------
CREATE INDEX idx_reg_student_id ON activity_registrations(student_id);
CREATE INDEX idx_reg_career_talk_id ON activity_registrations(career_talk_id);
CREATE INDEX idx_reg_is_attended ON activity_registrations(is_attended);

-- ---------- users 表（已存在 username/email 唯一索引，补一个 role） ----------
CREATE INDEX idx_user_role ON users(role);

-- ============================================
-- 验证索引已创建
-- ============================================
SELECT TABLE_NAME, INDEX_NAME, COLUMN_NAME, SEQ_IN_INDEX
FROM INFORMATION_SCHEMA.STATISTICS
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME IN ('applications', 'students', 'jobs', 'companies', 'job_favorites', 'career_talks', 'activity_registrations', 'users')
  AND INDEX_NAME LIKE 'idx_%'
ORDER BY TABLE_NAME, INDEX_NAME;
