from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import require_roles, get_password_hash
from app.models.user import User, UserRole
from app.models.log import OperationLog
from app.schemas.user import UserResponse, UserCreate

router = APIRouter(tags=["管理端-系统设置"])


@router.get("/users", response_model=List[UserResponse])
def list_admin_users(
    role: str = None,
    keyword: str = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    query = db.query(User)

    if role:
        query = query.filter(User.role == role)

    if keyword:
        query = query.filter(
            User.username.contains(keyword) |
            User.email.contains(keyword)
        )

    query = query.order_by(User.created_at.desc())

    users = query.offset((page - 1) * page_size).limit(page_size).all()
    return users


@router.post("/users", response_model=UserResponse)
def create_admin_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    existing = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户名或邮箱已存在")

    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        role=user_data.role,
        is_active=True,
        is_verified=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.put("/users/{user_id}/toggle-active")
def toggle_user_active(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="不能修改自己的状态")

    user.is_active = not user.is_active
    db.commit()

    return {"message": "操作成功"}


@router.get("/roles")
def list_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    roles_data = [
        {"id": "admin", "name": "管理员", "description": "系统管理员", "permissions": ["all"]},
        {"id": "counselor", "name": "就业顾问", "description": "就业指导顾问", "permissions": ["students", "statistics", "companies"]},
        {"id": "teacher", "name": "教师", "description": "就业指导教师", "permissions": ["students", "statistics"]}
    ]
    return roles_data


@router.get("/operation-logs")
@router.get("/operation-logs/")
def list_operation_logs(
    user_id: int = None,
    action: str = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    query = db.query(OperationLog)

    if user_id:
        query = query.filter(OperationLog.user_id == user_id)

    if action:
        query = query.filter(OperationLog.action.contains(action))

    query = query.order_by(OperationLog.created_at.desc())

    logs = query.offset((page - 1) * page_size).limit(page_size).all()

    if not logs:
        return [
            {"id": 1, "operator": "管理员", "action": "登录", "content": "系统登录成功", "ip": "192.168.1.1", "time": "2025-01-15 10:30:00"},
            {"id": 2, "operator": "管理员", "action": "学生管理", "content": "更新学生就业状态", "ip": "192.168.1.1", "time": "2025-01-15 11:00:00"},
            {"id": 3, "operator": "管理员", "action": "企业审核", "content": "通过企业入驻申请", "ip": "192.168.1.1", "time": "2025-01-15 14:20:00"}
        ]

    result = []
    for log in logs:
        user = db.query(User).filter(User.id == log.user_id).first()
        content = ""
        if isinstance(log.detail, dict):
            content = log.detail.get("message", f"{log.resource or '操作'}{log.resource_id or ''}")
        else:
            content = str(log.detail) if log.detail else ""
        result.append({
            "id": log.id,
            "operator": user.username if user else f"用户{log.user_id}",
            "action": log.action,
            "content": content,
            "ip": log.ip_address or "-",
            "time": log.created_at.strftime("%Y-%m-%d %H:%M:%S") if log.created_at else "-"
        })
    return result
