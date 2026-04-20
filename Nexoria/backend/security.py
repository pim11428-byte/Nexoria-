import time
from fastapi import HTTPException

RATE_LIMIT = {}
WINDOW = 10          # окно в секундах
MAX_REQUESTS = 5     # максимум запросов за окно


def rate_limit(key: str):
    now = time.time()

    if key not in RATE_LIMIT:
        RATE_LIMIT[key] = []

    RATE_LIMIT[key] = [t for t in RATE_LIMIT[key] if now - t < WINDOW]

    if len(RATE_LIMIT[key]) >= MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="Слишком много запросов. Подождите немного.")

    RATE_LIMIT[key].append(now)
