# 高校就业服务平台 API 接口文档

| 版本号 | 日期 | 作者 | 变更说明 |
|--------|------|------|----------|
| 1.0 | 2026-04-23 | MiniMax Agent | 初稿完成 |
| 1.1 | 2026-04-24 | MiniMax Agent | 新增学生、企业、管理端完整API |
| 1.2 | 2026-11-03 | 项目组 | 按后端实际路由全面校准，补齐消息、偏好、备份与导出接口 |

---

## 一、概述

### 1.1 基础信息

- **Base URL**: `http://localhost:8000/api/v1`
- **认证方式**: JWT Bearer Token
- **数据格式**: JSON（文件上传使用 `multipart/form-data`）
- **字符编码**: UTF-8

### 1.2 请求头

```
Content-Type: application/json
Authorization: Bearer {token}
```

> 注意：后端关闭了自动尾斜杠重定向（`redirect_slashes=False`），请严格按本文档路径调用。

### 1.3 全局错误码

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未授权/登录过期 |
| 403 | 无权限访问 |
| 404 | 资源不存在 |
| 422 | 参数校验失败 |
| 429 | 请求过于频繁 |
| 500 | 服务器内部错误 |

---

## 二、认证模块 /auth

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| POST | `/auth/register` | 否 | 用户注册（限流 5 次/分钟） |
| POST | `/auth/login` | 否 | JSON 登录（限流 10 次/分钟） |
| POST | `/auth/login/json` | 否 | JSON 登录（兼容接口） |
| POST | `/auth/sms/send` | 否 | 发送短信验证码（限流 3 次/分钟） |
| POST | `/auth/phone/login` | 否 | 手机号验证码登录 |
| GET | `/auth/wechat/qrcode` | 否 | 获取微信登录二维码（演示实现） |
| GET | `/auth/wechat/qrstatus/{scene}` | 否 | 查询扫码状态（演示实现） |
| GET | `/auth/me` | 是 | 获取当前用户信息 |
| POST | `/auth/password` | 是 | 修改密码 |
| GET | `/auth/preferences` | 是 | 获取个人偏好设置 |
| PUT | `/auth/preferences` | 是 | 保存个人偏好设置 |
| GET | `/auth/public/stats` | 否 | 首页公开统计数据 |

### 2.1 用户注册

```json
POST /auth/register
{
  "username": "string",
  "email": "user@example.com",
  "password": "string（至少6位）",
  "role": "student | company | admin | counselor"
}
```

### 2.2 用户登录

```json
POST /auth/login
{
  "username": "string",
  "password": "string",
  "role": "student | company | admin | counselor"
}
```

响应：

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2.3 获取当前用户信息

```json
GET /auth/me
```

```json
{
  "id": 1,
  "username": "string",
  "email": "user@example.com",
  "role": "student",
  "is_active": true,
  "is_verified": false,
  "created_at": "2026-11-03T10:00:00Z",
  "student_profile": { "id": 1, "student_no": "20220001", "name": "张三" },
  "company_profile": null
}
```

### 2.4 修改密码

```json
POST /auth/password
{
  "old_password": "string",
  "new_password": "string（至少6位）"
}
```

### 2.5 偏好设置

`GET /auth/preferences` 返回任意 JSON 对象，例如：

```json
{
  "preferences": { "jobType": "full_time", "city": "北京" },
  "notifications": { "newApplicant": true, "weeklyReport": false }
}
```

`PUT /auth/preferences` 请求体为任意 JSON 对象，整体覆盖保存。

---

## 三、学生端 API

### 3.1 仪表盘 /student/dashboard

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/student/dashboard/` | 学生首页统计（投递数、收藏数、报名数等） |

### 3.2 简历管理 /student/resumes

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/student/resumes/` | 简历列表 |
| GET | `/student/resumes/{resume_id}` | 简历详情 |
| POST | `/student/resumes/` | 创建简历 |
| PUT | `/student/resumes/{resume_id}` | 更新简历 |
| DELETE | `/student/resumes/{resume_id}` | 删除简历 |
| POST | `/student/resumes/{resume_id}/set-default` | 设为默认简历 |
| POST | `/student/resumes/{resume_id}/suggestions` | 生成 AI 优化建议 |
| POST | `/student/resumes/upload` | 上传 PDF 简历（≤10MB，`multipart/form-data`，字段名 `file`） |

