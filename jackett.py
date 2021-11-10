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
    #Transformation du libelle media_type en id catégorie yggtorrent
    if request.media_type == "tv":
        request.media_type = "102184"
    elif request.media_type == "movie":
        request.media_type = "102183"
    #Creation du regex
    regex = "^"
    if request.encoding is not None:
        regex = regex + "(?=.*" + request.encoding + ".*)"
    if request.resolution is not None:
        regex = regex + "(?=.*" + request.resolution + ".*)"
    #Creation et requêtage de l'url jackett
    baseURL = "http://"+request.host+"/api/v2.0/indexers/yggcookie/results/torznab/api?"
    getParametre={"apikey": request.apiKey, "t": "search", "cat": request.media_type, "q": request.query}
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
                        title=entry.title, category=request.media_type, size=entry.size, seeders=seeders, url=entry.link)
    return torrent
