import structlog

from app.domain.student.data.profile import UserProfile
from app.domain.student.data.user_karma import UserKarma
from app.domain.student.event.karma_coins_minted import KarmaCoinsMintedData
from app.domain.student.repository.db.profile import UserProfileRepository
from app.domain.student.repository.db.user_karma import UserKarmaRepository

logger = structlog.get_logger()


async def handle_karma_coins_minted_event_usecase(
    karma_coins_minted_data: KarmaCoinsMintedData,
    user_profile_repo: UserProfileRepository,
    user_karma_repo: UserKarmaRepository,
):
    existing_user_profile = await user_profile_repo.get_by_user_id(karma_coins_minted_data.id)
   
    if not existing_user_profile:
        logger.info("[UpdateProfileOnKarmaCoinsMintedEventUsecase: attempt to update non-existing user profile]")
        return

    user_profile = UserProfile(props=existing_user_profile)
    user_profile.add_karma_coins(karma_coins_minted_data.karma_point)
    await user_profile_repo.update_profile(user_profile.props)

    for user_karma in karma_coins_minted_data.user_karma:
        user_karma_props = await user_karma_repo.get_by_tag_id_and_user_id(karma_coins_minted_data.id, user_karma.tag_id)

        if not user_karma_props:
            props = UserKarma.from_event(karma_coins_minted_data.id, user_karma)
            await user_karma_repo.create_user_karma(props.props)
        else:
            user_karma_domain = UserKarma(props=user_karma_props)
            user_karma_domain.update_from_event(user_karma)
            await user_karma_repo.update_user_karma(user_karma_domain.props)