创建简历请求示例（`student_id` 由登录身份自动绑定，无需传入）：

```json
{
  "title": "我的简历",
  "is_default": true,
  "visibility": "public | protected | private",
  "template": "default",
  "personal_name": "张三",
  "personal_phone": "13800138000",
  "personal_email": "zhangsan@example.com",
  "education_school": "某某大学",
  "education_major": "计算机科学"
}
```

### 3.3 岗位搜索 /student/jobs

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/student/jobs/` | 岗位搜索（分页） |
| GET | `/student/jobs/favorites` | 我的收藏列表 |
| GET | `/student/jobs/{job_id}` | 岗位详情 |
| POST | `/student/jobs/{job_id}/collect` | 收藏岗位 |
| DELETE | `/student/jobs/{job_id}/collect` | 取消收藏 |
| POST | `/student/jobs/{job_id}/apply` | 投递岗位 |

搜索参数：`keyword`、`job_type`、`province`、`city`、`salary_min`、`salary_max`、`page`、`page_size`。

列表响应为分页对象：

```json
{
  "total": 120,
  "page": 1,
  "page_size": 20,
  "data": [
    {
      "id": 1,
      "company_id": 1,
      "title": "前端开发工程师",
      "job_type": "full_time",
      "salary_min": 8000,
      "salary_max": 15000,
      "province": "北京",
      "city": "北京市",
      "headcount": 5,
      "application_count": 23,
      "company_name": "某科技有限公司",
      "company_logo": "https://..."
    }
  ]
}
```

投递请求体（均可选；不传 `resume_id` 时使用默认简历）：

```json
{
  "resume_id": 1,
  "cover_letter": "自荐信内容..."
}
```

### 3.4 投递管理 /student/applications

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/student/applications/` | 投递列表（`status`、`page`、`page_size`） |
| POST | `/student/applications/` | 创建投递（`job_id`、`resume_id`、`cover_letter`） |
| POST | `/student/applications/{application_id}/withdraw` | 撤回投递 |

### 3.5 宣讲会 /student/career-talks

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/student/career-talks/` | 宣讲会列表 |
| GET | `/student/career-talks/my-registrations` | 我的报名列表 |
| GET | `/student/career-talks/{talk_id}` | 宣讲会详情 |
| POST | `/student/career-talks/{talk_id}/register` | 报名 |
| DELETE | `/student/career-talks/{talk_id}/cancel` | 取消报名 |

### 3.6 个人信息 /student/profile

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/student/profile/` | 获取个人信息 |
| PUT | `/student/profile/` | 更新个人信息 |
| POST | `/student/profile/avatar` | 上传头像（`multipart/form-data`，字段名 `file`） |

更新参数（均为可选）：

```json
{
  "name": "string",
  "gender": "male | female",
  "phone": "string",
  "major": "string",
  "class_name": "string",
  "graduation_year": 2026,
  "employment_status": "unemployed | searching | offered | signed | further_study | startup"
}
```

### 3.7 消息中心 /student/messages

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/student/messages/` | 消息列表（`type`、`is_read`、`page`、`page_size`） |
| GET | `/student/messages/unread-count` | 未读数量 |
| POST | `/student/messages/{message_id}/read` | 单条已读 |
| POST | `/student/messages/read-all` | 全部已读 |
| DELETE | `/student/messages/{message_id}` | 删除消息 |

---

## 四、企业端 API

### 4.1 工作台与数据 /company

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/company/dashboard/` | 企业工作台数据 |
| GET | `/company/analytics/` | 招聘数据分析 |

