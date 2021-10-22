from sqlalchemy import Column, String
from pydantic import BaseModel
from typing import Optional

from database import Base


class Film(Base):
    __tablename__ = "films"

    id_imdb = Column(String, primary_key=True, unique=True, index=True)
    hash_torrent = Column(String, unique=True, index=True)


class TMDBRequest(BaseModel):
    mediaType: str
    apiKey: str
    lang: Optional[str] = "en-US"


class TMDBSearch(TMDBRequest):
    query: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "query": "Deadpool 2"
            }
        }


class TMBDContent(TMDBRequest):
    id: int
    name: Optional[str] = None


class TMDBMovieInfo(TMBDContent):
    backdrop: str
    poster: str
    genres: dict
    overview: str
    runtime: int
    release_date: str
    vote_average: float
    vote_count: int
    popularity: float
    collection: Optional[dict] = None
    adult: str
    videos: list


class TorrentRequest(BaseModel):
    query: str
    mediaType: str
    sizeMax: Optional[int] = 15000000000
    encoding: Optional[str] = "264"
    resolution: Optional[str] = "1080"


class TorrentFind(BaseModel):
    title: str
    category: str
    size: int
    seeders: int
    url: str
