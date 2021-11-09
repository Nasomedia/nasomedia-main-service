from typing import Generator
from fastapi import UploadFile, Depends, params
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.db.session import SessionLocal
from app.core.config import settings
from app import schemas

from azure.storage.blob.aio import BlobServiceClient
from azure.storage.blob import ContentSettings

import aiohttp

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class AzureBlobService():
    connection_string = settings.AZURE_STORAGE_CONNECTION_STRING
    container_name = settings.AZURE_STORAGE_CONTAINER_NAME
    blob_url = settings.BLOB_URL

    async def upload_file(self, filename: str, file_in: UploadFile):
        blob_service_client = BlobServiceClient.from_connection_string(
            self.connection_string)

        async with blob_service_client:
            container_client = blob_service_client.get_container_client(
                self.container_name)
            await container_client.upload_blob(
                name=filename,
                data=file_in.file,
                content_settings=ContentSettings(
                    content_type=file_in.content_type)
            )

resuable_oauth2 = OAuth2PasswordBearer(
    tokenUrl = settings.IDENTITY_SERVICE_BASE_URL+settings.TOKEN_URL
)

async def get_current_user(
    token: str = Depends(resuable_oauth2)
) -> schemas.User:
    headers={"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f"{settings.IDENTITY_SERVICE_BASE_URL}/api/v1/users/me") as resp:
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