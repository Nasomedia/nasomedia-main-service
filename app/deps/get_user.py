from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app import schemas

import aiohttp

resuable_oauth2 = OAuth2PasswordBearer(
    tokenUrl = settings.TOKEN_URL
)


async def get_current_user(
    token: str = Depends(resuable_oauth2)
) -> schemas.User:
    headers={"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f"{settings.IDENTITY_SERVICE_BASE_URL}/v1/users/me") as resp:
            if resp.status != 200:
                raise HTTPException(status_code=resp.status, detail=await resp.text())
            user_data = await resp.json()
            user = schemas.User(**user_data)
            return user

async def get_current_active_user(
    current_user: schemas.User = Depends(get_current_user)
) -> schemas.User:
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return current_user

async def get_current_active_superuser(
    current_user: schemas.User = Depends(get_current_user)
) -> schemas:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    return current_user