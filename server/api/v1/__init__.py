from fastapi import APIRouter

from api.v1 import auth_api, user_api, appointment_api, message_api, analytics_api

api_router = APIRouter()
api_router.include_router(auth_api.router, prefix="/auth", tags=["🔑 auth"])
api_router.include_router(user_api.router, prefix="/users", tags=["👤 users"])
api_router.include_router(
    appointment_api.router, prefix="/appointments", tags=["📅 appointments"]
)
api_router.include_router(message_api.router, prefix="/messages", tags=["✉️ messages"])
api_router.include_router(analytics_api.router, prefix="/analytics", tags=["📊 analytics"])
