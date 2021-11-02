from sqlalchemy.orm import Session
from fastapi import HTTPException

import models


def get_movie(db: Session, film_id: str):
    return db.query(models.Movie).filter(models.Movie.id_imdb == film_id).first()


def get_movie_by_hash(db: Session, hash_torrent: str):
    return db.query(models.Movie).filter(models.Movie.hash_torrent == hash_torrent).first()


def get_movies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Movie).offset(skip).limit(limit).all()


def create_movie(db: Session, film: models.Movie):
    db_film = models.Movie(id_imdb=film.id_imdb, hash_torrent=film.hash_torrent)
    db.add(db_film)
    db.commit()
    db.refresh(db_film)
    return db_film


def delete_movie(db: Session, movie_id: str):
    db_movie = db.query(models.Movie).get(movie_id)
    if db_movie:
        try:
            db.delete(db_movie)
            db.commit()
            return {'message': 'Film deleted', 'film': db_movie}
        except:
            db.rollback()
            raise HTTPException(status_code=500, detail="Error when deleting the movie")
    raise HTTPException(status_code=404, detail="Movie not found")
