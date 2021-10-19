from fastapi import FastAPI

from torrent import test_dl_billie
from torrent import test_rm_all
from tmdb import popular


app = FastAPI()

import json

@app.get("/")
def read_root():
    r=popular("tv", "569760ff55e24c593b9cf89e8503decd")
    print(r["1"].id)
    return {"r:": "test"}

@app.get("/rm")
def read_root():
    test_rm_all()


@app.get("/top/{media}/{top}")
def read_item(media: str, top: int):
    r=popular(media, "569760ff55e24c593b9cf89e8503decd")
    return {
        "top": top,
        "name": r[format(top)].title,
        "id": r[format(top)].id,
    }