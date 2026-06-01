from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from services import employee_service


router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("", status_code=status.HTTP_201_CREATED, tags=["Employees"])
async def create_employee(
    body: dict = Body(...), db: AsyncSession = Depends(get_db)
):  # endpoint to create an employee, it takes a JSON body with name and email, validates the input and then calls the employee_service to create the employee in the database, and returns the created employee as a dictionary
    name = body.get("name")
    email = body.get("email")
    employee = await employee_service.create(db, name, email)
    return employee.to_api_dict()


@router.get("")
async def get_all_employees(db: AsyncSession = Depends(get_db)):
    result = await employee_service.get_all_employees(db)
    print(result)
    return [r.to_api_dict() for r in result]


@router.get("/{id}")
async def get_employee_id(id: int, db: AsyncSession = Depends(get_db)):
    result = await employee_service.get_employee_id(id, db)
    return result.to_api_dict()


@router.patch("/{id}")
async def update_employee(
    emp_id: int, body: dict = Body(...), db: AsyncSession = Depends(get_db)
):
    name = body.get("name")
    email = body.get("email")
    result = await employee_service.update_employee(emp_id, name, email, db)
    return result.to_api_dict()


@router.delete("/{id}")
async def delete_employee(emp_id: int, db: AsyncSession = Depends(get_db)):
    result = await employee_service.delete_employee(id, db)
    return result.to_api_dict()
