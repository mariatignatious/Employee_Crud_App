from fastapi import APIRouter, Body, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db
from services import employee_service
from models.employee import EmployeeRole
from employees.schemas import EmployeeCreate, EmployeeResponse, GetbyidResponse

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
    employee = await employee_service.create(db, body.name, body.email, body.age, body.password, body.role)
    return employee


@router.get("", response_model=list[EmployeeResponse])
async def get_all_employees(
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    result = await employee_service.get_all_employees(db)
    return result


@router.get("/search")
async def get_by_name(
    name: str,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    result = await employee_service.get_by_name(name, db)
    print(result)
    return result


@router.get("/{id}", response_model=GetbyidResponse)
async def get_employee_id(id: int, db: AsyncSession = Depends(get_db)):
    result = await employee_service.get_employee_id(id, db)
    return result


@router.put("/{id}", dependencies=[Depends(require_role(EmployeeRole.HR))])
async def update_employee(
    emp_id: int, body: dict = Body(...), db: AsyncSession = Depends(get_db)
):
    name = body.get("name")
    email = body.get("email")
    role = body.get("role")
    result = await employee_service.update_employee(emp_id, name, email, role, db)
    return result


@router.delete("/{id}", dependencies=[Depends(require_role(EmployeeRole.HR))])
async def delete_employee(id: int, db: AsyncSession = Depends(get_db)):
    result = await employee_service.delete_employee(id, db)
    return {
        "message": "Employee deleted",
    }
