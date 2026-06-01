from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import get_current_user
from database.connection import get_db

from addresses import service
from addresses.schemas import AddressCreate, AddressResponse


router = APIRouter(
    prefix="/addresses", tags=["Addresses"], dependencies=[Depends(get_current_user)]
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    tags=["Addresses"],
    response_model=AddressResponse,
)
async def create_address(
    emp_id: int, body: AddressCreate, db: AsyncSession = Depends(get_db)
):
    address = await service.create_address(db, body, emp_id)
    return address


@router.get("", response_model=list[AddressResponse])
async def get_all_addresses(db: AsyncSession = Depends(get_db)):
    result = await service.get_all_addresses(db)
    return [addr for addr in result]


@router.get("/{id}", response_model=AddressResponse)
async def get_address_id(id: int, db: AsyncSession = Depends(get_db)):
    result = await service.get_address_id(id, db)
    return result


@router.get("/employee/{emp_id}", response_model=list[AddressResponse])
async def get_address_by_empid(emp_id: int, db: AsyncSession = Depends(get_db)):
    address = await service.get_address_by_empid(emp_id, db)
    return address


@router.put("/{emp_id}/{id}", response_model=AddressResponse)
async def update_address(
    emp_id: int, id: int, body: AddressCreate, db: AsyncSession = Depends(get_db)
):
    address = await service.update_address(emp_id, id, body, db)
    return address


@router.delete("/{id}")
async def delete_address(id: int, db: AsyncSession = Depends(get_db)):
    result = await service.delete_address(id, db)
    return {
        "message": "Address deleted",
    }


@router.delete(
    "/employee/{emp_id}/address/{address_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_employee_address(
    emp_id: int, address_id: int, db: AsyncSession = Depends(get_db)
):
    address = await service.delete_employee_address(emp_id, address_id, db)
    return {"message": f"Address with id {address_id} of employee {emp_id} is deleted"}
