import asyncio

import structlog
from aiobotocore.session import get_session
from dotenv import dotenv_values

config = dotenv_values(".env") or {}

AWS_REGION = config.get("AWS_REGION")
AWS_ACCESS_KEY = config.get("AWS_ACCESS_KEY")
AWS_SECRET = config.get("AWS_SECRET")
S3_MEDIA_BUCKET = config.get("S3_MEDIA_BUCKET", "bucket")
S3_HOST = config.get("AWS_SNS_SQS_HOST")

logger = structlog.getLogger()


async def setup() -> None:
    session = get_session()
    S3_CLIENT = session.create_client(
        "s3",
        endpoint_url=S3_HOST,
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET,
    )
    async with S3_CLIENT as s3_client:
        response = await s3_client.create_bucket(Bucket=S3_MEDIA_BUCKET)
        logger.info(f"S3 bucket created: {response}")


if __name__ == "__main__":
    asyncio.run(setup())
