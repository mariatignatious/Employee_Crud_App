from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, EmailStr
from addresses.schemas import AddressCreate
from departments.schemas import DepartmentCreate


class EmployeeCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    name: str = Field(min_length=1)
    email: EmailStr
    age: int | None = Field(ge=0, le=150)
    address: AddressCreate | None = None
    department: DepartmentCreate | None = None
    password: str = Field(min_length=6)


class EmployeeResponse(BaseModel):  # how the output should look like
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    age: int | None


class GetbyidResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    age: int | None
    created_at: datetime
    updated_at: datetime
