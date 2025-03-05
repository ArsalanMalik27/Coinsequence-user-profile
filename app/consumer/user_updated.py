import asyncio
import json
from typing import Any

import structlog
from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from app.container import Container
from app.domain.student.event.user_updated import UserUpdatedData
from app.domain.student.repository.db.profile import UserProfileRepository
from app.domain.student.usecase.update_profile_on_user_updated_event import (
    update_profile_on_user_updated_event_usecase,
)
from app.infra.config import settings
from app.shared.domain.repository.event_client import EventClient

logger = structlog.get_logger()


@inject
async def process_user_updated(
    message: Any,
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
    event_client: EventClient = Depends(Provide[Container.event_client]),
) -> None:
    message_data = json.loads(message)
    logger.info(f"{settings.SQS.USER_UPDATED} Received", data=message_data)
    user_updated_data = UserUpdatedData(**message_data["data"])
    await update_profile_on_user_updated_event_usecase(
        user_updated_data, user_profile_repo, event_client
    )
    # TODO: UserUpdated event from Accounts service & call `update_profile_usecase` to update Profile in DB and it will raise an event ProfileUpdated
    # which will be listened in KarmaPost


async def start_consumer() -> None:
    container = Container()
    container.wire(modules=[__name__])
    event_client = container.event_client()
    await event_client.listen(
        queue_name=settings.SQS.USER_UPDATED, callback=process_user_updated
    )


if __name__ == "__main__":
    try:
        asyncio.run(start_consumer())
    except KeyboardInterrupt as e:
        print(e)
