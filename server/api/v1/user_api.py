# server/api/v1/user_api.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_db_session, get_current_active_user
from crud.user_crud import create_user, update_user, delete_user
from schemas.user_schema import User, UserCreate, UserUpdate

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
    "/me",
    response_model=User,
    summary="Get current user profile",
    description="Retrieve the profile of the currently authenticated user. 📖",
)
def read_user_profile(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.put(
    "/me",
    response_model=User,
    summary="Update current user profile",
    description="Update the profile of the currently authenticated user. ✏️",
)
def update_user_profile(
        user: UserUpdate, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_active_user)
):
    return update_user(db, user_id=current_user.id, user=user)


@router.delete(
    "/{user_id}",
    response_model=User,
    summary="Delete a user",
    description="Delete an existing user from the system by their ID. 🗑️",
)
def delete_existing_user(user_id: int, db: Session = Depends(get_db_session)):
    return delete_user(db, user_id)
