"""
Employee entity — ORM mapped class for table `employees`.
"""

from datetime import datetime
from typing import Any

from models.entity import Entity

from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.emp_department import EmployeeDepartment

import enum

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.address import Address
    from models.department import Department


def _datetime_to_iso(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat()


class EmployeeRole(str, enum.Enum):
    UI = "UI"
    UX = "UX"
    DEVELOPER = "Developer"
    HR = "HR"


class Employee(Entity):
    __abstract__ = False
    __tablename__ = "employees"  # name of the table in the database

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    addresses: Mapped[list["Address"]] = (
        relationship(  # no need to import if imported it will cause error
            "Address",
            back_populates="employee",
        )
    )

    departments: Mapped[list["Department"]] = relationship(
        "Department",
        secondary=EmployeeDepartment.__table__,
        back_populates="employees",
        viewonly=True,
    )

    role: Mapped[EmployeeRole] = mapped_column(
        Enum(
            EmployeeRole,
            name="employeerole",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
        server_default=EmployeeRole.DEVELOPER.value,
    )

    employee_departments: Mapped[list["EmployeeDepartment"]] = relationship(
        "EmployeeDepartment", back_populates="employee"
    )

    # added these in entity
    # created_at: Mapped[datetime] = mapped_column( #created_at is a datetime column with timezone information, server_default func.now() to automatically set the current timestamp when a new employee is created, nullable false to prevent null values
    #     DateTime(timezone=True),
    #     server_default=func.now(),
    #     nullable=False,
    # )
    # updated_at: Mapped[Optional[datetime]] = mapped_column( #updated_at is a datetime column with timezone information, server_default func.now() to automatically set the current timestamp when a new employee is created, onupdate func.now() to automatically update the timestamp when an employee is updated, nullable true to allow null values for employees that have not been updated yet
    #     DateTime(timezone=True),
    #     server_default=func.now(),
    #     onupdate=func.now(),
    #     nullable=True,
    # )
    # deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True) #deleted_at is a datetime column with timezone information, nullable true to allow null values for employees that have not been deleted yet

    def to_api_dict(
        self,
    ) -> dict[
        str, Any
    ]:  # to_api_dict method to convert the Employee object to a JSON-friendly dictionary, using ISO 8601 format for the datetime fields
        """JSON-friendly representation (ISO 8601 for timestamps)."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": _datetime_to_iso(self.created_at),
            "updated_at": _datetime_to_iso(self.updated_at),
            "deleted_at": _datetime_to_iso(self.deleted_at),
        }
