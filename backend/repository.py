from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload

from database import new_session, StreamOrm, UserOrm
from schemas import StreamCreate, SStream, UserCreate, User


class StreamRepository:
    @staticmethod
    async def create_stream(data: StreamCreate, owner_id: int) -> int:
        async with new_session() as session:
            stream_dict = data.model_dump()

            stream = StreamOrm(**stream_dict, owner_id=owner_id)
            session.add(stream)
            await session.flush()
            await session.commit()
            return stream.id

    @staticmethod
    async def get_all() -> list[SStream]:
        async with new_session() as session:
            query = select(StreamOrm).options(joinedload(StreamOrm.owner))
            result = await session.execute(query)
            stream_models = result.scalars().all()
            stream_schemas = [
                SStream.model_validate(stream_model).copy(update={"owner_name": stream_model.owner.username})
                for stream_model in stream_models
            ]
            return stream_schemas

    @staticmethod
    async def get_user_streams(owner_id: int) -> list[SStream]:
        # Возвращает все стримы, принадлежащие конкретному пользователю.
        async with new_session() as session:
            query = select(StreamOrm).where(StreamOrm.owner_id == owner_id)
            result = await session.execute(query)
            stream_models = result.scalars().all()
            return [SStream.model_validate(stream_model) for stream_model in stream_models]

    @staticmethod
    async def get_stream_by_id(stream_id: int) -> StreamOrm:
        # Возвращает стрим по ID, если он существует.
        async with new_session() as session:
            query = select(StreamOrm).where(StreamOrm.id == stream_id)
            result = await session.execute(query)
            return result.scalars().first()

    @staticmethod
    async def update_stream(stream_id: int, data: StreamCreate) -> bool:
        async with new_session() as session:
            query = (
                update(StreamOrm)
                .where(StreamOrm.id == stream_id)
                .values(**data.model_dump())
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0  # Возвращает True, если обновление произошло

    @staticmethod
    async def delete_stream(stream_id: int) -> bool:
        async with new_session() as session:
            query = (
                delete(StreamOrm)
                .where(StreamOrm.id == stream_id)
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0  # Возвращает True, если удаление произошло


class UserRepository:
    @staticmethod
    async def create_user(data: UserCreate) -> User:
        async with new_session() as session:
            user = UserOrm(**data.model_dump())
            session.add(user)
            await session.flush()
            await session.commit()
            return user

    @staticmethod
    async def get_user_by_username(username: str) -> UserOrm:
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.username == username)
            result = await session.execute(query)
            user = result.scalars().first()
            return user

    @staticmethod
    async def get_user_by_email(email: str) -> UserOrm:
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.email == email)
            result = await session.execute(query)
            return result.scalars().first()

    @staticmethod
    async def confirm_user_email(user_id: int):
        async with new_session() as session:
            async with session.begin():
                user = await session.get(UserOrm, user_id)
                if user:
                    user.is_verified = True
                    await session.commit()