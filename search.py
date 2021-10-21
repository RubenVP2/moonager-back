import feedparser
import requests
import re


class Torrent:
    def __init__(self, name, cat, size, seeders, url, enc, res):
        self.name = name
        self.cat = cat
        self.size = size
        self.seeders = seeders
        self.url = url
        self.enc = enc
        self.res = res

def findTorrent(q, cat, enc, res, sizeMax):
    if cat == "tv":
        cat = "102184"
    elif cat == "movie":
        cat = "102183"
    if enc is None:
        enc=""
    if res is None:
        res=""
    if sizeMax is None:
        sizeMax=""
    q = q.replace(" ", "+")
    url = "https://jk.etur.fr/api/v2.0/indexers/yggcookie/results/torznab/api?apikey=pfpk2qtgiik9dvctqxpk54txn58vyudf&t=search&cat="+cat+"&q="+q
    news_feed = feedparser.parse(url)
    n, t = 0, {}
    response = requests.get(url)
    for entry in news_feed.entries:
        seed = response.text.split("<item>")[n+1].split("seeders")[1].split("\"")
        if len(seed) > n:
            if re.search(enc, entry.title):
                if re.search(res, entry.title):
                    if int(entry.size) < int(sizeMax):
                        t = Torrent(entry.title, cat, entry.size, seed[2], entry.link, enc, res)
                            #print(" Name: "+t.name+" Size: "+t.size+" Seeders: "+t.seeders+" URL: "+t.url)
        n = n+1
    return t

#findTorrent("Venom", "movie", "x264", "1080p", "100000000000000000")