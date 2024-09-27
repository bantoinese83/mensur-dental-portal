from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_db_session
from crud.user_crud import create_user, get_user, update_user, delete_user
from schemas.user_schema import User, UserCreate, UserUpdate
from services.appointment_service import days_between_appointments

router = APIRouter()


@router.post(
    "/",
    response_model=User,
    summary="Create a new user",
    description="Create a new user in the system with the provided details. 🆕",
)
def create_new_user(user: UserCreate, db: Session = Depends(get_db_session)):
    return create_user(db, user)


@router.get(
    "/{user_id}",
    response_model=User,
    summary="Read user details",
    description="Retrieve the details of a user by their ID. 📖",
)
def read_user(user_id: int, db: Session = Depends(get_db_session)):
    return get_user(db, user_id)


@router.put(
    "/{user_id}",
    response_model=User,
    summary="Update user details",
    description="Update the details of an existing user by their ID. ✏️",
)
def update_existing_user(
        user_id: int, user: UserUpdate, db: Session = Depends(get_db_session)
):
    return update_user(db, user_id, user)


@router.delete(
    "/{user_id}",
    response_model=User,
    summary="Delete a user",
    description="Delete an existing user from the system by their ID. 🗑️",
)
def delete_existing_user(user_id: int, db: Session = Depends(get_db_session)):
    return delete_user(db, user_id)


@router.get(
    "/days-between-appointments",
    summary="Calculate days between two appointments",
    description="Calculate the number of days between two appointments by their IDs. 📅",
)
def calculate_days_between_appointments(
        appointment_id1: int, appointment_id2: int, db: Session = Depends(get_db_session)
):
    days = days_between_appointments(db, appointment_id1, appointment_id2)
    return {"days_between_appointments": days}






