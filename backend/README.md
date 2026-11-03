# 高校就业服务平台 - 后端

## 项目简介

基于 FastAPI 的高校就业服务平台后端 API 服务。

## 技术栈

- **框架**: FastAPI
- **ORM**: SQLAlchemy 2.0
- **数据库**: MySQL + Redis
- **任务队列**: Celery + Redis
- **认证**: JWT (python-jose)
- **密码加密**: bcrypt (passlib)

## 项目结构

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py          # 认证模块
│   │       ├── student/         # 学生端API
│   │       ├── company/         # 企业端API
│   │       └── admin/           # 管理端API
│   ├── core/
│   │   ├── config.py           # 配置管理
│   │   ├── database.py         # 数据库连接
│   │   └── security.py         # 安全认证
│   ├── models/                 # 数据模型
│   ├── schemas/                 # Pydantic schemas
│   ├── tasks/                  # Celery异步任务
│   └── main.py                 # 应用入口
├── requirements.txt
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件:

```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/campus_employment
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-change-in-production
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
```

### 3. 启动服务

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 访问 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 模块

### 认证 /auth
- POST /auth/login - 用户登录
- POST /auth/register - 用户注册
- GET /auth/me - 获取当前用户

### 学生端 /student
- /resumes - 简历管理
- /jobs - 岗位搜索
- /applications - 投递管理
- /career-talks - 宣讲会
- /profile - 个人信息

### 企业端 /company
- /jobs - 岗位管理
- /resumes - 简历筛选
- /career-talks - 宣讲会管理
- /profile - 企业信息

### 管理端 /admin
- /dashboard - 数据统计
- /students - 学生管理
- /companies - 企业管理
- /jobs - 岗位审核
- /activities - 活动管理
- /system - 系统设置

## 数据模型

### 用户角色
- admin - 超级管理员
- student - 学生
- company - 企业
- counselor - 辅导员

### 就业状态
- unemployed - 未就业
- searching - 求职中
- offered - 已签约
- signed - 已签约(正式)
- further_study - 升学
- startup - 创业

## 开发说明

### 创建数据库迁移

```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 运行 Celery Worker

```bash
celery -A app.celery_app worker --loglevel=info
```

### 运行 Celery Beat (定时任务)

```bash
celery -A app.celery_app beat --loglevel=info
```
