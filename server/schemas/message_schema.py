# server/schemas/message_schema.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MessageBase(BaseModel):
    sender_id: int
    receiver_id: int
    content: str


class MessageCreate(MessageBase):
    pass


class MessageUpdate(MessageBase):
    content: Optional[str] = None


class MessageInDBBase(MessageBase):
    id: int
    sent_at: datetime

    class Config:
        orm_mode = True


class Message(MessageInDBBase):
    pass


class MessageInDB(MessageInDBBase):
    pass
