from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class EmployeeDepartmentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    employee_id: int = Field(gt=0)
    department_id: int = Field(gt=0)


class EmployeeDepartmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    employee_id: int
    department_id: int
    created_at: datetime | None
    deleted_at: datetime | None
