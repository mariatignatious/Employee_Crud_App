from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db

from emp_department import service
from emp_department.schemas import EmployeeDepartmentResponse

from auth.dependencies import get_current_user

router = APIRouter(
    prefix="/employee_department",
    tags=["Employee_Department"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "/{emp_id}/departments/{dept_id}",
    response_model=EmployeeDepartmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def attach(emp_id: int, dept_id: int, db: AsyncSession = Depends(get_db)):
    emp_dept = await service.attach(emp_id, dept_id, db)
    return emp_dept


@router.delete(
    "/{emp_id}/departments/{dept_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def detatch(emp_id: int, dept_id: int, db: AsyncSession = Depends(get_db)):
    emp_dept = await service.detatch(emp_id, dept_id, db)
    return {"message": "Department is detatched"}
