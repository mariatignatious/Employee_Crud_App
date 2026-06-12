from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db
from employees import service
from models.employee import EmployeeRole
from employees.schemas import (
    EmployeeCreate,
    EmployeeResponse,
    GetbyidResponse,
    UpdateResponse,
    UpdateCreate,
)
from addresses import router as address_router
from departments import router as department_router
from emp_department import router as emp_dept_router
from auth.dependencies import get_current_user, require_role
from auth.schemas import TokenPayload

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    tags=["Employees"],
    response_model=EmployeeResponse,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def create_employee(body: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    employee = await service.create(
        db,
        body.name,
        body.email,
        body.age,
        body.password,
        body.role,
        body.status,
        body.experience,
    )
    address = await address_router.create_address(employee.id, body.address, db)
    dept = await department_router.create_department(body.department, db)
    emp_dept = await emp_dept_router.attach(employee.id, dept.id, db)
    return employee


@router.get("", response_model=list[EmployeeResponse])
async def get_all_employees(
    status: str | None = None,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    result = await service.get_all_employees(db, status)
    return result


@router.get("/search")
async def get_by_name(
    name: str,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    result = await service.get_by_name(name, db)
    print(result)
    return result


@router.get("/{id}", response_model=GetbyidResponse)
async def get_employee_id(
    id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    result = await service.get_employee_id(id, db)
    return result


@router.put(
    "/{id}",
    # response_model=UpdateResponse,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def update_employee(
    id: int, body: UpdateCreate, db: AsyncSession = Depends(get_db)
):
    # Get only the fields that were explicitly set in the request
    update_data = body.model_dump(exclude_unset=True)
    
    result = await service.update_employee(
        id=id,
        update_data=update_data,
        db=db,
    )
    return result


@router.delete("/{id}", dependencies=[Depends(require_role(EmployeeRole.HR))])
async def delete_employee(id: int, db: AsyncSession = Depends(get_db)):
    result = await service.delete_employee(id, db)
    return {
        "message": f"Employee {id} deleted",
    }
