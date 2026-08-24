from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db

from app.schemas.Authentication.registration_schema import (
    UserCreate,
    UserResponse
)

from app.schemas.Authentication.login_schema import (
    LoginUser,
    LoginResponse
)

from app.schemas.Authentication.logout_schema import LogoutResponse

from app.controllers.Authentication.user_controller import (
    user_registration_service as register_user_controller,
    user_login_service as login_user_controller,
    user_logout_service as logout_user_controller
)

#main code start from here

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=UserResponse)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return register_user_controller(user, db)

@router.post("/login", response_model=LoginResponse)
def login_user(
    user: LoginUser,
    db: Session = Depends(get_db)
):
    return login_user_controller(user, db)

@router.post("/logout", response_model=LogoutResponse)
def logout_user():
    return logout_user_controller()