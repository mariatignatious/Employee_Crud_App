from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends

from auth import service as auth_service
from auth.schemas import TokenResponse
from database import get_db

from fastapi.security import OAuth2PasswordRequestForm

import logging

logger = logging.getLogger(__name__)  # current file name

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(
    form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    token = await auth_service.login(db, form.username, form.password)
    logger.info(f"User {form.username} logged in successfully")  # never log passwords
    return TokenResponse(access_token=token)


# @router.post("/login", response_model=TokenResponse)
# async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
#     token = await auth_service.login(db, body.email, body.password)
#
