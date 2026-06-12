from sqlalchemy.ext.asyncio import AsyncSession
from exceptions import ConflictException, NotFoundException

from emp_department import repo
from models.emp_department import EmployeeDepartment
from employees import service as employee_service
from departments import service as department_service


async def attach(emp_id: int, dept_id: int, db: AsyncSession) -> EmployeeDepartment:
    await employee_service.get_employee_id(emp_id, db)
    await department_service.get_department_id(dept_id, db)
    result = await repo.get_emp_dept(emp_id, dept_id, db)
    if result:
        raise ConflictException("Department already exists.")
    emp_dept = await repo.attach(emp_id, dept_id, db)
    return emp_dept


async def detatch(emp_id: int, dept_id: int, db: AsyncSession) -> EmployeeDepartment:
    emp = await repo.get_emp_dept(emp_id, dept_id, db)
    if not emp:
        raise NotFoundException("Employee not found")
    department = await repo.detatch(emp, db)
    return department
