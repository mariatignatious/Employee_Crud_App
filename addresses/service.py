from sqlalchemy.ext.asyncio import AsyncSession
from exceptions import BadRequestException, NotFoundException

from addresses import repo
from models.address import Address
from addresses.schemas import AddressCreate
from services import employee_service


async def create_address(db: AsyncSession, body: AddressCreate, emp_id: int) -> Address:
    if not isinstance(body.city, str) or not body.city.strip():
        raise BadRequestException("city must be a non-empty string")
    if not isinstance(body.line1, str) or not body.line1.strip():
        raise BadRequestException("line1 must be a non-empty string")
    if not isinstance(body.country, str) or not body.country.strip():
        raise BadRequestException("country must be a non-empty string")
    address = await repo.create_address(db, body, emp_id)
    return address


async def get_all_addresses(db: AsyncSession) -> Address:
    result = await repo.get_all_addresses(db)
    return result


async def get_address_id(id: int, db: AsyncSession) -> Address:
    result = await repo.get_address_id(id, db)
    if result is None:
        raise NotFoundException("Address not found")
    return result


async def get_address_by_empid(emp_id: int, db: AsyncSession):
    address = await repo.get_address_by_empid(emp_id, db)
    if address is None:
        raise NotFoundException("Address not found")
    return address


async def update_address(
    emp_id: int, address_id: int, body: AddressCreate, db: AsyncSession
):
    address = await get_address_id(address_id, db)
    address = await repo.update_address(emp_id, address, body, db)
    return address


async def delete_address(address_id: int, db: AsyncSession):
    address = await get_address_id(address_id, db)
    address = await repo.delete_address(address, db)
    return address


async def delete_employee_address(
    emp_id: int, address_id: int, db: AsyncSession
) -> Address:
    emp = await employee_service.get_employee_id(emp_id, db)
    address = await get_address_id(address_id, db)
    if address.employee_id != emp_id:
        raise BadRequestException(
            f"employee {emp_id} does not have address with id {address_id}"
        )
    address = await repo.delete_address(address, db)
    return address
