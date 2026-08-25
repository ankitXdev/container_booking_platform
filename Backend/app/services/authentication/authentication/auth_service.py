from sqlalchemy.orm import Session

from app.models.user_model import users

from app.utils.password import hash_password, verify_password

from app.security.jwt import create_access_token


def register_user(user, db: Session):

    # Business rule
    if user.role not in ["exporter", "provider"]:
        raise ValueError("Invalid role")

    # Check if email already exists
    existing_user = (
        db.query(users)
        .filter(users.email == user.email)
        .first()
    )

    if existing_user:
        raise ValueError("Email already registered")

    # Hash password
    hashed_password = hash_password(user.password)

    # Create user
    new_user = users(
        name=user.name,
        email=user.email,
        password_hash=hashed_password,
        role=user.role,
        status=user.status
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(user, db: Session):

    existing_user = (
        db.query(users)
        .filter(users.email == user.email)
        .first()
    )

    if existing_user is None:
        raise ValueError("Invalid email or password")

    if not verify_password(
        user.password,
        existing_user.password_hash
    ):
        raise ValueError("Invalid email or password")

    access_token = create_access_token(existing_user.user_id)

    return existing_user, access_token


def logout_user():

    return {
        "message": "Logout successful"
    }