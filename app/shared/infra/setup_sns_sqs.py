import asyncio

import structlog
from aiobotocore.session import get_session
from dotenv import dotenv_values

config = dotenv_values(".env") or {}

AWS_REGION = config.get("AWS_REGION")
AWS_ACCESS_KEY = config.get("AWS_ACCESS_KEY")
AWS_SECRET = config.get("AWS_SECRET")
SNS_SQS_HOST = config.get("AWS_SNS_SQS_HOST")

logger = structlog.getLogger()

TOPIC_QUEUE_MAPPING = []
mappings = (config.get("SNS_SQS_MAPPING") or "").split(",")
for mapping in mappings:
    topic_subs_list = mapping.split(":")
    topic, subs = topic_subs_list[0], topic_subs_list[1:]
    TOPIC_QUEUE_MAPPING.append({"topic": topic, "queues": subs})


async def setup() -> None:
    session = get_session()
    SNSClient = session.create_client(
        "sns",
        endpoint_url=SNS_SQS_HOST,
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET,
    )
    SQSClient = session.create_client(
        "sqs",
        endpoint_url=SNS_SQS_HOST,
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET,
    )
    async with SNSClient as sns_client:
        async with SQSClient as sqs_client:
            for item in TOPIC_QUEUE_MAPPING:
                sns_response = await sns_client.create_topic(Name=item.get("topic"))
                topic_arn = sns_response.get("TopicArn")
                logger.info(f"Created topic: {topic_arn}")
                for queue in item.get("queues") or []:
                    response = await sqs_client.create_queue(QueueName=queue)
                    queue_url = response.get("QueueUrl")
                    await sns_client.subscribe(
                        TopicArn=topic_arn,
                        Protocol="sqs",
                        Endpoint=queue_url,
                    )
                    logger.info(f"Subscription created: {queue_url}")


if __name__ == "__main__":
    asyncio.run(setup())
