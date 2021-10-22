import qbittorrentapi


def download(url, cat):
    qbt_client = qbittorrentapi.Client(
        host='https://dl.etur.fr', username='sam', password='usLw9QiXxQ23Dt', SIMPLE_RESPONSES=True)
    qbt_client.torrents_add(urls=url, category=cat)


# def getTorrentsInfos():
qbt_client = qbittorrentapi.Client(
    host='https://dl.etur.fr', username='sam', password='usLw9QiXxQ23Dt')