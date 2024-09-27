import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from api.v1 import api_router
from core.celery_config import init_celery
from core.database_config import init_db
from core.middlewares import init_middlewares
from core.redis_config import init_redis

load_dotenv()

app = FastAPI(
    title="🏥 Dental Portal 🦷",
    description="Dental Portal FastAPI",
    version="0.1.0",
)

# Initialize middlewares
middleware_config = {
    "cors": True,
    "gzip": True,
    "session": True,
    "trusted_host": True,
    "error_handling": True,
    "rate_limit": True,
    "timeout": True,
}

init_middlewares(app, middleware_config)
init_redis()
init_db()
init_celery()

# Include your routers here
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
