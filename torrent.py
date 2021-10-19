import qbittorrentapi

def test_dl_billie(tUrl):
    qbt_client = qbittorrentapi.Client(host='https://dl.etur.fr', username='sam', password='usLw9QiXxQ23Dt', SIMPLE_RESPONSES=True)

    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    tUrl="https://jk.etur.fr/dl/yggcookie/?jackett_apikey=pfpk2qtgiik9dvctqxpk54txn58vyudf&amp;path=Q2ZESjhGcW9MdThZZ2xsRGh3THRaeXlqakxGa0MxRUV1NWdFN1kxUm1IT2x2XzhhV1BBc212WTRlYWR0ajIzSGh4S2RWU0h5dFBENGxfY1JfZWFYblEtcE9LQ3NPZ1pVVm9ack1WdVhGVjgtR21sNjJnTWs1dnZYLUpnODVWRklBVENTVlZ5bDVDZE5BaG1OMkJ2M2g1VVN5SjlGbHByM1FIRC10aVlRaTdzVXpVYzVHNDVKbk5RdHloLThkU3N3WFl0dVJ3&amp;file=Billie+Eilish+-+Happier+Than+Ever+(Explicit)+-+(2021)+(Hi-Res)+(FLAC+WEB)+(24+bit+-+44.1+kHz)"
    print(f'qBittorrent: {qbt_client.app.version}')
    qbt_client.torrents_add(urls=tUrl,category="musiques")

def test_rm_all():
    qbt_client = qbittorrentapi.Client(host='https://dl.etur.fr', username='sam', password='usLw9QiXxQ23Dt')

    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    for qbt_client.torrent in qbt_client.torrents_info():
        qbt_client.torrents_delete(delete_files=True, torrent_hashes=qbt_client.torrent.hash)