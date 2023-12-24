import time
import json
import requests
import os
from selenium import webdriver
import multiprocessing as mp
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv(dotenv_path="../../env/learning.env", override=True)

av_fc2_url = os.environ.get('av_fc2_url')
av_main_cn = os.environ.get('av_main_cn')
av_video_path = os.environ.get('av_video_path')
av_picture = os.environ.get('av_picture')


# read local json file
def read_data_list(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)


def download_ts(download_url, write_url):
    response = requests.get(download_url)
    if response.status_code == 200:
        with open(write_url, 'wb') as r:
            r.write(response.content)


def main():
    # json_list = read_data_list('../../out/missav/fc2/fc2.json')
    chrome_options = webdriver.ChromeOptions()

    # prohibit images loading
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2,
            'javascript': 2
        }
    }
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(av_fc2_url)
    driver.maximize_window()
    time.sleep(1)

    data_list = []
    for data in read_data_list('../../out/missav/fc2/fc2.json'):
        driver.get(av_main_cn + data['video_id'])
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        thu = str(soup.findAll('script', {'type': 'text/javascript'})[2])
        index = thu.find('urls')
        http = thu[index:index + 80].replace('\\', '').split('/')
        url = http[0][8:] + '//' + http[2] + '/' + http[3] + '/' + av_picture
        print(url)
        count = 0
        count_split = data['count_split']
        while count < count_split:
            name = count
            next = len(str(count_split)) - len(str(count))
            if next > 0:
                if next == 1:
                    name = '0' + str(count)
                if next == 2:
                    name = '00' + str(count)
                if next == 3:
                    name = '000' + str(count)
            download_url = url + '/video' + str(count) + '.ts'
            write_url = av_video_path + data['video_id'] + '//' + str(name) + '.ts'
            data_list.append((download_url, write_url))
            count += 1

    return data_list


if __name__ == '__main__':
    data_list = main()
    if len(data_list) > 0:
        with open('../../out/missav/fc2/fc2_download.json', "w", encoding='utf-8') as json_list:
            json.dump(data_list, json_list)
        with mp.Pool(mp.cpu_count()) as p:
            p.starmap(download_ts, data_list)
