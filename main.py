<<<<<<< HEAD
import json
from fastapi import FastAPI
from pkg_resources import resource_listdir

from torrent import test_dl_billie
from torrent import test_rm_all
from tmdb import popular
import search
=======
from typing import Optional, List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
>>>>>>> 0776f59681562b305510efd9d5b30c067af0ec9a

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    r = popular("tv", "569760ff55e24c593b9cf89e8503decd")
    print(r["1"].id)
    return {"r:": "test"}


@app.get("/rm")
def read_root():
    test_rm_all()


@app.get("/top/{media}/{top}")
def read_item(media: str, top: int):
    p = popular(media, "569760ff55e24c593b9cf89e8503decd")
    t = search.findTorrent(p[format(top)].title, media, "x264", "1080p")
    # print(p[format(top)].title)
    return {
        "top": top,
        "name": p[format(top)].title,
        "id": p[format(top)].id,
        "dl": t.url if t else "not found",
    }

@app.get("/films")
def read_films(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    films = crud.get_films(db, skip=skip, limit=limit)
    return films


@app.get("/films/add")
def add_film(db: Session = Depends(get_db)):
    # A modifier, actuellement insert un film dans la base de données avec un vieu id et hash
    film = crud.create_film(db, models.Film(id_imdb=1, hash_torrent="TEST"))
    return film

@app.get("/films/{film_id}/delete")
def delete_film(film_id: int, db: Session = Depends(get_db)):
    # A modifier, actuellement supprime un film dans la base de données avec un vieu id et hash
    film = crud.delete_film(db, film_id=film_id)
    return film

@app.get("/top/{media}/")
async def read_item(media: str):
    result = {}
    p = popular(media, "569760ff55e24c593b9cf89e8503decd")
    n = 1
    # {print(p)
    for key, value in p.items():
        print(key)
        t = search.findTorrent(value.title, media, "x264", "1080p")
        result[n] = {"top": value.top, "name": value.title,
                     "id": value.id, "dl": t.url if t else "not found"}
        n = n+1
    # print(p[format(top)].title)
    return result
