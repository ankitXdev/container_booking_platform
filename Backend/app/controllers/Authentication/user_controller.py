from sqlalchemy.orm import Session

from app.schemas.Authentication.registration_schema import UserCreate
from app.schemas.Authentication.login_schema import LoginUser

from app.services.authentication.authentication.auth_service import (
    register_user as register_user_service,
    login_user as login_user_service
)


def user_registration_service(user: UserCreate, db: Session):

    return register_user_service(user, db)


def user_login_service(user: LoginUser, db: Session):
    existing_user, access_token = login_user_service(user, db)

    return {
        "message": "Login successful",
        "name": existing_user.name,
        "access_token": access_token,
        "token_type": "bearer"
    }

def user_logout_service():
    return{
        "message" : "Logout successful"
    }