from pydantic import BaseModel, EmailStr

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    message: str

