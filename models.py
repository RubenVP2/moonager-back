from typing import Optional

from sqlalchemy import Column, String
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import Base


class Movie(Base):
    __tablename__ = "films"
    id_imdb = Column(String, primary_key=True, unique=True, index=True)
    hash_torrent = Column(String, unique=True, index=True)

    def __str__(self):
        return self.id_imdb + " - " + self.hash_torrent


# Search TMDB content

class TMDBRequest(BaseModel):
    media_type: str
    lang: Optional[str] = "fr-FR"

    class Config:
        schema_extra = {
            "example": {
                "media_type": "movie",
            }
        }


class TMDBSearch(TMDBRequest):
    query: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "media_type": "movie",
                "query": "Deadpool 2"
            }
        }


class TMDBContent(TMDBRequest):
    id: int
    name: Optional[str] = None


class TMDBMovieInfo(TMDBContent):
    backdrop: str
    poster: str
    genres: list
    overview: str
    runtime: str
    release_date: str
    vote_average: float
    vote_count: int
    popularity: float
    collection: Optional[dict] = None
    adult: str
    videos: list
    added: bool = False
    progress: float = 0


class TorrentFind(BaseModel):
    title: str
    category: str
    size: int
    seeders: int
    url: str


class Media(BaseModel):
    id: str
    name: Optional[str] = None


def get_movie_local_infos(db: Session, movie: TMDBContent):
    movie_infos = db.query(Movie).filter(Movie.id_imdb == movie.id).first()
    if movie_infos is not None:
        movie.added = True

    return movie