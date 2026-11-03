"""
Redis 客户端工具模块

提供统一的 Redis 连接和常用操作封装
- 缓存读写（get_cache / set_cache）
- 限流计数（incr_with_expire）
"""
import json
from typing import Any, Optional

import redis

from app.core.config import settings


# 全局 Redis 客户端（连接池）
redis_client = redis.Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,   # 自动把 bytes 转成 str，方便使用
    socket_timeout=5,        # 5 秒超时
    socket_connect_timeout=5,
)


def get_cache(key: str) -> Optional[Any]:
    """
    从 Redis 读取缓存数据（自动 JSON 反序列化）

    Args:
        key: 缓存键

    Returns:
        反序列化后的对象，如果不存在或 Redis 出错返回 None
    """
    try:
        data = redis_client.get(key)
        if data is None:
            return None
        return json.loads(data)
    except (redis.RedisError, json.JSONDecodeError):
        return None


def set_cache(key: str, value: Any, expire: int = 300) -> bool:
    """
    把数据写入 Redis 缓存（自动 JSON 序列化）

    Args:
        key: 缓存键
        value: 要缓存的数据（必须是 JSON 可序列化的）
        expire: 过期时间（秒），默认 5 分钟

    Returns:
        True 成功，False 失败
    """
    try:
        redis_client.setex(
            key,
            expire,
            json.dumps(value, ensure_ascii=False, default=str)
        )
        return True
    except (redis.RedisError, TypeError):
        return False


def delete_cache(key: str) -> bool:
    """删除指定 key 的缓存"""
    try:
        redis_client.delete(key)
        return True
    except redis.RedisError:
        return False


def delete_cache_pattern(pattern: str) -> int:
    """
    按模式批量删除缓存（如 'job:list:*'）

    Returns:
        删除的 key 数量
    """
    try:
        keys = redis_client.keys(pattern)
        if keys:
            return redis_client.delete(*keys)
        return 0
    except redis.RedisError:
        return 0


def incr_with_expire(key: str, expire: int) -> int:
    """
    限流专用：原子自增 + 设置过期时间

    用于实现"X 秒内最多 N 次请求"的限流逻辑。
    第一次调用时设置过期时间，后续自增不会重置过期时间。

    Args:
        key: 限流键
        expire: 过期时间（秒）

    Returns:
        自增后的值
    """
    try:
        pipe = redis_client.pipeline()
        pipe.incr(key)
        pipe.expire(key, expire)
        results = pipe.execute()
        return results[0]
    except redis.RedisError:
        return 0
