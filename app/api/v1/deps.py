from typing import Generator
from fastapi import UploadFile
from app.db.session import SessionLocal
from app.core.config import settings
from azure.storage.blob.aio import BlobServiceClient
from azure.storage.blob import ContentSettings

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
        
    async def upload_file(self, filename: str ,file_in: UploadFile):
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
    
        async with blob_service_client:
            container_client = blob_service_client.get_container_client(self.container_name)
            await container_client.upload_blob(
                name=filename,
                data=file_in.file,
                content_settings=ContentSettings(content_type=file_in.content_type)
            )
