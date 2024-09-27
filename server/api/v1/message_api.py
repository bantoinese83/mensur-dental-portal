from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_db_session
from crud.message_crud import (
    create_message,
    get_message,
    update_message,
    delete_message,
)
from schemas.message_schema import Message, MessageCreate, MessageUpdate

router = APIRouter()


@router.post(
    "/",
    response_model=Message,
    summary="Create a new message",
    description="Create a new message in the system with the provided details. 🆕",
)
def create_new_message(message: MessageCreate, db: Session = Depends(get_db_session)):
    return create_message(db, message)


@router.get(
    "/{message_id}",
    response_model=Message,
    summary="Read message details",
    description="Retrieve the details of a message by its ID. 📖",
)
def read_message(message_id: int, db: Session = Depends(get_db_session)):
    return get_message(db, message_id)


@router.put(
    "/{message_id}",
    response_model=Message,
    summary="Update message details",
    description="Update the details of an existing message by its ID. ✏️",
)
def update_existing_message(
    message_id: int, message: MessageUpdate, db: Session = Depends(get_db_session)
):
    return update_message(db, message_id, message)


@router.delete(
    "/{message_id}",
    response_model=Message,
    summary="Delete a message",
    description="Delete an existing message from the system by its ID. 🗑️",
)
def delete_existing_message(message_id: int, db: Session = Depends(get_db_session)):
    return delete_message(db, message_id)
