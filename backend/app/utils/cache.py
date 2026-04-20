import json
import functools
from flask import request
from redis import Redis
from config import Config

redis_client = None

def get_redis():
    """Get Redis client instance"""
    global redis_client
    if redis_client is None:
        try:
            redis_client = Redis.from_url(Config.REDIS_URL, decode_responses=True)
            redis_client.ping()
        except Exception as e:
            print(f"Redis connection failed: {e}")
            return None
    return redis_client

def cache_key(prefix):
    """Generate cache key based on request URL and parameters"""
    args = request.args.to_dict()
    if args:
        params = '_'.join(f"{k}={v}" for k, v in sorted(args.items()))
        return f"{prefix}:{params}"
    return prefix

def cached(timeout=300, prefix='api'):
    """
    Cache decorator for API endpoints
    
    Args:
        timeout: Cache timeout in seconds (default: 5 minutes)
        prefix: Cache key prefix
    """
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            r = get_redis()
            if r is None:
                return f(*args, **kwargs)
            
            key = f"{prefix}:{request.path}:{cache_key(prefix)}"
            
            try:
                cached_data = r.get(key)
                if cached_data:
                    return json.loads(cached_data)
            except Exception:
                pass
            
            response = f(*args, **kwargs)
            
            try:
                if hasattr(response, 'get'):
                    r.setex(key, timeout, json.dumps(response))
            except Exception:
                pass
            
            return response
        return decorated_function
    return decorator

def invalidate_cache(prefix):
    """Invalidate cache by prefix"""
    r = get_redis()
    if r is None:
        return
    
    try:
        keys = r.keys(f"{prefix}:*")
        if keys:
            r.delete(*keys)
    except Exception:
        pass
