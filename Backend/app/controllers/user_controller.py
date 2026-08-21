from sqlalchemy.orm import Session

from app.models.user_model import users
from app.schemas.user_schema import UserCreate

def create_user(user:UserCreate, db:Session):
   new_user = users(
        name = user.name,
        email = user.email,
        password = user.password,
        role = user.role,
        status = user.status
    )
   db.add(new_user)
   db.commit()
   db.refresh(new_user)

   return new_user