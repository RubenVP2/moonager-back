import json
from fastapi import FastAPI
from pkg_resources import resource_listdir

from torrent import test_dl_billie
from torrent import test_rm_all
from tmdb import popular
import search

app = FastAPI()


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
