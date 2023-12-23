import re
import pytube
from pytube import Playlist
from pytube import YouTube
import os
import time
import pandas as pd
import lib.constant.globals as constant
import lib.function.common as common
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv(dotenv_path="../../env/learning.env", override=True)

youtube_genshin_impact = os.environ.get('youtube_genshin_impact')


def download_aother(link):
    try:
        video = YouTube(link)
        stream = video.streams.filter(only_audio=True).first()
        stream.download(filename=f"{video.title}.mp3")
        print("The video is downloaded in MP3")
    except KeyError:
        print("Unable to fetch video information. Please check the video URL or your network connection.")


def pytube_list(link):
    # Youtube video URL
    yt = YouTube(link)

    print("Title:", yt.title)
    print("Author:", yt.author)
    print("Published date:", yt.publish_date)
    print("Number of views:", yt.views)
    print("Length of video:", yt.length, "seconds")

    yt.streams.get_highest_resolution().download()
    print("Video successfullly downloaded from", link)


# Download
def main():
    print('Start Youtube Download')
    # chrome_options = webdriver.ChromeOptions()
    # prefs = {'profile.managed_default_content_settings.images': 2}
    # chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(youtube_genshin_impact)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'contents')))

    time.sleep(1)

    next_count = 0
    while next_count < 1:
        driver.execute_script(constant.PAPERS_SCROLL_JS)
        time.sleep(3.5)
        next_count += 1

    try:
        link_list = driver.find_elements(By.ID, 'video-title-link')
        for link in link_list:
            print(link.text)
            print(link.get_attribute('href'))
            pytube_list(link.get_attribute('href'))
    except:
        pass


def github_pytube():
    YouTube('https://youtu.be/2lAe1cqCOXo').streams.first().download()
    yt = YouTube('http://youtube.com/watch?v=2lAe1cqCOXo')
    yt.streams.get_highest_resolution().download()


if __name__ == '__main__':
    # main()
    #pytube_list('https://www.youtube.com/watch?v=qbwe6FZyTwk')
    github_pytube()