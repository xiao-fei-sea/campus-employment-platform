-- 高校就业服务平台 数据库建表语句
-- 数据库：MySQL 8.0+
-- 字符集：utf8mb4
-- 排序规则：utf8mb4_unicode_ci

-- 创建数据库
CREATE DATABASE IF NOT EXISTS campus_employment
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE campus_employment;

-- ============================================
-- 1. 用户表（users）
-- ============================================
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    `username` VARCHAR(50) NOT NULL COMMENT '用户名',
    `email` VARCHAR(100) NOT NULL COMMENT '邮箱',
    `hashed_password` VARCHAR(255) NOT NULL COMMENT '加密密码',
    `role` VARCHAR(20) NOT NULL DEFAULT 'student' COMMENT '角色',
    `is_active` BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    `is_verified` BOOLEAN DEFAULT FALSE COMMENT '是否已验证',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE INDEX `idx_username` (`username`),
    UNIQUE INDEX `idx_email` (`email`),
    INDEX `idx_role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- ============================================
-- 2. 学生表（students）
-- ============================================
CREATE TABLE IF NOT EXISTS `students` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '学生ID',
    `user_id` INT NOT NULL COMMENT '用户ID',
    `student_no` VARCHAR(20) NOT NULL COMMENT '学号',
    `name` VARCHAR(50) NOT NULL COMMENT '姓名',
    `gender` VARCHAR(10) COMMENT '性别',
    `phone` VARCHAR(20) COMMENT '联系电话',
    `avatar` VARCHAR(500) COMMENT '头像URL',
    `major` VARCHAR(100) COMMENT '专业',
    `college` VARCHAR(100) COMMENT '学院',
    `class_name` VARCHAR(50) COMMENT '班级',
    `graduation_year` INT COMMENT '毕业年份',
    `employment_status` VARCHAR(20) DEFAULT 'searching' COMMENT '就业状态',
    `is_key_assistance` BOOLEAN DEFAULT FALSE COMMENT '是否重点帮扶',
    `assistance_note` TEXT COMMENT '帮扶备注',
    `resume_url` VARCHAR(500) COMMENT '简历URL',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE INDEX `idx_user_id` (`user_id`),
    UNIQUE INDEX `idx_student_no` (`student_no`),
    INDEX `idx_employment_status` (`employment_status`),
    CONSTRAINT `fk_students_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学生表';

