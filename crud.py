from sqlalchemy.orm import Session



import models




def get_film(db: Session, film_id: str):

    return db.query(models.Film).filter(models.Film.id_imdb == film_id).first()




def get_film_by_hash(db: Session, hash_torrent: str):

    return db.query(models.Film).filter(models.Film.hash_torrent == hash_torrent).first()




def get_films(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Film).offset(skip).limit(limit).all()



def create_film(db: Session, film: models.Film):
    db_film = models.Film(id_imdb=film.id_imdb, hash_torrent=film.hash_torrent)
    db.add(db_film)
    db.commit()
    db.refresh(db_film)
    return db_film



def delete_film(db: Session, film_id: int):
    db_film = db.query(models.Film).get(film_id)
    if db_film:
        db.delete(db_film)
        db.commit()
        return {'message': 'Film deleted', 'film': db_film}