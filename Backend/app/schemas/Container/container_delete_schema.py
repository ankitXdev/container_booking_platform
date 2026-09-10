from pydantic import BaseModel


class ContainerDeleteResponse(BaseModel):
    message: str
