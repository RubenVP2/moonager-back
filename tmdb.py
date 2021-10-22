import requests

from models import TMBDContent, TMDBMovieInfo

# Création de constante pour les str utilisés plusieurs fois
TMDB_API = "https://api.themoviedb.org/3/"
PARAM_LANGUAGE = "&language="


def get_populars(request):
    """
    Cette fonction retourne le top 20 des films populaires depuis l'api TMDB
    request: Objet TMDBRequest
    """
    response_from_tmdb = requests.get(TMDB_API + request.mediaType +
                                      "/popular?api_key=" + request.apiKey + PARAM_LANGUAGE + request.lang).json()
    content = {}
    for index, results in enumerate(response_from_tmdb["results"]):
        if request.mediaType == "movie":
            content[format(index)] = TMBDContent(mediaType=request.mediaType,
                                                 apiKey=request.apiKey, lang=request.lang, id=results["id"],
                                                 name=results["title"])
        elif request.mediaType == "tv":
            content[format(index)] = TMBDContent(mediaType=request.mediaType,
                                                 apiKey=request.apiKey, lang=request.lang, id=results["id"],
                                                 name=results["name"])
    return content


def find_content(search):
    """
    Cette fonction retourne la liste des films correspondant à la recherche
    search: Objet TMDBRequest
    """
    response_search = requests.get(TMDB_API+"search/" + search.mediaType + "?api_key=" +
                                   search.apiKey + PARAM_LANGUAGE + search.lang + PARAM_LANGUAGE + search.lang
                                   + "&query=" + search.query).json()
    return response_search


def get_infos(content):
    response_video = requests.get(TMDB_API + content.mediaType +
                                  "/" + str(content.id) + "/videos?api_key=" + content.apiKey + PARAM_LANGUAGE +
                                  content.lang).json()
    response_info = requests.get(TMDB_API + content.mediaType +
                                 "/" + str(content.id) + "?api_key=" + content.apiKey + PARAM_LANGUAGE +
                                 content.lang).json()
    info = TMDBMovieInfo(
        title=response_info["title"],
        mediaType=content.mediaType,
        apiKey=content.apiKey,
        lang=content.lang,
        id=content.id,
        backdrop=response_info["backdrop_path"],
        poster=response_info["poster_path"],
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
    if response_info["belongs_to_collection"]:
        info = TMDBMovieInfo(collection=response_info["belongs_to_collection"])
    return info
