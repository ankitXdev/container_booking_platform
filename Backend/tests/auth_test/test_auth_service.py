import pytest
from unittest.mock import MagicMock, patch

from app.services.authentication.authentication.auth_service import (
    register_user,
    login_user,
    logout_user
)


# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------

def create_mock_user(
    name="Ankit",
    email="ankit@example.com",
    password="verysecurepassword123",
    role="exporter",
    status="active"
):
    user = MagicMock()

    user.name = name
    user.email = email
    user.password = password
    user.role = role
    user.status = status

    return user


# =========================================================
# REGISTER USER TESTS
# =========================================================

def test_register_user_success():

    user = create_mock_user()

    db = MagicMock()

    # No existing user
    db.query.return_value.filter.return_value.first.return_value = None

    # Mock newly created database user
    created_user = MagicMock()
    created_user.user_id = 1
    created_user.name = user.name
    created_user.email = user.email
    created_user.role = user.role
    created_user.status = user.status

    with patch(
        "app.services.authentication.authentication.auth_service.hash_password",
        return_value="hashed_password"
    ):

        result = register_user(user, db)

    # User should be added to database
    db.add.assert_called_once()

    # Transaction should be committed
    db.commit.assert_called_once()

    # SQLAlchemy refresh should happen
    db.refresh.assert_called_once()

    # Returned object should exist
    assert result is not None


def test_register_user_invalid_role():

    user = create_mock_user(role="admin")

    db = MagicMock()

    with pytest.raises(ValueError, match="Invalid role"):
        register_user(user, db)

    # Database should never be touched
    db.query.assert_not_called()
    db.add.assert_not_called()
    db.commit.assert_not_called()


def test_register_user_duplicate_email():

    user = create_mock_user()

    db = MagicMock()

    # Simulate existing user
    existing_user = MagicMock()

    db.query.return_value.filter.return_value.first.return_value = existing_user

    with pytest.raises(
        ValueError,
        match="Email already registered"
    ):
        register_user(user, db)

    # New user must not be created
    db.add.assert_not_called()

    # Database must not be committed
    db.commit.assert_not_called()


def test_register_user_password_is_hashed():

    user = create_mock_user()

    db = MagicMock()

    db.query.return_value.filter.return_value.first.return_value = None

    with patch(
        "app.services.authentication.authentication.auth_service.hash_password",
        return_value="hashed_password"
    ) as mock_hash:

        register_user(user, db)

    # Verify hash_password was called
    mock_hash.assert_called_once_with(user.password)

    # Get object passed to db.add()
    added_user = db.add.call_args[0][0]

    # Plain password should NOT be stored
    assert added_user.password_hash == "hashed_password"


# =========================================================
# LOGIN USER TESTS
# =========================================================

def test_login_user_success():

    user = create_mock_user()

    db = MagicMock()

    existing_user = MagicMock()

    existing_user.user_id = 1
    existing_user.name = "Ankit"
    existing_user.email = user.email
    existing_user.password_hash = "hashed_password"

    db.query.return_value.filter.return_value.first.return_value = existing_user

    with patch(
        "app.services.authentication.authentication.auth_service.verify_password",
        return_value=True
    ) as mock_verify:

        with patch(
            "app.services.authentication.authentication.auth_service.create_access_token",
            return_value="fake_access_token"
        ) as mock_token:

            returned_user, access_token = login_user(user, db)

    assert returned_user == existing_user
    assert access_token == "fake_access_token"

    mock_verify.assert_called_once_with(
        user.password,
        existing_user.password_hash
    )

    mock_token.assert_called_once_with(
        existing_user.user_id
    )


def test_login_user_email_not_found():

    user = create_mock_user()

    db = MagicMock()

    # No user with this email
    db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(
        ValueError,
        match="Invalid email or password"
    ):
        login_user(user, db)


def test_login_user_wrong_password():

    user = create_mock_user()

    db = MagicMock()

    existing_user = MagicMock()

    existing_user.user_id = 1
    existing_user.email = user.email
    existing_user.password_hash = "correct_hashed_password"

    db.query.return_value.filter.return_value.first.return_value = existing_user

    with patch(
        "app.services.authentication.authentication.auth_service.verify_password",
        return_value=False
    ) as mock_verify:

        with pytest.raises(
            ValueError,
            match="Invalid email or password"
        ):
            login_user(user, db)

    mock_verify.assert_called_once_with(
        user.password,
        existing_user.password_hash
    )


# =========================================================
# LOGOUT TESTS
# =========================================================

def test_logout_user():

    result = logout_user()

    assert result == {
        "message": "Logout successful"
    }