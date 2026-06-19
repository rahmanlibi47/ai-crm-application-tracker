from fastapi import HTTPException

from app.core.redis_client import redis_client


def check_rate_limit(
    key: str,
    limit: int,
    window_seconds: int
):
    current_count = redis_client.get(key)

    if current_count is None:
        redis_client.set(
            key,
            1,
            ex=window_seconds
        )
        return

    current_count = int(current_count)

    if current_count >= limit:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )

    redis_client.incr(key)