import requests
from fastapi import HTTPException
from models import *

tmdb_picture_base_link = "https://image.tmdb.org/t/p/original"
apiKey: str = "569760ff55e24c593b9cf89e8503decd"

def get_popular(media_type):
    tmdb = TMDBRequest(media_type=media_type)
    response = requests.get("https://api.themoviedb.org/3/" + media_type +
                            "/popular?api_key=" + apiKey + "&language=" + tmdb.lang).json()
    content = []
    try:
        for index, media in enumerate(response["results"]):
            if media_type == "movie":
                content.append(TMDBMovieInfo(media_type=tmdb.media_type,
                                             lang=tmdb.lang,
                                             id=media["id"],
                                             name=media["title"],
                                             backdrop=tmdb_picture_base_link + media["backdrop_path"],
                                             poster=tmdb_picture_base_link + media["poster_path"],
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
                content.append(TMDBContent(media_type=tmdb.media_type,
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


def search(media):
    response_search = requests.get("https://api.themoviedb.org/3/search/" + media.media_type + "?api_key=" +
                                   apiKey + "&language=" + media.lang + "&language=" + media.lang +
                                   "&query=" + media.query).json()
    return response_search


def get_media_info(media):
    response_video = requests.get("https://api.themoviedb.org/3/" + media.media_type +
                                  "/" + str(media.id) + "/videos?api_key=" + apiKey + "&language=" + media.lang).json()
    response_info = requests.get("https://api.themoviedb.org/3/" + media.media_type +
                                 "/" + str(media.id) + "?api_key=" + apiKey + "&language=" + media.lang).json()
    info = TMDBMovieInfo(
        media_type=media.media_type,
        lang=media.lang,
        id=media.id,
        name=response_info["title"],
        backdrop=tmdb_picture_base_link + response_info["backdrop_path"],
        poster=tmdb_picture_base_link + response_info["poster_path"],
        genres=response_info["genres"],
        overview=response_info["overview"],
        runtime=response_info["runtime"],
        release_date=response_info["release_date"],
        vote_average=response_info["vote_average"],
        vote_count=response_info["vote_count"],
        popularity=response_info["popularity"],
        adult=response_info["adult"],
        videos=response_video["results"]
    )
    return info
