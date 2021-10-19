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


def findTorrent(q, cat, enc, res):
    if cat == "tv":
        cat = "102184"
    elif cat == "movie":
        cat = "102183"

    q = q.replace(" ", "+")
    url = "https://jk.etur.fr/api/v2.0/indexers/yggcookie/results/torznab/api?apikey=pfpk2qtgiik9dvctqxpk54txn58vyudf&t=search&cat="+cat+"&q="+q
    print("Start", url)
    # print(url)
    news_feed = feedparser.parse(url)
    n = 0
    t = {}
    response = requests.get(url)
    for entry in news_feed.entries:
        seed = response.text.split(
            "<item>")[n+1].split("seeders")[1].split("\"")
        if len(seed) > n:
            if re.search(enc, entry.title):
                if re.search(res, entry.title):
                    t = Torrent(entry.title, cat, entry.size,
                                seed[2], entry.link, enc, res)
                    #print(" Name: "+t.name+" Size: "+t.size+" Seeders: "+t.seeders+" URL: "+t.url)
        n = n+1
    # print(t.url)

    return t
