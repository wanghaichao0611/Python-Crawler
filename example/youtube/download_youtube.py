import json
import os
import multiprocessing as mp
from pytube import YouTube
from dotenv import load_dotenv

load_dotenv(dotenv_path="../../env/learning.env", override=True)

youtube_out_json = os.environ.get('youtube_out_json')
youtube_out_file = os.environ.get('youtube_out_file')


def read_data_list(youtube_out_json):
    with open('../../out/youtube/' + youtube_out_json, 'r') as f:
        return json.load(f)


# Mp3
def download_mp3(link):
    try:
        video = YouTube(link)
        stream = video.streams.filter(only_audio=True).first()
        stream.download(filename=f"{video.title}.mp3")
        print("The video is downloaded in MP3")
    except KeyError:
        print("Unable to fetch video information. Please check the video URL or your network connection.")


def main(title, link):
    try:
        # Youtube video URL
        yt = YouTube(link)

        print("Title: ", yt.title)
        print("Author: ", yt.author)
        print("Published date: ", yt.publish_date)
        print("Number of views: ", yt.views)
        print("Length of video: ", yt.length, "seconds")
        yt.streams.get_highest_resolution().download(youtube_out_file)
        print("The Video downloaded successfully: ", link)
    except:
        pass


if __name__ == '__main__':
    link_list = read_data_list(youtube_out_json)

    with mp.Pool(mp.cpu_count()) as p:
        p.starmap(main, link_list)
