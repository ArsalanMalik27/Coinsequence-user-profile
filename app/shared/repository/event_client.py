import json
from typing import Awaitable, Callable

import botocore
import structlog
from aiobotocore.session import get_session

from app.infra.config import settings
from app.shared.domain.event.domain_event import DomainEvent

logger = structlog.getLogger()


class EventClient(object):
    async def publish(self, topic_name: str, data: DomainEvent) -> None:
        session = get_session()
        config = {
            "region_name": settings.AWS_REGION,
            "aws_access_key_id": settings.AWS_ACCESS_KEY,
            "aws_secret_access_key": settings.AWS_SECRET,
        }
        if settings.ENV == "local":
            config["endpoint_url"] = settings.AWS_SNS_SQS_HOST
        SNSClient = session.create_client("sns", **config)
        async with SNSClient as sns_client:
            try:
                await sns_client.publish(
                    TopicArn=self._create_topic_arn(topic_name),
                    Message=json.dumps({"default": data.json()}),
                    MessageStructure="json",
                )
                logger.info(f"Published messages to {topic_name}...", data=data)
            except botocore.exceptions.ClientError as err:
                logger.error(
                    "Failed to publish message to SNS",
                    data=err,
                )
                return

    def _create_topic_arn(self, topic_name: str) -> str:
        return (
            f"arn:aws:sns:{settings.AWS_REGION}:{settings.AWS_ACCOUNT_ID}:{topic_name}"
        )

    async def listen(
        self,
        queue_name: str,
        callback: Callable[[object], Awaitable[None]],
    ) -> None:
        session = get_session()
        config = {
            "region_name": settings.AWS_REGION,
            "aws_access_key_id": settings.AWS_ACCESS_KEY,
            "aws_secret_access_key": settings.AWS_SECRET,
        }
        if settings.ENV == "local":
            config["endpoint_url"] = settings.AWS_SNS_SQS_HOST
        self.SQSClient = session.create_client("sqs", **config)
        async with self.SQSClient as sqs_client:
            try:
                response = await sqs_client.get_queue_url(QueueName=queue_name)
            except botocore.exceptions.ClientError as err:
                logger.error("Failed to get SQS Queue URL", data=err)
                return
            queue_url = response["QueueUrl"]
            while True:
                msg_response = await sqs_client.receive_message(
                    QueueUrl=queue_url,
                    WaitTimeSeconds=20,
                )
                if "Messages" in msg_response:
                    for message in msg_response["Messages"]:
                        body = json.loads(message["Body"])
                        await callback(body["Message"])
                        await sqs_client.delete_message(
                            QueueUrl=queue_url,
                            ReceiptHandle=message["ReceiptHandle"],
                        )
                else:
                    logger.warn("No messages in queue")
