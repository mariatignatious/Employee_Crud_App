from sqlalchemy.ext.asyncio import AsyncSession
from exceptions import BadRequestException, NotFoundException

from departments import repo
from models.department import Department


async def create_department(
    db: AsyncSession, name: str
) -> Department:  # connects to repository to create a department and returns the created department object
    department = await repo.create_department(db, name=name)
    return department


async def get_all_departments(db: AsyncSession) -> Department:
    result = await repo.get_all_departments(db)
    return result


async def get_department_id(id: int, db: AsyncSession) -> Department:
    result = await repo.get_department_id(id, db)
    if result is None:
        raise NotFoundException(f"Department {id} not found")
    return result


async def update_department(id: int, name: str, db: AsyncSession) -> Department:
    if not isinstance(name, str) or not name.strip():
        raise BadRequestException("name must be a non-empty string")
    department = await repo.update_department(db, id, name=name.strip())
    return department


async def delete_department(id: int, db: AsyncSession) -> Department:
    result = await repo.delete_department(id, db)
    return result
