import requests
import sys


class Tops:
    def __init__(self, id, media, top, title):
        self.id = id
        self.media = media
        self.top = top
        self.title = title


def popular(media, apiKey):
    response = requests.get(
        "https://api.themoviedb.org/3/"+media+"/popular?api_key="+apiKey)
    r = response.json()
    n = 0
    globals()[media] = {}
    for i in r["results"]:
        n = n+1
        if media == "movie":
            # sys.stderr.write("#"+str(n)+" "+i["title"]+" "+str(i["id"])+"\n")
            globals()[media][format(n)] = Tops(i["id"], media, n, i["title"])
        elif media == "tv":
            # sys.stderr.write("#"+str(n)+" "+i["name"]+" "+str(i["id"])+"\n")
            globals()[media][format(n)] = Tops(i["id"], media, n, i["name"])
    return globals()[media]


popular("movie", "569760ff55e24c593b9cf89e8503decd")
