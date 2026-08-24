from pydantic import BaseModel, EmailStr

class ProviderCreate(BaseModel):
    business_name:str
    business_address:str
    contact:str

class ProviderResponse(BaseModel):
    message:str
    status:str
    
