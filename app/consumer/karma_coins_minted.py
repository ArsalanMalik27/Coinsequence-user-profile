import asyncio
import json
from typing import Any

import structlog
from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from app.container import Container
from app.domain.student.event.karma_coins_minted import KarmaCoinsMintedData
from app.domain.student.repository.db.profile import UserProfileRepository
from app.domain.student.repository.db.user_karma import UserKarmaRepository
from app.domain.student.usecase.handle_karma_coins_minted_event_usecase import (
    handle_karma_coins_minted_event_usecase,
)
from app.domain.student.usecase.upsert_profile_embeddings import (
    upsert_profile_embedding_usecase,
)
from app.infra.config import settings
from app.shared.domain.repository.vectordb_client import VectorDBClient

logger = structlog.get_logger()


@inject
async def process_karma_coins_minted(
    message: Any,
    student_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
    user_karma_repo: UserKarmaRepository = Depends(
        Provide[Container.user_karma_db_repository]
    ),
    vectordb_client: VectorDBClient = Depends(
        Provide[Container.vectordb_client]
    ),
) -> None:
    print("karma_coins_minted_consumer_custom-logs", "event received")
    message_data = json.loads(message)
    logger.info(f"{settings.SQS.KARMA_COIN_MINTED} Received", data=message_data)
    karma_coins_minted_data = KarmaCoinsMintedData(**message_data["data"])
    await handle_karma_coins_minted_event_usecase(
        karma_coins_minted_data,
        student_profile_repo,
        user_karma_repo
    )

    await upsert_profile_embedding_usecase(
        karma_coins_minted_data.id,
        student_profile_repo,
        vectordb_client,
    )


async def start_consumer() -> None:
    container = Container()
    container.wire(modules=[__name__])
    event_client = container.event_client()
    print("karma_coins_minted_consumer_custom-logs", "listening consumer...")
    await event_client.listen(
        queue_name=settings.SQS.KARMA_COIN_MINTED, callback=process_karma_coins_minted
    )


if __name__ == "__main__":
    try:
        print("karma_coins_minted_consumer_custom-logs", "Starting consumer...")
        asyncio.run(start_consumer())
    except KeyboardInterrupt as e:
        print(e)
