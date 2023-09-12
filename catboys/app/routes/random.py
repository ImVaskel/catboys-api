from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from catboys.db import models

from catboys.db.dependency import get_db


router = APIRouter()


class RandomCatboy(BaseModel):
    url: str
    artist_url: str
    artist_name: str
    source_url: str
    anime: str

    class Config:
        from_attributes = True


@router.get("/")
async def random_catboy(
    limit: int = 1, db: AsyncSession = Depends(get_db)
) -> list[RandomCatboy]:
    catboys = await db.execute(
        select(models.Media).order_by(func.random()).limit(limit)
    )

    return catboys.scalars().all()
