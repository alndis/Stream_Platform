from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# Создание асинхронного движка базы данных для PostgreSQL
engine = create_async_engine(
    "postgresql+asyncpg://username:password@db/mydatabase",  # Замените на свои данные
)

new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass

# Модель для стримов
class StreamOrm(Model):
    __tablename__ = "stream"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    preview: Mapped[Optional[str]]
    link: Mapped[Optional[str]]
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    # Отношение к пользователю
    owner = relationship("UserOrm", back_populates="streams")

# Модель для пользователей
class UserOrm(Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)  # Уникальное имя пользователя
    email: Mapped[str] = mapped_column(unique=True)  # Уникальный email
    password: Mapped[str]  # Хранит хешированный пароль
    is_verified: Mapped[bool] = mapped_column(default=False)
    streams = relationship("StreamOrm", back_populates="owner", cascade="all, delete")

# Создание таблиц в базе данных
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

# Удаление всех таблиц из базы данных
async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
