from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from database import Base


class Film(Base):

    __tablename__ = "films"

    id_imdb = Column(String, primary_key=True, unique=True, index=True)
    hash_torrent = Column(String, unique=True, index=True)
