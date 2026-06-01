from fastapi import HTTPException, status

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


from models.department import Department


async def create_department(
    db: AsyncSession, name: str
) -> (
    Department
):  # connects to db, creates a department and returns the created department object
    db_department = Department(name=name)
    db.add(db_department)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
    await db.refresh(db_department)
    return db_department


async def get_all_departments(db: AsyncSession) -> Department:
    stmt = select(Department).where(Department.deleted_at.is_(None))
    result = await db.scalars(stmt)
    return result.all()


async def get_department_id(id: int, db: AsyncSession) -> Department:
    stmt = select(Department).where(
        Department.id == id, Department.deleted_at.is_(None)
    )
    result = await db.scalar(stmt)
    return result


async def update_department(db: AsyncSession, dept_id: int, name: str) -> Department:
    stmt = select(Department).where(
        Department.id == dept_id, Department.deleted_at.is_(None)
    )
    result = await db.scalar(stmt)
    result.name = name

    try:
        await db.commit()
        await db.refresh(result)
    except IntegrityError:
        await db.rollback()

    return result


async def delete_department(id: int, db: AsyncSession) -> Department:
    stmt = select(Department).where(
        Department.id == id, Department.deleted_at.is_(None)
    )
    result = await db.scalar(stmt)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with id {id} not found",
        )
    result.deleted_at = func.now()
    db.add(result)
    await db.commit()
    return result
