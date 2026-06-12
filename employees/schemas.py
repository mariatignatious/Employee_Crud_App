from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, EmailStr
from addresses.schemas import AddressCreate, AddressResponse
from departments.schemas import DepartmentCreate
from models.employee import EmployeeRole, EmployeeStatus, EmployeeStatus


class EmployeeCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    name: str = Field(min_length=1)
    email: EmailStr
    age: int | None = Field(ge=0, le=150)
    address: AddressCreate | None = None
    department: DepartmentCreate | None = None
    password: str = Field(min_length=6)
    role: EmployeeRole = EmployeeRole.DEVELOPER
    status: EmployeeStatus = EmployeeStatus.ACTIVE
    experience: int = 1


class EmployeeResponse(BaseModel):  # how the output should look like
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    age: int | None
    role: str
    status: EmployeeStatus
    experience: int
    addresses: list[AddressResponse] | None = None
    created_at: datetime


class GetbyidResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    age: int | None
    role: str
    created_at: datetime
    updated_at: datetime
    status: EmployeeStatus
    experience: int
    addresses: list[AddressResponse] | None = None


class UpdateCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    name: str = Field(min_length=1)
    email: str
    age: int | None = Field(default=None, ge=0, le=150)
    password: str | None = Field(default=None, min_length=6)
    role: EmployeeRole | None = None
    status: EmployeeStatus | None = None
    experience: int | None = None
    department: DepartmentCreate | None = None
    address: AddressCreate | None = None

class UpdateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    email: str
    age: int | None
    role: str
    experience: int
    address: AddressResponse | None = None
    department: DepartmentCreate | None = None
    created_at: datetime
    updated_at: datetime
