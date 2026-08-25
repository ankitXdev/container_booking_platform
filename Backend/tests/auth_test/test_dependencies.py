import jwt
import pytest

from unittest.mock import MagicMock

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.security.dependencies import get_current_user
from app.security.jwt import (
    SECRET_KEY,
    ALGORITHM,
    create_access_token
)


# =========================================================
# VALID TOKEN
# =========================================================

def test_get_current_user_success():

    user_id = 1

    token = create_access_token(user_id)

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token
    )

    mock_user = MagicMock()
    mock_user.user_id = user_id

    db = MagicMock()

    db.query.return_value.filter.return_value.first.return_value = mock_user

    result = get_current_user(
        credentials=credentials,
        db=db
    )

    assert result == mock_user

    db.query.assert_called_once()


# =========================================================
# INVALID TOKEN
# =========================================================

def test_get_current_user_invalid_token():

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="this-is-not-a-valid-jwt"
    )

    db = MagicMock()

    with pytest.raises(HTTPException) as exc_info:

        get_current_user(
            credentials=credentials,
            db=db
        )

    assert exc_info.value.status_code == 401

    assert exc_info.value.detail == "Invalid or expired token"


# =========================================================
# TOKEN WITHOUT SUB
# =========================================================

def test_get_current_user_missing_sub():

    payload = {
        "exp": 9999999999
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token
    )

    db = MagicMock()

    with pytest.raises(HTTPException) as exc_info:

        get_current_user(
            credentials=credentials,
            db=db
        )

    assert exc_info.value.status_code == 401

    assert exc_info.value.detail == "Invalid or expired token"


# =========================================================
# INVALID USER ID
# =========================================================

def test_get_current_user_invalid_user_id():

    payload = {
        "sub": "not-a-number",
        "exp": 9999999999
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token
    )

    db = MagicMock()

    with pytest.raises(HTTPException) as exc_info:

        get_current_user(
            credentials=credentials,
            db=db
        )

    assert exc_info.value.status_code == 401

    assert exc_info.value.detail == "Invalid or expired token"


# =========================================================
# USER DOES NOT EXIST
# =========================================================

def test_get_current_user_user_not_found():

    token = create_access_token(999)

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token
    )

    db = MagicMock()

    # Database cannot find this user
    db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:

        get_current_user(
            credentials=credentials,
            db=db
        )

    assert exc_info.value.status_code == 401

    assert exc_info.value.detail == "User not found"


# =========================================================
# EXPIRED TOKEN
# =========================================================

def test_get_current_user_expired_token():

    payload = {
        "sub": "1",
        "exp": 1
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token
    )

    db = MagicMock()

    with pytest.raises(HTTPException) as exc_info:

        get_current_user(
            credentials=credentials,
            db=db
        )

    assert exc_info.value.status_code == 401

    assert exc_info.value.detail == "Invalid or expired token"