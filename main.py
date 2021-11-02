import uvicorn
from fastapi import FastAPI, Depends
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


@app.post("/top/")
async def get_top20(request: tmdb.TMDBRequest):
    top20 = tmdb.getPopulars(request)
    return top20


@app.post("/addMovie/")
def addMovie(query: search.TorrentRequest, db: Session = Depends(get_db)):
    torrent = search.findTorrent(query)
    #film = crud.create_film(db, models.Film(id_imdb=1, hash_torrent="TEST"))
    return torrent


@app.post("/search/")
def TMBDSearch(search: tmdb.TMDBSearch):
    content = tmdb.findContent(search)
    return content


@app.get("/films")
def read_films(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    films = crud.get_films(db, skip=skip, limit=limit)
    return films


@app.get("/films/{film_id}/delete")
def delete_film(film_id: int, db: Session = Depends(get_db)):
    # A modifier, actuellement supprime un film dans la base de données avec un vieu id et hash
    film = crud.delete_film(db, film_id=film_id)
    return film

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)