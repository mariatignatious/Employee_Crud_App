from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from exceptions import ConflictException
from models.employee import Employee


async def create(
    db: AsyncSession, name: str, email: str, age: int, password: str, role: str
) -> (
    Employee
):  # connects to db, creates an employee and returns the created employee object
    db_employee = Employee(
        name=name, email=email, age=age, password_hash=password, role=role
    )
    db.add(db_employee)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException("Email is already in use")
    await db.refresh(db_employee)
    return db_employee


async def get_all_employees(db: AsyncSession) -> Employee:
    stmt = select(Employee).where(Employee.deleted_at.is_(None))
    result = await db.scalars(stmt)
    return result.all()


async def get_by_name(name: str, db: AsyncSession) -> Employee:
    stmt = select(Employee).where(Employee.name == name, Employee.deleted_at.is_(None))
    result = await db.scalar(stmt)
    return result


async def get_employee_id(id: int, db: AsyncSession) -> Employee:
    stmt = select(Employee).where(Employee.id == id, Employee.deleted_at.is_(None))
    result = await db.scalar(stmt)
    return result


async def update_employee(
    db: AsyncSession, emp_id: int, name: str, email: str, role: str
) -> Employee:
    stmt = select(Employee).where(Employee.id == emp_id, Employee.deleted_at.is_(None))
    result = await db.scalar(stmt)
    result.name = name
    result.email = email
    result.role = role

    try:
        await db.commit()
        await db.refresh(result)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{email.strip()}' is already in use",
        )

    return result


async def delete_employee(id: int, db: AsyncSession) -> Employee:
    stmt = select(Employee).where(Employee.id == id, Employee.deleted_at.is_(None))
    result = await db.scalar(stmt)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id {id} not found",
        )
    result.deleted_at = func.now()
    db.add(result)
    await db.commit()
    return result


async def get_by_email(db: AsyncSession, email: str) -> Employee | None:
    stmt = select(Employee).where(
        Employee.email == email, Employee.deleted_at.is_(None)
    )
    result = await db.scalars(stmt)
    return result.first()
