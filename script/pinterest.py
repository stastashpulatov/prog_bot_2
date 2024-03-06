'''
Pinterest video downloader
Made by Harshit
'''
import requests
from bs4 import BeautifulSoup
from os import system
import re
from script.request_download import download_file


system("cls")


def pint_download(page_url, id_chat):
    if ("https://pin.it/" in page_url):  # pin url short check
        t_body = requests.get(page_url)
        if (t_body.status_code != 200):
            return False
        soup = BeautifulSoup(t_body.content, "html.parser")
        href_link = (soup.find("link", rel="alternate"))['href']
        match = re.search('url=(.*?)&', href_link)
        page_url = match.group(1)  # update page url

    body = requests.get(page_url)  # GET response from url
    if (body.status_code != 200):  # checks status code
        return False
    else:
        soup = BeautifulSoup(body.content, "html.parser")  # parsing the content
        ''' extracting the url
        <video
            autoplay="" class="hwa kVc MIw L4E"
            src="https://v1.pinimg.com/videos/mc/hls/......m3u8"
            ....
        ></video>
        '''
        extract_url = (soup.find("video", class_="hwa kVc MIw L4E"))['src']
        convert_url = extract_url.replace("hls", "720p").replace("m3u8", "mp4")
        download_file(convert_url, f'db/video/{id_chat}.mp4')
        return True
