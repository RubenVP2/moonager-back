from os import stat_result
import feedparser
from pydantic.main import BaseModel
import requests
import re
from typing import Optional


class TorrentRequest(BaseModel):
    query: str
    mediaType: str
    sizeMax: Optional[int] = 15000000000
    encoding: Optional[str] = "264"
    resolution: Optional[str] = "1080"


class TorrentFind(BaseModel):
    title: str
    category: str
    size: int
    seeders: int
    url: str


def findTorrent(request):
    regex = "^"
    if request.mediaType == "tv":
        request.mediaType = "102184"
    elif request.mediaType == "movie":
        request.mediaType = "102183"
    if request.encoding is not None:
        regex = regex+"(?=.*"+request.encoding+".*)"
    if request.resolution is not None:
        regex = regex+"(?=.*"+request.resolution+".*)"
    request.query = request.query.replace(" ", "+")
    url = "https://jk.etur.fr/api/v2.0/indexers/yggcookie/results/torznab/api?apikey=pfpk2qtgiik9dvctqxpk54txn58vyudf&t=search&cat=" + \
        request.mediaType+"&q="+request.query
    print(url)
    result = feedparser.parse(url)
    ResponseSeeders = requests.get(url)
    torrent = {}
    for index, entry in enumerate(result.entries):
        seeders = ResponseSeeders.text.split(
            "<item>")[index+1].split("seeders")[1].split("\"")[2]
        if len(entry) > index:
            if re.search(regex, entry.title, re.IGNORECASE):
                if int(entry.size) < int(request.sizeMax):
                    torrent[index] = TorrentFind(
                        title=entry.title, category=request.mediaType, size=entry.size, seeders=seeders, url=entry.link)
    return torrent


# request = TorrentRequest(query="Venom", mediaType="movie",
#                         encoding="x264", resolution="1080p", sizeMax="100000000000000000")
# print(findTorrent(request))
