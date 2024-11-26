from typing import Optional

from pydantic import BaseModel, ConfigDict


class StreamCreate(BaseModel):
    name: str
    description: Optional[str] = None
    preview: Optional[str] = None
    link: Optional[str] = None
class SStream(StreamCreate):
    id: int
    owner_name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class StreamID(BaseModel):
    ok: bool = True
    stream_id: int



class UserCreate(BaseModel):
    email: str
    username: str
    password: str
class User(UserCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str