### 4.2 岗位管理 /company/jobs

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/company/jobs/` | 企业岗位列表（分页） |
| GET | `/company/jobs/{job_id}` | 岗位详情 |
| GET | `/company/jobs/{job_id}/applicants` | 该岗位投递人列表 |
| POST | `/company/jobs/` | 创建岗位 |
| PUT | `/company/jobs/{job_id}` | 更新岗位 |
| DELETE | `/company/jobs/{job_id}` | 关闭岗位 |
| POST | `/company/jobs/{job_id}/refresh` | 刷新岗位 |

创建岗位参数：

```json
{
  "title": "string",
  "job_type": "full_time | part_time | internship | practice",
  "salary_min": 8000,
  "salary_max": 15000,
  "province": "string",
  "city": "string",
  "district": "string",
  "address": "string",
  "description": "string",
  "requirement": "string",
  "benefit": "string",
  "headcount": 5
}
```

岗位列表响应为 `{ total, page, page_size, data }` 分页对象。

### 4.3 简历与投递 /company/resumes

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/company/resumes/applications/` | 收到的投递（`job_id`、`status`、分页） |
| GET | `/company/resumes/applications/{application_id}` | 投递详情 |
| PUT | `/company/resumes/applications/{application_id}/status` | 更新投递状态 |
| GET | `/company/resumes/talent-pool/` | 人才库 |

更新投递状态参数：

```json
{
  "status": "viewed | passed | failed | offered | rejected",
  "feedback": "string",
  "interview_time": "2026-11-05T10:00:00Z",
  "interview_location": "string",
  "offer_salary": 12000
}
```

> 状态变更后会自动向学生发送一条站内消息。

### 4.4 宣讲会管理 /company/career-talks

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/company/career-talks/` | 宣讲会列表 |
| GET | `/company/career-talks/{talk_id}` | 宣讲会详情 |
| POST | `/company/career-talks/` | 创建宣讲会 |
| PUT | `/company/career-talks/{talk_id}` | 更新宣讲会 |
| DELETE | `/company/career-talks/{talk_id}` | 删除宣讲会 |
| GET | `/company/career-talks/{talk_id}/registrations` | 报名列表 |

### 4.5 企业信息 /company/profile

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/company/profile/` | 获取企业信息 |
| PUT | `/company/profile/` | 更新企业信息 |
| POST | `/company/profile/logo` | 上传企业 Logo |
| POST | `/company/profile/license/upload` | 上传营业执照（PDF/JPG/PNG，≤10MB） |

---

## 五、管理端 API

### 5.1 数据统计 /admin/statistics

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/admin/statistics/all` | 汇总统计 |
| GET | `/admin/statistics/stats` | 仪表盘核心指标 |
| GET | `/admin/statistics/employment-trend` | 就业趋势（`days`，默认30） |
| GET | `/admin/statistics/employment-status-distribution` | 就业状态分布 |
| GET | `/admin/statistics/region-distribution` | 区域分布 |
| GET | `/admin/statistics/department-stats` | 院系统计 |
| GET | `/admin/statistics/major-stats` | 专业统计 |
| GET | `/admin/statistics/salary-distribution` | 薪资分布 |
| GET | `/admin/statistics/conversion-funnel` | 招聘转化漏斗 |
| GET | `/admin/statistics/company-scale-distribution` | 企业规模分布 |
| GET | `/admin/statistics/activity-stats` | 活动统计 |
| GET | `/admin/statistics/export` | 导出学生就业明细 CSV |

### 5.2 学生管理 /admin/students

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/admin/students` | 学生列表（`employment_status`、`major`、`graduation_year`、`is_key_assistance`、`keyword`、分页） |
| POST | `/admin/students` | 新增学生（同时创建登录账号） |
| GET | `/admin/students/{student_id}` | 学生详情 |
| PUT | `/admin/students/{student_id}` | 更新学生信息/就业状态 |
| GET | `/admin/students/{student_id}/employment-status/update` | 单独更新就业状态（兼容旧接口） |

新增学生参数：

```json
{
  "student_no": "20220001",
  "name": "张三",
  "username": "可选，默认使用学号",
  "email": "可选，默认 学号@campus.edu.cn",
  "password": "可选，默认 123456",
  "college": "string",
  "major": "string",
  "class_name": "string",
  "graduation_year": 2026,
  "phone": "string"
}
```

