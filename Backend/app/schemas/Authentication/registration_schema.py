from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=16)
    role: str
    status: str

class UserResponse(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    role: str
    status: str


