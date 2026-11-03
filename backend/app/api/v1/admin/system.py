from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from datetime import datetime
import json
import os

from app.core.database import get_db, Base
from app.core.security import require_roles, get_password_hash
from app.models.user import User, UserRole
from app.models.log import OperationLog
from app.schemas.user import UserResponse, UserCreate, UserUpdate

router = APIRouter(tags=["管理端-系统设置"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
SETTINGS_FILE = os.path.join(DATA_DIR, "system_settings.json")

DEFAULT_SETTINGS = {
    "notifications": {
        "system": True,
        "jobReview": True,
        "activityReminder": True,
        "email": False
    },
    "backup": {
        "frequency": "weekly"
    }
}


def _read_settings() -> dict:
    if not os.path.exists(SETTINGS_FILE):
        return json.loads(json.dumps(DEFAULT_SETTINGS))
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return json.loads(json.dumps(DEFAULT_SETTINGS))
    merged = json.loads(json.dumps(DEFAULT_SETTINGS))
    for section, values in data.items():
        if isinstance(values, dict) and isinstance(merged.get(section), dict):
            merged[section].update(values)
        else:
            merged[section] = values
    return merged


def _write_settings(data: dict) -> dict:
    os.makedirs(DATA_DIR, exist_ok=True)
    current = _read_settings()
    for section, values in data.items():
        if isinstance(values, dict) and isinstance(current.get(section), dict):
            current[section].update(values)
        else:
            current[section] = values
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(current, f, ensure_ascii=False, indent=2)
    return current


def _backup_records() -> list:
    if not os.path.isdir(BACKUP_DIR):
        return []
    records = []
    for name in os.listdir(BACKUP_DIR):
        if not name.endswith(".json"):
            continue
        path = os.path.join(BACKUP_DIR, name)
        stat = os.stat(path)
        records.append({
            "filename": name,
            "time": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "type": "手动",
            "size": f"{stat.st_size / 1024 / 1024:.2f} MB" if stat.st_size > 1024 * 1024 else f"{max(1, stat.st_size // 1024)} KB",
            "status": "success"
        })
    return sorted(records, key=lambda r: r["time"], reverse=True)


def _serialize_row(row) -> dict:
    result = {}
    for key, value in row._mapping.items():
        if isinstance(value, datetime):
            result[key] = value.isoformat()
        elif isinstance(value, bytes):
            result[key] = value.decode("utf-8", errors="ignore")
        else:
            result[key] = value
    return result



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


@router.put("/users/{user_id}", response_model=UserResponse)
def update_admin_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    data = user_data.model_dump(exclude_unset=True)
    if "email" in data and data["email"] != user.email:
        existing = db.query(User).filter(User.email == data["email"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="邮箱已被使用")
        user.email = data["email"]
    if "role" in data:
        user.role = data["role"]
    if "is_active" in data:
        if user.id == current_user.id and not data["is_active"]:
            raise HTTPException(status_code=400, detail="不能禁用自己的账号")
        user.is_active = data["is_active"]
    if data.get("password"):
        user.hashed_password = get_password_hash(data["password"])

    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}")
def delete_admin_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="不能删除自己的账号")

    try:
        db.delete(user)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="该账号存在关联数据，无法删除")

    return {"message": "删除成功"}


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


@router.get("")
@router.get("/")
def get_system_settings(
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    return _read_settings()


@router.put("")
@router.put("/")
def update_system_settings(
    data: dict,
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    return _write_settings(data)


@router.get("/backups")
def list_backups(
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    return _backup_records()


@router.post("/backup")
def create_backup(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path = os.path.join(BACKUP_DIR, filename)

    payload = {
        "created_at": datetime.now().isoformat(),
        "tables": {}
    }
    for table in Base.metadata.sorted_tables:
        rows = db.execute(table.select()).fetchall()
        payload["tables"][table.name] = [_serialize_row(row) for row in rows]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, default=str)

    records = _backup_records()
    return records[0] if records else {"filename": filename, "status": "success"}


@router.get("/backups/{filename}")
def download_backup(
    filename: str,
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    if os.path.basename(filename) != filename or not filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="非法的文件名")
    path = os.path.join(BACKUP_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="备份文件不存在")
    return FileResponse(path, filename=filename, media_type="application/json")


@router.delete("/backups/{filename}")
def delete_backup(
    filename: str,
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    if os.path.basename(filename) != filename or not filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="非法的文件名")
    path = os.path.join(BACKUP_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="备份文件不存在")
    os.remove(path)
    return {"message": "删除成功"}