### 5.3 企业管理 /admin/companies

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/admin/companies` | 企业列表（`status`、`keyword`、`industry`、分页） |
| GET | `/admin/companies/{company_id}` | 企业详情 |
| POST | `/admin/companies/{company_id}/approve` | 审核通过（无请求体） |
| POST | `/admin/companies/{company_id}/reject` | 审核拒绝（`comment`） |
| POST | `/admin/companies/{company_id}/blacklist` | 加入黑名单 |
| DELETE | `/admin/companies/{company_id}/remove-blacklist` | 移出黑名单 |

### 5.4 岗位管理 /admin/jobs

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/admin/jobs` | 岗位列表（`status`、`keyword`、分页） |
| GET | `/admin/jobs/{job_id}` | 岗位详情 |
| POST | `/admin/jobs/{job_id}/approve` | 审核岗位 |
| POST | `/admin/jobs/{job_id}/top` | 置顶岗位 |
| POST | `/admin/jobs/{job_id}/highlight` | 优选岗位 |

审核参数：`{ "status": "approved | rejected", "comment": "审核备注" }`

### 5.5 活动管理 /admin/activities

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/admin/activities/career-talks` | 宣讲会列表 |
| POST | `/admin/activities/career-talks` | 创建宣讲会（需传 `company_id`） |
| GET | `/admin/activities/career-talks/{talk_id}` | 宣讲会详情 |
| PUT | `/admin/activities/career-talks/{talk_id}` | 更新宣讲会 |
| DELETE | `/admin/activities/career-talks/{talk_id}` | 删除宣讲会 |
| POST | `/admin/activities/career-talks/{talk_id}/approve` | 审核宣讲会 |
| GET | `/admin/activities/career-talks/{talk_id}/registrations` | 报名列表 |
| POST | `/admin/activities/registrations/{registration_id}/sign-in` | 签到 |

### 5.6 系统设置 /admin/system

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/admin/system/users` | 用户列表（`role`、`keyword`、分页） |
| POST | `/admin/system/users` | 创建管理员/辅导员账号 |
| PUT | `/admin/system/users/{user_id}` | 更新用户（邮箱、角色、密码、状态） |
| DELETE | `/admin/system/users/{user_id}` | 删除用户 |
| PUT | `/admin/system/users/{user_id}/toggle-active` | 启用/禁用用户 |
| GET | `/admin/system/roles` | 角色列表 |
| GET | `/admin/system/operation-logs` | 操作日志 |
| GET | `/admin/system` | 获取系统设置（通知、备份频率） |
| PUT | `/admin/system` | 保存系统设置 |
| GET | `/admin/system/backups` | 备份文件列表 |
| POST | `/admin/system/backup` | 立即创建全量 JSON 备份 |
| GET | `/admin/system/backups/{filename}` | 下载备份文件 |
| DELETE | `/admin/system/backups/{filename}` | 删除备份文件 |

---

## 六、数据模型

### 6.1 用户角色 (UserRole)
- `admin`: 超级管理员
- `student`: 学生
- `company`: 企业
- `counselor`: 辅导员

### 6.2 就业状态 (EmploymentStatus)
- `unemployed`: 未就业
- `searching`: 求职中
- `offered`: 已录用（待签约）
- `signed`: 已签约
- `further_study`: 升学
- `startup`: 创业

### 6.3 企业状态 (CompanyStatus)
- `pending`: 待审核
- `approved`: 已通过
- `rejected`: 已拒绝
- `blacklisted`: 黑名单

### 6.4 岗位状态 (JobStatus)
- `draft`: 草稿
- `pending`: 待审核
- `approved`: 已通过
- `rejected`: 已拒绝
- `closed`: 已关闭

### 6.5 投递状态 (ApplicationStatus)
- `pending`: 待处理
- `viewed`: 已查看
- `passed`: 已通过
- `failed`: 未通过
- `offered`: 已发 offer
- `rejected`: 已拒绝
- `withdrawn`: 已撤回

### 6.6 活动状态 (ActivityStatus)
- `draft`: 草稿
- `pending`: 待审核
- `approved`: 已通过
- `rejected`: 已拒绝
- `cancelled`: 已取消
- `ended`: 已结束

### 6.7 消息类型（业务约定）
- `system`: 系统通知
- `application`: 投递反馈
- `activity`: 活动提醒

---

## 七、启动说明

### 7.1 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

### 7.2 配置环境变量
在 `backend` 目录创建 `.env`：

```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/campus_employment
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-change-in-production
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### 7.3 启动服务
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 7.4 访问文档
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/api/v1/openapi.json
