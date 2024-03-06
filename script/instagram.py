import urllib.request
import json

from script.request_download import download_file


def insta_download(url, id_chat):
    try:
        with urllib.request.urlopen(f"https://instagram-videos.vercel.app/api/video?url={url}") as url:
            data = json.load(url)
            if data['status'] == "success":
                url_link = data['data']['videoUrl']
                download_file(url_link, f'db/video/{id_chat}.mp4') # bug!
                return True
            return False
    except Exception as e:
        return False
