from sqlalchemy import Column, String
from pydantic import BaseModel
from typing import Optional

from database import Base


class Film(Base):
    __tablename__ = "films"
    id_imdb = Column(String, primary_key=True, unique=True, index=True)
    hash_torrent = Column(String, unique=True, index=True)

# Search TMDB content
class TMDBRequest(BaseModel):
    mediaType: str
    apiKey: str
    lang: Optional[str] = "en-US"

    class Config:
        schema_extra = {
            "example": {
                "mediaType": "movie",
                "apiKey": "569760ff55e24c593b9cf89e8503decd"
                }
        }


class TMDBSearch(TMDBRequest):
    query: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "mediaType": "movie",
                "apiKey": "569760ff55e24c593b9cf89e8503decd",
                "query": "Deadpool 2"
            }
        }


class TMBDContent(TMDBRequest):
    id: int

    class Config:
        schema_extra = {
            "example": {
                "id": 383498
            }
        }

class TMDBMovieInfo(TMBDContent):
    title: str
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

# Search torrent class
class TorrentRequest(BaseModel):
    query: str
    apiKey: str
    host: str
    mediaType: str
    sizeMax: Optional[int] = 15000000000
    encoding: Optional[str] = "264"
    resolution: Optional[str] = "1080"

    class Config:
        schema_extra = {
            "example": {
                "query": "Deadpool 2",
                "apiKey": "pfpk2qtgiik9dvctqxpk54txn58vyudf",
                "host": "jk.etur.fr",
                "mediaType": "movie",
                "sizeMax": 15000000000,
                "encoding": "264",
                "resolution": "1080"
            }
        }



class TorrentFind(BaseModel):
    title: str
    category: str
    size: int
    seeders: int
    url: str
