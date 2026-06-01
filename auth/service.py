from auth.utils import create_access_token, verify_password
from exceptions import UnauthorizedException
from repository import employee_repo
from sqlalchemy.ext.asyncio import AsyncSession


async def login(db: AsyncSession, email: str, password: str) -> str:
    employee = await employee_repo.get_by_email(db, email)
    if employee is None:
        raise UnauthorizedException("Invalid email or password")

    if not verify_password(password, employee.password_hash):
        raise UnauthorizedException("Invalid email or password")

    return create_access_token(
        {"id": employee.id, "email": employee.email, "role": employee.role.value}
    )
