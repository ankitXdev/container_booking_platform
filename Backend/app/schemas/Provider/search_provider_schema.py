from pydantic import BaseModel, EmailStr

class ProviderSearch(BaseModel):
    business_name:str

class SearchResponse(BaseModel):
    business_name:str
    business_address:str
    contact:str
    email:EmailStr
