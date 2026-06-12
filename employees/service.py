from sqlalchemy.ext.asyncio import AsyncSession
from exceptions import BadRequestException, NotFoundException
from employees import repo

from models.employee import Employee, EmployeeRole

from auth.utils import hash_password


async def create(
    db: AsyncSession,
    name: str,
    email: str,
    age: int,
    password: str,
    role: EmployeeRole,
    status: EmployeeStatus,
    experience: int = 1,
) -> Employee:
    hashed = hash_password(password)
    employee = await repo.create(
        db,
        name=name,
        email=email,
        age=age,
        password=hashed,
        role=role,
        status=status,
        experience=experience,
    )
    return employee


async def get_all_employees(db: AsyncSession, status: str | None = None) -> Employee:
    result = await repo.get_all_employees(db, status)
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
    id: int,
    update_data: dict,
    db: AsyncSession,
) -> Employee:
    # Validate required fields
    if "name" in update_data:
        name = update_data["name"]
        if not isinstance(name, str) or not name.strip():
            raise BadRequestException("name must be a non-empty string")
        update_data["name"] = name.strip()
    
    if "email" in update_data:
        email = update_data["email"]
        if not isinstance(email, str) or not email.strip():
            raise BadRequestException("email must be a non-empty string")
        update_data["email"] = email.strip()
    
    # Hash password if provided
    if "password" in update_data and update_data["password"]:
        update_data["password"] = hash_password(update_data["password"])
    
    # Strip role if provided
    if "role" in update_data and update_data["role"]:
        update_data["role"] = update_data["role"].value if hasattr(update_data["role"], 'value') else str(update_data["role"])
    
    # Handle status enum
    if "status" in update_data and update_data["status"]:
        update_data["status"] = update_data["status"].value if hasattr(update_data["status"], 'value') else str(update_data["status"])
    
    employee = await repo.update_employee(db, id, **update_data)
    return employee


async def delete_employee(id: int, db: AsyncSession) -> Employee:
    result = await repo.delete_employee(id, db)
    return result
