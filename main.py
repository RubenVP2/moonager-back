from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine
import crud
import jackett
import tmdb
from models import TMDBRequest, TMDBSearch, TorrentRequest, Film


# Initialization
models.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Moonager-back",
    version="0.0.1",
    contact={
        "name": "Mange mort squad",
        "url": "https://mangemort-squad.myspreadshop.fr/",
        "email": "667@mangemort-squad.com",
    },
    license_info={
        "name": " MIT License  ",
        "url": "https://mit-license.org/",
    },
)

# Dependency for db


def get_db():
    """
    Ouverture de la session database
    Se ferme automatiquement après le return d'une réponse http
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Routes API
@app.get("/")
def read_root():
    """
    Route de base de l'API
    """
    return {"ekip": "https://youtu.be/-lDdP5o_Yao?t=13"}


@app.post("/top")
async def get_top(request: TMDBRequest):
    """
    Retourne le top 20 des films populaires
    """
    top = tmdb.get_populars(request)
    return top


@app.post("/searchTorrent")
def get_torrent(query: TorrentRequest, db: Session = Depends(get_db)):
    """
    Retourne l'url du torrent pour un film
    """
    torrent = jackett.find_torrent(query)
    # crud.create_film(db, Film(id_imdb=1, hash_torrent="TEST"))
    return torrent


@app.post("/search")
def search_from_tmdb(search: TMDBSearch):
    """
    Recherche et retourne les infos d'un film
    """
    content = tmdb.find_content(search)
    return content


@app.get("/films")
def read_films(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retourne tous les films de la base de données
    """
    films = crud.get_films(db, skip=skip, limit=limit)
    return films


@app.get("/films/{film_id}/delete")
def delete_film(film_id: int, db: Session = Depends(get_db)):
    """
    Supprime un film de la base de données
    """
    # A modifier, actuellement supprime un film dans la base de données avec un vieu id et hash
    film = crud.delete_film(db, film_id=film_id)
    return film
