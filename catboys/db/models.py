import uuid
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from catboys.db.base import Base


class Media(Base):
    __tablename__ = "media"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)

    url: Mapped[str] = mapped_column(default="")
    artist_url: Mapped[str] = mapped_column(default="")
    artist_name: Mapped[str] = mapped_column(default="")
    source_url: Mapped[str] = mapped_column(default="")
    anime: Mapped[str] = mapped_column(default="")


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    submitter: Mapped[int] = mapped_column(BigInteger)

    url: Mapped[str] = mapped_column(default="")
    artist_url: Mapped[str] = mapped_column(default="")
    artist_name: Mapped[str] = mapped_column(default="")
    source_url: Mapped[str] = mapped_column(default="")
    anime: Mapped[str] = mapped_column(default="")
