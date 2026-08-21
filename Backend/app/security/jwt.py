import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"


def create_access_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)