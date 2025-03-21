from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select
from typing import TypeVar, Generic
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from src.database.dao.models import Base, User, Questionnaire, UserRefreshToken

T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    model: type[T]

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: UUID, session: AsyncSession):
        try:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            return record
        except SQLAlchemyError as e:
            raise e

    @classmethod
    async def find_all(cls, session: AsyncSession, filters: BaseModel | None):
        if filters:
            filter_dict = filters.model_dump(exclude_unset=True)
        else:
            filter_dict = {}
        try:
            query = select(cls.model).filter_by(**filter_dict)
            result = await session.execute(query)
            records = result.scalars().all()
            return records
        except SQLAlchemyError as e:
            raise e

    @classmethod
    async def add(cls, session: AsyncSession, values: BaseModel):
        values_dict = values.model_dump(exclude_unset=True)
        new_instance = cls.model(**values_dict)
        session.add(new_instance)
        try:
            await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    async def delete_one_by_id(cls, data_id: UUID, session: AsyncSession):
        try:
            data = await session.get(cls.model, data_id)
            if data:
                await session.delete(data)
                await session.flush()

            return True
        except SQLAlchemyError as e:
            await session.rollback()
            raise e


class UserDAO(BaseDAO[User]):
    model = User

    @classmethod
    async def get_password_hash_by_nickname(cls, nickname: str, session: AsyncSession) -> str:
        try:
            stmp = sa.select(cls.model.password).filter(cls.model.nickname == nickname)
            result = await session.execute(stmp)
            result = result.scalar_one_or_none()
            return result
        except SQLAlchemyError as e:
            raise e

    @classmethod
    async def get_user_by_nickname(cls, nickname: str, session: AsyncSession) -> User:

        try:
            stmp = sa.select(cls.model).where(cls.model.nickname == nickname)
            result = await session.execute(stmp)
            result = result.scalar_one_or_none()
            return result
        except SQLAlchemyError as e:
            raise e


class QuestionnaireDAO(BaseDAO[Questionnaire]):
    model = Questionnaire


class UserRefreshTokenDAO(BaseDAO[UserRefreshToken]):
    model = UserRefreshToken
