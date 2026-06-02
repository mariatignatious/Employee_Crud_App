from auth.utils import (
    create_access_token,
    verify_password,
    create_refresh_token,
    decode_access_token,
)
from exceptions import UnauthorizedException
from employees import repo
from sqlalchemy.ext.asyncio import AsyncSession


async def login(db: AsyncSession, email: str, password: str):
    employee = await repo.get_by_email(db, email)
    if employee is None:
        raise UnauthorizedException("invalid email or password")
    if not verify_password(password, employee.password_hash):
        raise UnauthorizedException("invalid email or password")

    access_token = create_access_token(
        {"id": employee.id, "email": employee.email, "role": employee.role.value}
    )
    refresh_token = create_refresh_token(
        {"id": employee.id, "email": employee.email, "role": employee.role.value}
    )
    return {"access_token": access_token, "refresh_token": refresh_token}


async def refresh(refresh_token: str):
    token = decode_access_token(refresh_token)
    if token is None:
        raise UnauthorizedException("invalid refresh token")
    if token.get("type") != "refresh":
        raise UnauthorizedException("invalid refreh token")
    access_token = create_access_token({"id": token["id"], "email": token["email"]})
    return access_token
