import feedparser
import requests
import re


class Torrent:
    def __init__(self, name, cat, size, seeders):
        self.name = name
        self.cat = cat
        self.size = size
        self.seeders = seeders


cat = "102183"
news_feed = feedparser.parse(
    'https://jk.etur.fr/api/v2.0/indexers/yggcookie/results/torznab/api?apikey=pfpk2qtgiik9dvctqxpk54txn58vyudf&t=search&cat=102183&q=Venom')
response = requests.get(
    "https://jk.etur.fr/api/v2.0/indexers/yggcookie/results/torznab/api?apikey=pfpk2qtgiik9dvctqxpk54txn58vyudf&t=search&cat=102183&q=Venom")
splited = response.text.split("<item>")
seed=splited[1].split("seeders")
seed=seed[1].split("\"")
nb = len(seed)
n = 0
r = {}
for entry in news_feed.entries:
    splited = response.text.split("<item>")
    seed=splited[n+1].split("seeders")
    seed=seed[1].split("\"")
    seed=seed[2]
    #print(nb)
    #if nb > n:
    r[n] = Torrent(entry.title, cat, entry.size, seed)
    print(" Name: "+r[n].name+" Size: "+r[n].size+" Seeders: "+r[n].seeders)
    n = n+1
    # print(f"{entry}")
