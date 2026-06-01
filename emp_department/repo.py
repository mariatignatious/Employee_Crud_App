from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.emp_department import EmployeeDepartment


async def get_emp_dept(
    emp_id: int, dept_id: int, db: AsyncSession
) -> EmployeeDepartment:
    stmt = select(EmployeeDepartment).where(
        EmployeeDepartment.employee_id == emp_id,
        EmployeeDepartment.department_id == dept_id,
        EmployeeDepartment.deleted_at.is_(None),
    )
    result = await db.scalar(stmt)
    emp = result
    return emp


async def attach(emp_id: int, dept_id: int, db: AsyncSession) -> EmployeeDepartment:
    emp = EmployeeDepartment(employee_id=emp_id, department_id=dept_id)
    db.add(emp)
    await db.commit()
    await db.refresh(emp)
    return emp


async def detatch(emp: EmployeeDepartment, db: AsyncSession) -> EmployeeDepartment:
    emp.deleted_at = func.now()
    db.add(emp)
    await db.commit()
    await db.refresh(emp)
    return emp
