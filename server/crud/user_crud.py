from sqlalchemy.orm import Session

from models.user_model import User
from schemas.user_schema import UserCreate, UserUpdate
from utils.cache_utils import set_cache, get_cache, delete_cache


def get_user(db: Session, user_id: int):
    cache_key = f"user:{user_id}"
    cached_user = get_cache(cache_key)
    if cached_user:
        return cached_user

    user = db.query(User).filter(User.id == user_id).first()
    if user:
        set_cache(cache_key, user, expire=3600)  # Cache for 1 hour
    return user


def get_user_by_email(db: Session, email: str):
    cache_key = f"user:email:{email}"
    cached_user = get_cache(cache_key)
    if cached_user:
        return cached_user

    user = db.query(User).filter(User.email == email).first()
    if user:
        set_cache(cache_key, user, expire=3600)  # Cache for 1 hour
    return user


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=user.password,  # Hash the password in a real application
        full_name=user.full_name,
        is_active=user.is_active,
        is_dentist=user.is_dentist,
        preferences=user.preferences,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    delete_cache(f"user:email:{db_user.email}")  # Invalidate cache
    return db_user


def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        delete_cache(f"user:{user_id}")  # Invalidate cache
        delete_cache(f"user:email:{db_user.email}")  # Invalidate cache
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        delete_cache(f"user:{user_id}")  # Invalidate cache
        delete_cache(f"user:email:{db_user.email}")  # Invalidate cache
    return db_user