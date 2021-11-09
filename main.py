import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine
import crud
import tmdb

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency for db
# TODO: Not use Franglais in your functions naming (example: replace delete_film with delete_movie)


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
    return {"ekip"}


@app.get("/{media_type}s/top")
# TODO: Use GET Method for searching media instead POST
async def get_top20(media_type: str, db: Session = Depends(get_db)):
    top20 = tmdb.get_popular(media_type=media_type)
    movie = db.query(models.Movie).filter(models.Movie.id_imdb == top20[0].id).first()
    if movie is not None:
        top20[0].added = True
        top20[0].progress = 30
    return top20


@app.post("/movies/add")
def add_movie(movie: tmdb.TMDBContent, db: Session = Depends(get_db)):
    return movie


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