-- ============================================
-- 3. 企业表（companies）
-- ============================================
CREATE TABLE IF NOT EXISTS `companies` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '企业ID',
    `user_id` INT NOT NULL COMMENT '用户ID',
    `name` VARCHAR(200) NOT NULL COMMENT '企业名称',
    `short_name` VARCHAR(50) COMMENT '企业简称',
    `logo` VARCHAR(500) COMMENT '企业Logo',
    `scale` VARCHAR(20) DEFAULT 'medium' COMMENT '企业规模',
    `industry` VARCHAR(20) DEFAULT 'other' COMMENT '所属行业',
    `status` VARCHAR(20) DEFAULT 'pending' COMMENT '审核状态',
    `license_no` VARCHAR(50) COMMENT '营业执照号',
    `license_url` VARCHAR(500) COMMENT '营业执照URL',
    `contact_name` VARCHAR(50) COMMENT '联系人姓名',
    `contact_phone` VARCHAR(20) COMMENT '联系人电话',
    `contact_email` VARCHAR(100) COMMENT '联系人邮箱',
    `province` VARCHAR(50) COMMENT '所在省份',
    `city` VARCHAR(50) COMMENT '所在城市',
    `district` VARCHAR(50) COMMENT '所在区县',
    `address` VARCHAR(500) COMMENT '详细地址',
    `description` TEXT COMMENT '企业简介',
    `website` VARCHAR(200) COMMENT '企业官网',
    `verified_at` DATETIME COMMENT '认证时间',
    `verified_by` INT COMMENT '认证管理员ID',
    `rejection_reason` TEXT COMMENT '驳回原因',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE INDEX `idx_user_id` (`user_id`),
    INDEX `idx_status` (`status`),
    INDEX `idx_industry` (`industry`),
    CONSTRAINT `fk_companies_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_companies_verified_by` FOREIGN KEY (`verified_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='企业表';

-- ============================================
-- 4. 岗位表（jobs）
-- ============================================
CREATE TABLE IF NOT EXISTS `jobs` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '岗位ID',
    `company_id` INT NOT NULL COMMENT '企业ID',
    `title` VARCHAR(200) NOT NULL COMMENT '岗位名称',
    `job_type` VARCHAR(20) DEFAULT 'full_time' COMMENT '岗位类型',
    `status` VARCHAR(20) DEFAULT 'pending' COMMENT '审核状态',
    `salary_min` INT COMMENT '最低薪资',
    `salary_max` INT COMMENT '最高薪资',
    `salary_show` VARCHAR(50) COMMENT '薪资显示',
    `province` VARCHAR(50) COMMENT '工作省份',
    `city` VARCHAR(50) COMMENT '工作城市',
    `district` VARCHAR(50) COMMENT '工作区县',
    `address` VARCHAR(500) COMMENT '详细地址',
    `description` TEXT COMMENT '岗位描述',
    `requirement` TEXT COMMENT '任职要求',
    `benefit` TEXT COMMENT '福利待遇',
    `skills` TEXT COMMENT '技能要求',
    `headcount` INT DEFAULT 1 COMMENT '招聘人数',
    `experience` VARCHAR(100) COMMENT '经验要求',
    `education` VARCHAR(50) COMMENT '学历要求',
    `application_count` INT DEFAULT 0 COMMENT '投递数量',
    `view_count` INT DEFAULT 0 COMMENT '浏览次数',
    `is_top` BOOLEAN DEFAULT FALSE COMMENT '是否置顶',
    `is_highlight` BOOLEAN DEFAULT FALSE COMMENT '是否精选',
    `is_urgent` BOOLEAN DEFAULT FALSE COMMENT '是否紧急',
    `is_campus_recruit` BOOLEAN DEFAULT FALSE COMMENT '是否校招',
    `rejection_reason` TEXT COMMENT '驳回原因',
    `approved_at` DATETIME COMMENT '审核时间',
    `approved_by` INT COMMENT '审核管理员ID',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `expired_at` DATETIME COMMENT '过期时间',
    INDEX `idx_company_id` (`company_id`),
    INDEX `idx_status` (`status`),
    INDEX `idx_job_type` (`job_type`),
    INDEX `idx_is_campus_recruit` (`is_campus_recruit`),
    INDEX `idx_created_at` (`created_at`),
    CONSTRAINT `fk_jobs_company_id` FOREIGN KEY (`company_id`) REFERENCES `companies` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_jobs_approved_by` FOREIGN KEY (`approved_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='岗位表';

-- ============================================
-- 5. 岗位收藏表（job_favorites）
-- ============================================
CREATE TABLE IF NOT EXISTS `job_favorites` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '收藏ID',
    `student_id` INT NOT NULL COMMENT '学生ID',
    `job_id` INT NOT NULL COMMENT '岗位ID',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '收藏时间',
    UNIQUE INDEX `idx_student_job` (`student_id`, `job_id`),
    INDEX `idx_student_id` (`student_id`),
    INDEX `idx_job_id` (`job_id`),
    CONSTRAINT `fk_job_favorites_student_id` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_job_favorites_job_id` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='岗位收藏表';

-- ============================================
-- 6. 简历表（resumes）
-- ============================================
CREATE TABLE IF NOT EXISTS `resumes` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '简历ID',
    `student_id` INT NOT NULL COMMENT '学生ID',
    `title` VARCHAR(100) NOT NULL COMMENT '简历标题',
    `is_default` BOOLEAN DEFAULT FALSE COMMENT '是否默认简历',
    `visibility` VARCHAR(20) DEFAULT 'public' COMMENT '可见性',
    `template` VARCHAR(50) DEFAULT 'default' COMMENT '简历模板',
    `personal_name` VARCHAR(50) COMMENT '姓名',
    `personal_gender` VARCHAR(10) COMMENT '性别',
    `personal_phone` VARCHAR(20) COMMENT '电话',
    `personal_email` VARCHAR(100) COMMENT '邮箱',
    `personal_age` INT COMMENT '年龄',
    `personal_city` VARCHAR(50) COMMENT '所在城市',
    `education_school` VARCHAR(100) COMMENT '学校',
    `education_major` VARCHAR(100) COMMENT '专业',
    `education_degree` VARCHAR(20) COMMENT '学历',
    `education_start` VARCHAR(20) COMMENT '入学时间',
    `education_end` VARCHAR(20) COMMENT '毕业时间',
    `experience_company` VARCHAR(100) COMMENT '公司名称',
    `experience_position` VARCHAR(100) COMMENT '职位名称',
    `experience_duration` VARCHAR(50) COMMENT '工作时长',
    `experience_description` TEXT COMMENT '工作描述',
    `skill_names` TEXT COMMENT '技能名称',
    `skill_levels` TEXT COMMENT '技能水平',
    `certificate_names` TEXT COMMENT '证书名称',
    `project_name` VARCHAR(100) COMMENT '项目名称',
    `project_role` VARCHAR(50) COMMENT '项目角色',
    `project_description` TEXT COMMENT '项目描述',
    `self_evaluation` TEXT COMMENT '自我评价',
    `strengths` TEXT COMMENT '个人优势',
    `education_list` TEXT COMMENT '教育经历列表',
    `experience_list` TEXT COMMENT '工作经历列表',
    `certificate_list` TEXT COMMENT '证书列表',
    `attachment_url` VARCHAR(500) COMMENT '附件简历URL',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_student_id` (`student_id`),
    INDEX `idx_is_default` (`is_default`),
    CONSTRAINT `fk_resumes_student_id` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='简历表';

-- ============================================
-- 7. 投递记录表（applications）
-- ============================================
CREATE TABLE IF NOT EXISTS `applications` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '投递ID',
    `student_id` INT NOT NULL COMMENT '学生ID',
    `job_id` INT NOT NULL COMMENT '岗位ID',
    `resume_id` INT NOT NULL COMMENT '简历ID',
    `status` VARCHAR(20) DEFAULT 'pending' COMMENT '投递状态',
    `cover_letter` TEXT COMMENT '求职信',
    `interview_time` DATETIME COMMENT '面试时间',
    `interview_location` VARCHAR(500) COMMENT '面试地点',
    `interview_result` TEXT COMMENT '面试结果',
    `offer_salary` INT COMMENT 'Offer薪资',
    `offer_letter_url` VARCHAR(500) COMMENT 'Offer函URL',
    `feedback` TEXT COMMENT '反馈信息',
    `viewed_at` DATETIME COMMENT '查看时间',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '投递时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE INDEX `idx_student_job` (`student_id`, `job_id`),
    INDEX `idx_student_id` (`student_id`),
    INDEX `idx_job_id` (`job_id`),
    INDEX `idx_status` (`status`),
    CONSTRAINT `fk_applications_student_id` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_applications_job_id` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_applications_resume_id` FOREIGN KEY (`resume_id`) REFERENCES `resumes` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='投递记录表';

-- ============================================
-- 8. 宣讲会表（career_talks）
-- ============================================
CREATE TABLE IF NOT EXISTS `career_talks` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '宣讲会ID',
    `company_id` INT NOT NULL COMMENT '企业ID',
    `title` VARCHAR(200) NOT NULL COMMENT '宣讲会标题',
    `speaker_name` VARCHAR(50) COMMENT '主讲人姓名',
    `speaker_title` VARCHAR(100) COMMENT '主讲人职位',
    `speaker_avatar` VARCHAR(500) COMMENT '主讲人头像',
    `status` VARCHAR(20) DEFAULT 'pending' COMMENT '活动状态',
    `activity_type` VARCHAR(20) DEFAULT 'career_talk' COMMENT '活动类型',
    `start_time` DATETIME NOT NULL COMMENT '开始时间',
    `end_time` DATETIME NOT NULL COMMENT '结束时间',
    `location` VARCHAR(200) NOT NULL COMMENT '活动地点',
    `max_attendees` INT COMMENT '最大参与人数',
    `current_attendees` INT DEFAULT 0 COMMENT '当前报名人数',
    `description` TEXT COMMENT '活动描述',
    `agenda` TEXT COMMENT '活动议程',
    `poster_url` VARCHAR(500) COMMENT '活动海报',
    `is_online` BOOLEAN DEFAULT FALSE COMMENT '是否线上',
    `online_url` VARCHAR(500) COMMENT '线上直播链接',
    `approval_comment` TEXT COMMENT '审批意见',
    `approved_at` DATETIME COMMENT '审批时间',
    `approved_by` INT COMMENT '审批管理员ID',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_company_id` (`company_id`),
    INDEX `idx_status` (`status`),
    INDEX `idx_start_time` (`start_time`),
    CONSTRAINT `fk_career_talks_company_id` FOREIGN KEY (`company_id`) REFERENCES `companies` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_career_talks_approved_by` FOREIGN KEY (`approved_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='宣讲会表';

-- ============================================
-- 9. 活动报名表（activity_registrations）
-- ============================================
CREATE TABLE IF NOT EXISTS `activity_registrations` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '报名ID',
    `student_id` INT NOT NULL COMMENT '学生ID',
    `career_talk_id` INT NOT NULL COMMENT '宣讲会ID',
    `status` VARCHAR(20) DEFAULT 'registered' COMMENT '报名状态',
    `is_attended` BOOLEAN DEFAULT FALSE COMMENT '是否签到',
    `signed_at` DATETIME COMMENT '签到时间',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '报名时间',
    UNIQUE INDEX `idx_student_talk` (`student_id`, `career_talk_id`),
    INDEX `idx_student_id` (`student_id`),
    INDEX `idx_career_talk_id` (`career_talk_id`),
    CONSTRAINT `fk_activity_registrations_student_id` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_activity_registrations_career_talk_id` FOREIGN KEY (`career_talk_id`) REFERENCES `career_talks` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='活动报名表';

-- ============================================
-- 10. 消息表（messages）
-- ============================================
CREATE TABLE IF NOT EXISTS `messages` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '消息ID',
    `user_id` INT NOT NULL COMMENT '接收用户ID',
    `title` VARCHAR(200) NOT NULL COMMENT '消息标题',
    `content` TEXT NOT NULL COMMENT '消息内容',
    `type` VARCHAR(20) DEFAULT 'system' COMMENT '消息类型',
    `is_read` BOOLEAN DEFAULT FALSE COMMENT '是否已读',
    `related_id` INT COMMENT '关联ID',
    `related_type` VARCHAR(50) COMMENT '关联类型',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '发送时间',
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_is_read` (`is_read`),
    CONSTRAINT `fk_messages_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='消息表';

-- ============================================
-- 11. 通知表（notifications）
-- ============================================
CREATE TABLE IF NOT EXISTS `notifications` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '通知ID',
    `user_id` INT NOT NULL COMMENT '接收用户ID',
    `title` VARCHAR(200) NOT NULL COMMENT '通知标题',
    `content` TEXT NOT NULL COMMENT '通知内容',
    `type` VARCHAR(20) DEFAULT 'info' COMMENT '通知类型',
    `is_read` BOOLEAN DEFAULT FALSE COMMENT '是否已读',
    `link` VARCHAR(500) COMMENT '跳转链接',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_is_read` (`is_read`),
    CONSTRAINT `fk_notifications_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='通知表';

-- ============================================
-- 12. 操作日志表（operation_logs）
-- ============================================
CREATE TABLE IF NOT EXISTS `operation_logs` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '日志ID',
    `user_id` INT COMMENT '操作用户ID',
    `action` VARCHAR(100) NOT NULL COMMENT '操作动作',
    `resource` VARCHAR(50) COMMENT '资源类型',
    `resource_id` INT COMMENT '资源ID',
    `detail` JSON COMMENT '操作详情',
    `ip_address` VARCHAR(50) COMMENT 'IP地址',
    `user_agent` VARCHAR(500) COMMENT '用户代理',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_action` (`action`),
    INDEX `idx_created_at` (`created_at`),
    CONSTRAINT `fk_operation_logs_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='操作日志表';

-- ============================================
-- 索引汇总（供参考）
-- ============================================
-- users: idx_username, idx_email, idx_role
-- students: idx_user_id, idx_student_no, idx_employment_status
-- companies: idx_user_id, idx_status, idx_industry
-- jobs: idx_company_id, idx_status, idx_job_type, idx_is_campus_recruit, idx_created_at
-- job_favorites: idx_student_job (unique), idx_student_id, idx_job_id
-- resumes: idx_student_id, idx_is_default
-- applications: idx_student_job (unique), idx_student_id, idx_job_id, idx_status
-- career_talks: idx_company_id, idx_status, idx_start_time
-- activity_registrations: idx_student_talk (unique), idx_student_id, idx_career_talk_id
-- messages: idx_user_id, idx_is_read
-- notifications: idx_user_id, idx_is_read
-- operation_logs: idx_user_id, idx_action, idx_created_at
