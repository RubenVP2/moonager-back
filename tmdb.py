import requests
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional

apiKey: str = "569760ff55e24c593b9cf89e8503decd"

class TMDBRequest(BaseModel):
    media_type: str
    lang: Optional[str] = "fr-FR"


class TMDBSearch(TMDBRequest):
    query: Optional[str] = None


class TMBDContent(TMDBRequest):
    id: int
    name: Optional[str] = None


class TMDBMovieInfo(TMBDContent):
    backdrop: str
    poster: str
    genres: list
    overview: str
    runtime: str
    release_date: str
    vote_average: float
    vote_count: int
    popularity: float
    collection: Optional[dict] = None
    adult: str
    videos: list


def get_popular(media_type):
    tmdb = TMDBRequest(media_type=media_type)
    response = requests.get("https://api.themoviedb.org/3/"+media_type +
                               "/popular?api_key="+apiKey+"&language="+tmdb.lang).json()
    content = []
    try:
        for index, media in enumerate(response["results"]):
            # reponseVideo = requests.get("https://api.themoviedb.org/3/"+media_type+"/"+str(
            #     results["id"])+"/videos?api_key="+request.apiKey+"&language="+request.lang).json()
            if media_type == "movie":
                content.append(TMDBMovieInfo(media_type=tmdb.media_type,
                                             lang=tmdb.lang,
                                             id=media["id"],
                                             name=media["title"],
                                             backdrop="https://image.tmdb.org/t/p/original" + media["backdrop_path"],
                                             poster="https://image.tmdb.org/t/p/original" + media["poster_path"],
                                             genres=media["genre_ids"],
                                             overview=media["overview"],
                                             runtime="",
                                             release_date=media["release_date"],
                                             vote_average=media["vote_average"],
                                             vote_count=media["vote_count"],
                                             popularity=media["popularity"],
                                             adult=media["adult"],
                                             videos=[]))
            elif media_type == "tv":
                content.append(TMBDContent(media_type=tmdb.media_type,
                                           lang=tmdb.lang,
                                           id=media["id"],
                                           name=media["name"]))
        return content
    except Exception as error:
        print(error)
        if "status_message" in response:
            raise HTTPException(status_code=500, detail=response["status_message"])
        else:
            raise HTTPException(status_code=500, detail="Internal error")


def search(search):
    responseSearch = requests.get("https://api.themoviedb.org/3/search/"+search.mediaType+"?api_key=" +
                                  apiKey+"&language="+search.lang+"&language="+search.lang+"&query="+search.query).json()
    return responseSearch


def get_media_info(media):
    reponseVideo = requests.get("https://api.themoviedb.org/3/"+media.mediaType +
                                "/"+str(media.id)+"/videos?api_key="+apiKey+"&language="+media.lang).json()
    responseInfo = requests.get("https://api.themoviedb.org/3/"+media.mediaType +
                                "/"+str(media.id)+"?api_key="+apiKey+"&language="+media.lang).json()
    info = TMDBMovieInfo(
        mediaType=media.mediaType,
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
