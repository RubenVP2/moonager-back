import requests
from pydantic import BaseModel
from typing import Optional


class TMDBRequest(BaseModel):
    mediaType: str
    apiKey: Optional[str] = "569760ff55e24c593b9cf89e8503decd"
    lang: Optional[str] = "fr-FR"


class TMDBSearch(TMDBRequest):
    query: Optional[str] = None


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


def get_popular(media_type):
    tmdb = TMDBRequest()
    responseTop = requests.get("https://api.themoviedb.org/3/"+media_type +
                               "/popular?api_key="+tmdb.apiKey+"&language="+tmdb.lang).json()
    content = {}
    for index, results in enumerate(responseTop["results"]):
        # reponseVideo = requests.get("https://api.themoviedb.org/3/"+media_type+"/"+str(
        #     results["id"])+"/videos?api_key="+request.apiKey+"&language="+request.lang).json()
        if media_type == "movie":
            content[format(index)] = TMBDContent(mediaType=media_type,
                                                 apiKey=tmdb.apiKey, lang=tmdb.lang, id=results["id"], name=results["title"])
        elif media_type == "tv":
            content[format(index)] = TMBDContent(mediaType=media_type,
                                                 apiKey=tmdb.apiKey, lang=tmdb.lang, id=results["id"], name=results["name"])
    return content


def search(search):
    responseSearch = requests.get("https://api.themoviedb.org/3/search/"+search.mediaType+"?api_key=" +
                                  search.apiKey+"&language="+search.lang+"&language="+search.lang+"&query="+search.query).json()
    return responseSearch


def get_media_info(media):
    reponseVideo = requests.get("https://api.themoviedb.org/3/"+media.mediaType +
                                "/"+str(media.id)+"/videos?api_key="+media.apiKey+"&language="+media.lang).json()
    responseInfo = requests.get("https://api.themoviedb.org/3/"+media.mediaType +
                                "/"+str(media.id)+"?api_key="+media.apiKey+"&language="+media.lang).json()
    info = TMDBMovieInfo(
        mediaType=media.mediaType,
        apiKey=media.apiKey,
        lang=media.lang,
        id=media.id,
        name=media.name,
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
