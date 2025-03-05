from uuid import UUID

import structlog

from app.api.api_v1.student.dto.score import UpdateScoreDTO
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.data.score import CreateScoreProps, Score
from app.domain.student.data.test import TestProps
from app.domain.student.repository.db.score import ScoreRepository
from app.domain.student.repository.db.test import TestRepository
from app.shared.utils.error import DomainError
from app.masterdata_shared.domain.client import MasterdataClient

logger = structlog.get_logger()


async def create_update_test_score_usecase(
    userprofile: UserProfileProps,
    test_id: UUID,
    update_score_dto_list: list[UpdateScoreDTO],
    test_repo: TestRepository,
    score_repo: ScoreRepository,
    masterdata_client: MasterdataClient,

) -> TestProps:
    test_props = await test_repo.get_by_test_id(test_id)
    if not test_props or test_props.profile_id != userprofile.id:
        logger.info(
            "[CreateUpdateTestScoreUsecase: attempt to update test score that is not owned]",
            data=userprofile,
        )
        raise DomainError("Invalid Test Id")

    masterdata_test_props = await masterdata_client.get_test(test_props.test_id)

    if not masterdata_test_props:
        raise DomainError("Invalid Master Data Test")

    for update_score_dto in update_score_dto_list:
        if (int(masterdata_test_props.min) > int(update_score_dto.score) or int(
                update_score_dto.score) > int(masterdata_test_props.max)) or int(
            update_score_dto.score) % int(masterdata_test_props.step) != 0:
            raise DomainError("Invalid Score")

        if not update_score_dto.id:
            score_props = CreateScoreProps(**update_score_dto.dict(exclude={'id','deleted'}))
            score = Score.create_from(props=score_props, profile_id=userprofile.id, test_id=test_id)
            await score_repo.create(score.props)
        else:
            existing_score = await score_repo.get_by_id(update_score_dto.id)
            if not existing_score or existing_score.profile_id != userprofile.id:
                logger.info(
                    "[UpdateScoreUsecase: attempt to update non-existing Score]",
                    data=update_score_dto,
                )
                raise DomainError("Invalid Score")

            score_updated_props = CreateScoreProps(**update_score_dto.dict(exclude={'id','deleted'}))
            score = Score(props=existing_score)
            score.update_from(score_updated_props, test_id)
            if update_score_dto.deleted:
                score.delete_score()
            await score_repo.update_score(score.props)
    test_props = await test_repo.get_by_test_id(test_id)
    return test_props
