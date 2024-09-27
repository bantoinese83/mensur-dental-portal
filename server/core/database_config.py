# server/database_config.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app_config import settings

# Create the SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created")

