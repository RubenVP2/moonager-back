import requests

class TMBDContent:
    def __init__(self, id, name, mediaType, adult, videos):
        self.id = id
        self.name = name
        self.mediaType = mediaType
        self.adult = adult
        self.videos= videos

class TMDBMovieInfo(TMBDContent):
    def __init__(self, poster, backdrop, genres, overview, runtime, release_date, vote_average, popularity, collection):
        self.backdrop = backdrop
        self.poster = poster
        self.genres = genres
        self.overview = overview
        self.runtime = runtime
        self.release_date = release_date
        self.vote_average = vote_average
        self.popularity = popularity
        self.collection = collection

def getPopulars(mediaType, apiKey, language):
    print("start top request")
    responseTop = requests.get("https://api.themoviedb.org/3/"+mediaType+"/popular?api_key="+apiKey+"&language="+language).json()
    print("stop top request")
    content = {}
    for index, results in enumerate(responseTop["results"]):
        print("start video request", index)
        reponseVideo = requests.get("https://api.themoviedb.org/3/"+mediaType+"/"+str(results["id"])+"/videos?api_key="+apiKey+"&language="+language).json()
        print("stop video request", index)
        if mediaType == "movie":
            content[format(index)] = TMBDContent(results["id"], results["title"], mediaType, results["adult"], reponseVideo["results"])
        elif mediaType == "tv":
            content[format(index)] = TMBDContent(results["id"], results["name"], mediaType, results["adult"], reponseVideo["results"])
    return content

#def getInfos(id, mediaType, apiKey, language):
#    responseInfo = requests.get("https://api.themoviedb.org/3/"+mediaType+"/"+id+"?api_key="+apiKey+"&language="+language).json()
#    content = {}
#    for index, results in enumerate(responseTop["results"]):
top20=getPopulars("movie", "569760ff55e24c593b9cf89e8503decd", "language=fr-FR")