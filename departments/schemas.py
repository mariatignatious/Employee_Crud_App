from pydantic import BaseModel, ConfigDict


class DepartmentCreate(BaseModel):
    name: str


class DepartmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
