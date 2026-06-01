from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.entity import Entity


class EmployeeDepartment(Entity):
    __abstract__ = False
    __tablename__ = "employee_department"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    employee_id: Mapped[int] = mapped_column(
        ForeignKey(
            "employees.id", ondelete="CASCADE"
        ),  # cascade: If the parent row is deleted, automatically delete the related child rows.
        primary_key=True,
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("department.id", ondelete="CASCADE"), primary_key=True
    )

    employee: Mapped["Employee"] = relationship(
        "Employee",
        back_populates="employee_departments"
    )

    department: Mapped["Department"] = relationship(
        "Department",
        back_populates="employee_departments"
    )


# from sqlalchemy import Table, Column, ForeignKey
# from sqlalchemy.orm import relationship, Mapped, mapped_column

# from models.entity import Entity

# employee_department = Table(
#     "employee_department",
#     Entity.metadata,   # or Base.metadata
#     employee_id = mapped_column(ForeignKey("employees.id")),
#     department_id = mapped_column(ForeignKey("department.id"))
# )

# """
# employee_department = Table(
#     "employee_department",
#     Entity.metadata,

#     Column(
#         "employee_id",
#         ForeignKey("employees.id"),
#         primary_key=True,
#     ),

#     Column(
#         "department_id",
#         ForeignKey("department.id"),
#         primary_key=True,
#     ),
# )
# """
