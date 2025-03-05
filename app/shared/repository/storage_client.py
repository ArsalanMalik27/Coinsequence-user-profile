from uuid import UUID, uuid4

from aiobotocore.session import get_session
from fastapi import UploadFile

from app.infra.config import settings
from app.shared.domain.repository.storage_client import FileInfo


class StorageClient:
    async def upload(
        self, folder: str, actor_uuid: UUID, files: list[UploadFile]
    ) -> list[FileInfo]:
        bucket = settings.S3_MEDIA_BUCKET
        session = get_session()
        config = {
            "region_name": settings.AWS_REGION,
            "aws_access_key_id": settings.AWS_ACCESS_KEY,
            "aws_secret_access_key": settings.AWS_SECRET,
        }
        if settings.ENV == "local":
            config["endpoint_url"] = settings.AWS_SNS_SQS_HOST
        S3_CLIENT = session.create_client("s3", **config)
        async with S3_CLIENT as s3_client:
            files_info: list[FileInfo] = []
            for file in files:
                new_name = uuid4()
                extension = file.filename.split(".")[-1]
                key = f"{folder}/{actor_uuid}/{new_name}.{extension}"
                await s3_client.put_object(Bucket=bucket, Key=key, Body=file.file._file)
                files_info.append(
                    {
                        "url": f"https://{bucket}.s3.{settings.AWS_REGION}.amazonaws.com/{key}",
                        "path": key,
                    }
                )
            return files_info
