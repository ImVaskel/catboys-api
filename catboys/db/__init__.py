from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from catboys.core import settings

from .base import Base
from .models import Media

engine = create_engine(settings.db_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
