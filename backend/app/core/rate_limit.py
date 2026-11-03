"""
限流工具模块

使用 Redis 实现"滑动窗口"限流，防止恶意请求
- rate_limit: FastAPI 依赖函数，可直接用于接口
"""
from fastapi import HTTPException, Request, status

from app.core.redis_client import incr_with_expire


def get_client_ip(request: Request) -> str:
    """获取客户端 IP（支持反向代理场景）"""
    # 优先取反向代理设置的 X-Forwarded-For
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    # 否则取直连 IP
    return request.client.host if request.client else "unknown"


def rate_limit(key_prefix: str, max_requests: int, window_seconds: int):
    """
    限流依赖工厂

    Args:
        key_prefix: 限流键前缀（区分不同接口）
        max_requests: 窗口内允许的最大请求数
        window_seconds: 窗口时间（秒）

    用法:
        @router.post("/login", dependencies=[Depends(rate_limit("login", 5, 60))])
        def login(...):
            ...
    """
    async def _check(request: Request):
        client_ip = get_client_ip(request)
        # 已登录用户优先用 user_id，否则用 IP
        user_id = request.headers.get("X-User-Id", "")
        identifier = f"user:{user_id}" if user_id else f"ip:{client_ip}"

        key = f"ratelimit:{key_prefix}:{identifier}"

        count = incr_with_expire(key, window_seconds)

        if count > max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"请求过于频繁，请 {window_seconds} 秒后再试"
            )

    return _check
