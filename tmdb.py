import requests
from pydantic import BaseModel
from typing import Optional


class TMDBRequest(BaseModel):
    mediaType: str
    apiKey: str
    lang: Optional[str] = "en-US"


class TMBDContent(TMDBRequest):
    id: int
    name: Optional[str] = None


class TMDBMovieInfo(TMBDContent):
    backdrop: str
    poster: str
    genres: dict
    overview: str
    runtime: int
    release_date: str
    vote_average: float
    vote_count: int
    popularity: float
    collection: Optional[dict] = None
    adult: str
    videos: list


def getPopulars(request):
    responseTop = requests.get("https://api.themoviedb.org/3/"+request.mediaType +
                               "/popular?api_key="+request.apiKey+"&language="+request.lang).json()
    content = {}
    for index, results in enumerate(responseTop["results"]):
        print("start video request", index)
        reponseVideo = requests.get("https://api.themoviedb.org/3/"+request.mediaType+"/"+str(
            results["id"])+"/videos?api_key="+request.apiKey+"&language="+request.lang).json()
        print("stop video request", index)
        if request.mediaType == "movie":
            content[format(index)] = TMBDContent(mediaType=request.mediaType,
                                                 apiKey=request.apiKey, lang=request.lang, id=results["id"], name=results["title"])
        elif request.mediaType == "tv":
            content[format(index)] = TMBDContent(mediaType=request.mediaType,
                                                 apiKey=request.apiKey, lang=request.lang, id=results["id"], name=results["name"])
    return content


def getInfos(content):
    reponseVideo = requests.get("https://api.themoviedb.org/3/"+content.mediaType +
                                "/"+str(content.id)+"/videos?api_key="+content.apiKey+"&language="+content.lang).json()
    #print(type(reponseVideo["results"]))
    responseInfo = requests.get("https://api.themoviedb.org/3/"+content.mediaType +
                                "/"+str(content.id)+"?api_key="+content.apiKey+"&language="+content.lang).json()
    print(responseInfo["belongs_to_collection"])
    info = TMDBMovieInfo(
            mediaType=content.mediaType,
            apiKey=content.apiKey,
            lang=content.lang,
            id=content.id,
            name=content.name,
            backdrop=responseInfo["backdrop_path"],
            poster=responseInfo["poster_path"],
            genres=responseInfo["genres"],
            overview=responseInfo["overview"],
            runtime=responseInfo["runtime"],
            release_date=responseInfo["release_date"],
            vote_average=responseInfo["vote_average"],
            vote_count=responseInfo["vote_count"],
            popularity=responseInfo["popularity"],
            adult=responseInfo["adult"],
            videos=reponseVideo["results"]
    )
    if responseInfo["belongs_to_collection"]:
        info = TMDBMovieInfo(collection=responseInfo["belongs_to_collection"])

    return info