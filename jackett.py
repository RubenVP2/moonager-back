import feedparser
import requests
import re

from models import TorrentFind


def find_torrent(request):
    """
    Com à rajouter
    """
    regex = "^"
    if request.mediaType == "tv":
        request.mediaType = "102184"
    elif request.mediaType == "movie":
        request.mediaType = "102183"
    if request.encoding is not None:
        regex = regex + "(?=.*" + request.encoding + ".*)"
    if request.resolution is not None:
        regex = regex + "(?=.*" + request.resolution + ".*)"
    request.query = request.query.replace(" ", "+")
    url = "https://jk.etur.fr/api/v2.0/indexers/yggcookie/results/torznab/api?apikey=pfpk2qtgiik9dvctqxpk54txn58vyudf" \
          "&t=search&cat=" + \
          request.mediaType + "&q=" + request.query
    result = feedparser.parse(url)
    response_seeders = requests.get(url)
    torrent = {}
    for index, entry in enumerate(result.entries):
        seeders = response_seeders.text.split(
            "<item>")[index + 1].split("seeders")[1].split("\"")[2]
        if len(entry) > index:
            if re.search(regex, entry.title, re.IGNORECASE):
                if int(entry.size) < int(request.sizeMax):
                    torrent[index] = TorrentFind(
                        title=entry.title, category=request.mediaType, size=entry.size, seeders=seeders, url=entry.link)
    return torrent
