import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "your-long-random-secret-key"
ALGORITHM = "HS256"


def create_access_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)