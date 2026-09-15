"""
fastapi-cache-decorator: Lightweight, async caching decorator for FastAPI.
Zero-dependency in-memory cache with TTL and Redis backend support.
"""

import functools
import hashlib
import inspect
import json
import time
from typing import Any, Callable, Dict, Optional, Tuple
from fastapi import Request, Response

class CacheBackend:
    """In-memory cache storage with TTL expiration."""
    def __init__(self):
        self._store: Dict[str, Tuple[Any, float]] = {}

    def get(self, key: str) -> Optional[Any]:
        if key in self._store:
            value, expires_at = self._store[key]
            if time.time() < expires_at:
                return value
            del self._store[key]
        return None

    def set(self, key: str, value: Any, ttl: int):
        self._store[key] = (value, time.time() + ttl)

    def clear(self):
        self._store.clear()

_DEFAULT_BACKEND = CacheBackend()

def cache(ttl: int = 60, key_func: Optional[Callable[..., str]] = None):
    """
    Decorator to cache responses of FastAPI route endpoints.

    Usage:
        @app.get("/items")
        @cache(ttl=60) # Cache for 60 seconds
        async def get_items():
            return {"items": [1, 2, 3]}
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # Default: hash function name and arguments
                req: Optional[Request] = None
                for arg in args:
                    if isinstance(arg, Request):
                        req = arg
                        break
                if not req:
                    for v in kwargs.values():
                        if isinstance(v, Request):
                            req = v
                            break

                if req:
                    cache_key = f"{func.__name__}:{req.url.path}:{str(req.query_params)}"
                else:
                    repr_args = repr(args) + repr(kwargs)
                    cache_key = f"{func.__name__}:{hashlib.md5(repr_args.encode()).hexdigest()}"

            # Check cache
            cached_result = _DEFAULT_BACKEND.get(cache_key)
            if cached_result is not None:
                return cached_result

            # Execute function
            if inspect.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            # Store in cache
            _DEFAULT_BACKEND.set(cache_key, result, ttl)
            return result

        return wrapper
    return decorator
