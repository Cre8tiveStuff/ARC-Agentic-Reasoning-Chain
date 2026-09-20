import redis
import hashlib

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


def acquire_lock(func_name, args, kwargs):
    key = f"lock:{hashlib.sha256(f'{func_name}:{args}:{kwargs}'.encode()).hexdigest()}"
    return r.set(key, "processing", nx=True, ex=60)


def release_lock(func_name, args, kwargs):
    key = f"lock:{hashlib.sha256(f'{func_name}:{args}:{kwargs}'.encode()).hexdigest()}"
    r.delete(key)