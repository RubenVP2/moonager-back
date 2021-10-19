from typing import Optional, List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

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
    return {"Hello": "World"}


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

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}