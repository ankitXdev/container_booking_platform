import jwt
from datetime import datetime, timezone

from app.security.jwt import (
    create_access_token,
    SECRET_KEY,
    ALGORITHM
)


def test_create_access_token():

    user_id = 1

    token = create_access_token(user_id)

    assert token is not None
    assert isinstance(token, str)


def test_access_token_contains_user_id():

    user_id = 123

    token = create_access_token(user_id)

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    assert payload["sub"] == "123"


def test_access_token_contains_expiration():

    token = create_access_token(1)

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    assert "exp" in payload


def test_access_token_expiration_is_valid():

    token = create_access_token(1)

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    expiration = payload["exp"]

    current_time = datetime.now(timezone.utc).timestamp()

    assert expiration > current_time


def test_access_token_can_be_decoded():

    token = create_access_token(1)

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    assert payload["sub"] == "1"