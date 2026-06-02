from models.entity import Entity
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.employee import Employee
    from models.department import Department


class EmployeeDepartment(Entity):
    __abstract__ = False
    __tablename__ = "employee_department"

    employee_id: Mapped[int] = mapped_column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    department_id: Mapped[int] = mapped_column(Integer, ForeignKey("department.id"), nullable=False, index=True)

    employee: Mapped["Employee"] = relationship(
        "Employee",
        back_populates="employee_departments",
    )

    department: Mapped["Department"] = relationship(
        "Department",
        back_populates="employee_departments",
    )

