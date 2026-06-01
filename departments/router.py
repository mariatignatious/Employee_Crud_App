from fastapi import APIRouter, Body, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db

from departments import service
from departments.schemas import DepartmentCreate, DepartmentResponse

from auth.dependencies import get_current_user
# from auth.schemas import TokenPayload

router = APIRouter(
    prefix="/departments",
    tags=["Departments"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    tags=["Departments"],
    response_model=DepartmentResponse,
)
async def create_department(body: DepartmentCreate, db: AsyncSession = Depends(get_db)):
    department = await service.create_department(db, body.name)
    return department


@router.get("", response_model=list[DepartmentResponse])
async def get_all_departments(db: AsyncSession = Depends(get_db)):
    result = await service.get_all_departments(db)
    return result


@router.get("/{id}", response_model=DepartmentResponse)
async def get_department_id(id: int, db: AsyncSession = Depends(get_db)):
    result = await service.get_department_id(id, db)
    return result


@router.patch("/{id}")
async def update_department(
    id: int, body: dict = Body(...), db: AsyncSession = Depends(get_db)
):
    name = body.get("name")
    result = await service.update_department(id, name, db)
    return result


@router.delete("/{id}")
async def delete_department(id: int, db: AsyncSession = Depends(get_db)):
    result = await service.delete_department(id, db)
    return {
        "message": "Department deleted",
    }
