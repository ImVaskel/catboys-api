import pathlib
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from catboys.db.base import Base


class Media(Base):
    __tablename__ = "media"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    file_extension: Mapped[str]

    url: Mapped[str] = ""
    artist_url: Mapped[str] = ""
    artist_name: Mapped[str] = ""
    source_url: Mapped[str] = ""
    anime: Mapped[str] = ""

    def get_file_path(self):
        return pathlib.Path("media") / self.id / self.file_extension