import feedparser
import requests
import re
import urllib.parse

from models import TorrentFind


def find_torrent(request):
    """
    Recherche un torrent en fonction de son nom, encodage, resolution, taille
    request: Objet TorrentRequest
    """
    #Transformation du libelle mediaType en id catégorie yggtorrent
    if request.mediaType == "tv":
        request.mediaType = "102184"
    elif request.mediaType == "movie":
        request.mediaType = "102183"
    #Creation du regex
    regex = "^"
    if request.encoding is not None:
        regex = regex + "(?=.*" + request.encoding + ".*)"
    if request.resolution is not None:
        regex = regex + "(?=.*" + request.resolution + ".*)"
    #Creation et requêtage de l'url jackett
    baseURL = "http://"+request.host+"/api/v2.0/indexers/yggcookie/results/torznab/api?"
    getParametre={"apikey": request.apiKey, "t": "search", "cat": request.mediaType, "q": request.query}
    url = baseURL+urllib.parse.urlencode(getParametre)
    result_parsed = feedparser.parse(url)
    result_no_parsed = requests.get(url)
    #On parcoure les résultats en récupérant les infos necessaire
    torrent = {}
    for index, entry in enumerate(result_parsed.entries):
        seeders = result_no_parsed.text.split(
            "<item>")[index + 1].split("seeders")[1].split("\"")[2]
        if len(entry) > index:
            if re.search(regex, entry.title, re.IGNORECASE):
                if int(entry.size) < int(request.sizeMax):
                    torrent[index] = TorrentFind(
                        title=entry.title, category=request.mediaType, size=entry.size, seeders=seeders, url=entry.link)
    return torrent
