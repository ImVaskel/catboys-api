from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from catboys.core import settings

from .base import Base
from .models import Media, Submission

engine = create_async_engine(str(settings.db_url), future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
