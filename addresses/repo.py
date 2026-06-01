from fastapi import HTTPException

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from addresses.schemas import AddressCreate
from models.address import Address


async def create_address(db: AsyncSession, body: AddressCreate, emp_id: int) -> Address:
    db_address = Address(
        line1=body.line1,
        city=body.city,
        postal_code=body.postal_code,
        country=body.country,
        employee_id=emp_id,
    )
    db.add(db_address)
    try:
        await db.commit()
        await db.refresh(db_address)
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=409, detail=str(e))
    return db_address


async def get_all_addresses(db: AsyncSession) -> Address:
    stmt = select(Address).where(Address.deleted_at.is_(None))
    result = await db.scalars(stmt)
    return result.all()


async def get_address_id(id: int, db: AsyncSession) -> Address:
    stmt = select(Address).where(Address.id == id, Address.deleted_at.is_(None))
    result = await db.scalar(stmt)
    # address = result.first()
    return result


async def get_address_by_empid(emp_id: int, db: AsyncSession):
    stmt = select(Address).where(
        Address.employee_id == emp_id, Address.deleted_at.is_(None)
    )
    result = await db.scalars(stmt)
    address = result.all()
    return address


async def update_address(
    emp_id: int,
    address: Address,
    body: AddressCreate,
    db: AsyncSession,
) -> Address:
    address.city = body.city
    address.country = body.country
    address.employee_id = emp_id
    address.line1 = body.line1
    address.postal_code = body.postal_code
    db.add(address)
    await db.commit()
    await db.refresh(address)
    return address


async def delete_address(address: Address, db: AsyncSession):
    address.deleted_at = func.now()
    db.add(address)
    await db.commit()
    await db.refresh(address)
    return {
        "message": "Department deleted",
    }
