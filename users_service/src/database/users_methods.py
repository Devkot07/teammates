import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.dao.dao import UserDAO
from src.database.dao.session_maker import connection
from src.models.models import UserModel

logger = logging.getLogger(__name__)


@connection()
async def get_user_by_public_id(session: AsyncSession, public_id: UUID):
    logger.info("Getting user by public ID for user %s", public_id)
    try:
        user = await UserDAO.find_one_or_none_by_id(session=session, data_id=public_id)
        pydantic_user = UserModel.model_validate(user, from_attributes=True)
        logger.info("Done getting user by public ID for user %s", public_id)
        return pydantic_user
    except Exception as e:
        logger.error("Can't get user by public ID for user %s: ", public_id, exc_info=e)
        return None


@connection()
async def get_public_id(auth_id: UUID, session: AsyncSession) -> UUID | None:
    logger.info("Getting public id for %s", auth_id)

    try:
        auth_id = await UserDAO.get_public_id_by_auth_id(auth_id, session=session)
    except Exception as e:
        logger.error("Can't get public_id for user with secret_id %s", auth_id, exc_info=e)
        return None

    if auth_id:
        logger.info("Done getting public id for user %s", auth_id)
        return auth_id

    return None


@connection()
async def get_user_by_nickname(nickname: str, session: AsyncSession) -> UserModel | None:
    logger.info("Getting user by nickname for user %s", nickname)
    try:
        user = await UserDAO.get_user_by_nickname(nickname=nickname, session=session)
        pydantic_user = UserModel.model_validate(user, from_attributes=True)
        logger.info("Done getting user by nickname for user %s", nickname)
        return pydantic_user
    except Exception as e:
        logger.error("Can't get user by nickname for user %s", nickname, exc_info=e)
        return None
