import uvicorn
from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from pkg_resources import resource_listdir
from typing import Optional, List
import models
import crud
import search
import tmdb
import torrent

# Initialization
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency for db
# TODO: Not use Franglais in your functions naming (example: replace delete_film with delete_movie)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Routes API
@app.get("/")
def read_root():
    return {"ekip"}


@app.get("/{media_type}s/top")
# TODO: Use GET Method for searching media instead POST
async def get_top20(media_type: str):
    top20 = tmdb.get_popular(media_type=media_type)
    return top20


@app.post("/movies/add")
def add_movie(query: search.TorrentRequest, db: Session = Depends(get_db)):
    torrent = search.findTorrent(query)
    #film = crud.create_film(db, models.Film(id_imdb=1, hash_torrent="TEST"))
    return torrent


@app.get("/search/")
# TODO: Use GET Method for searching media instead POST
def tmdb_search(search: tmdb.TMDBSearch):
    content = tmdb.search(search)
    return content


@app.get("/movies")
def read_films(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    films = crud.get_movies(db, skip=skip, limit=limit)
    return films


@app.post("/movies/delete")
def delete_movie(request: models.Media, db: Session = Depends(get_db)):
    film = crud.delete_movie(db, movie_id=request.id)
    return film

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
