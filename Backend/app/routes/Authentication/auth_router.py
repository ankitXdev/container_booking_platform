from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.controllers.user_controller import create_user

router = APIRouter(prefix='/auth', tags=['Authentication'])

@router.post('/register', response_model=UserResponse)
def register_user(
    user:UserCreate,
    db: Session=Depends(get_db)
):
    return create_user(user,db)
