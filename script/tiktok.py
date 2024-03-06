from tiktok_downloader import snaptik


def tiktok_download(url, id_chat):
    try:
        d = snaptik(url)
        d[0].download(f'db/video/{id_chat}.mp4')
        return True
    except Exception as e:
        return False
