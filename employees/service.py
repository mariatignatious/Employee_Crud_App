from sqlalchemy.ext.asyncio import AsyncSession
from exceptions import BadRequestException, NotFoundException
from employees import repo

from models.employee import Employee, EmployeeRole

from auth.utils import hash_password


async def create(
    db: AsyncSession, name: str, email: str, age: int, password: str, role: EmployeeRole
) -> Employee:  # connects to repository to create an employee and returns the created employee object
    hashed = hash_password(password)
    employee = await repo.create(
        db, name=name, email=email, age=age, password=hashed, role=role
    )
    return employee


async def get_all_employees(db: AsyncSession) -> Employee:
    result = await repo.get_all_employees(db)
    return result


async def get_by_name(name: str, db: AsyncSession) -> Employee:
    result = await repo.get_by_name(name, db)
    return result


async def get_employee_id(id: int, db: AsyncSession) -> Employee:
    result = await repo.get_employee_id(id, db)
    if result is None:
        raise NotFoundException(f"Employee {id} not found")
    return result


async def update_employee(
    id: int, name: str, email: str, role: str, department: str, db: AsyncSession
) -> Employee:
    if not isinstance(name, str) or not name.strip():
        raise BadRequestException("name must be a non-empty string")
    if not isinstance(email, str) or not email.strip():
        raise BadRequestException("email must be a non-empty string")
    employee = await repo.update_employee(
        db,
        id,
        name=name.strip(),
        email=email.strip(),
        role=role.strip(),
        department=department,
    )
    return employee


async def delete_employee(id: int, db: AsyncSession) -> Employee:
    result = await repo.delete_employee(id, db)
    return result
