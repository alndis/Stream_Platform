from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from repository import StreamRepository
from schemas import StreamCreate, SStream, StreamID, User
from auth_router import get_current_user


router = APIRouter(
    prefix="/api/streams",
    tags=["Стримы"],
)

# Зависимость для получения текущего пользователя
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.post("")
async def create_stream(
        stream: StreamCreate,
        current_user: User = Depends(get_current_user)  # Проверка на авторизацию
) -> StreamID:

    streams_id = await StreamRepository.create_stream(stream, owner_id=current_user.id)
    return {"ok": True, "stream_id": streams_id, "message": "Стрим успешно добавлен."}



@router.get("")
async def get_stream(
        #current_user: User = Depends(get_current_user)  # Проверка на авторизацию
) -> list[SStream]:
    streams = await StreamRepository.get_all()
    return streams

@router.put("/{stream_id}")
async def update_stream(
        stream_id: int,
        stream: StreamCreate,
        current_user: User = Depends(get_current_user)  # Проверка на авторизацию
) -> dict:
    # Проверяем, принадлежит ли стрим текущему пользователю
    existing_stream = await StreamRepository.get_stream_by_id(stream_id)
    if not existing_stream or existing_stream.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Вы не являетесь автором стрима")

    # Обновляем стрим
    updated = await StreamRepository.update_stream(stream_id, stream)
    if not updated:
        raise HTTPException(status_code=404, detail="Стрим не найден")
    return {"ok": True, "stream_id": stream_id}

@router.delete("/{stream_id}")
async def delete_stream(
        stream_id: int,
        current_user: User = Depends(get_current_user)  # Проверка на авторизацию
) -> dict:
    # Проверяем, принадлежит ли стрим текущему пользователю
    existing_stream = await StreamRepository.get_stream_by_id(stream_id)
    if not existing_stream or existing_stream.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Вы не являетесь автором стрима")

    # Удаляем стрим
    deleted = await StreamRepository.delete_stream(stream_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Стрим не найден")
    return {"ok": True, "stream_id": stream_id}
