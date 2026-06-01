from datetime import datetime
from models.entity import Entity

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.emp_department import EmployeeDepartment


def _datetime_to_iso(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat()


class Department(Entity):
    __abstract__ = False
    __tablename__ = "department"

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    employees: Mapped[list["Employee"]] = relationship(
    "Employee",
    secondary="employee_department",
    back_populates="departments"
    )

    employee_departments: Mapped[list["EmployeeDepartment"]] = relationship(
    "EmployeeDepartment",
    back_populates="department"
    )
