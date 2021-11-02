from typing import Optional

from sqlalchemy import Column, String
from pydantic import BaseModel

from database import Base


class Movie(Base):
    __tablename__ = "films"

    id_imdb = Column(String, primary_key=True, unique=True, index=True)
    hash_torrent = Column(String, unique=True, index=True)


class Media(BaseModel):
    id: str
    name: Optional[str] = None
