from pydantic import BaseModel, EmailStr

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    message: str
    name:str
    access_token: str
    token_type: str

