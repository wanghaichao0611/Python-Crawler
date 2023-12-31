import time
import json
import os
import lib.function.common as common
import lib.constant.globals as constant
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

load_dotenv(dotenv_path="../../env/learning.env", override=True)

twitch_user_videos = os.environ.get('twitch_user_videos')
twitch_user = os.environ.get('twitch_user')
twitch_user_out_path = os.environ.get('twitch_user_out_path')
twitch_video_path = os.environ.get('twitch_video_path')
twitch_mp4_path = os.environ.get('twitch_mp4_path')
twitch_720 = os.environ.get('twitch_720')


# get_author_information
def get_author_information():
    print('start twitch:')
    driver = webdriver.Chrome()
    driver.get(twitch_user_videos)
    driver.maximize_window()
    time.sleep(1)
    driver.execute_script(constant.PAPERS_SCROLL_JS)
    time.sleep(2)
    textarea = driver.find_elements(By.CSS_SELECTOR, '.Layout-sc-1xcs6mc-0.eFvOkl')
    data_list = []
    for text in textarea:
        img_link = text.find_element(By.TAG_NAME, 'img')
        img_title = img_link.get_attribute('title')
        img_src = img_link.get_attribute('src')
        if img_src.find(twitch_user) == -1:
            continue
        video_time = text.find_element(By.CSS_SELECTOR,
                                       '.ScMediaCardStatWrapper-sc-anph5i-0.jRUNHm.tw-media-card-stat').text
        print('video_author: ' + twitch_user)
        print('img_title: ' + img_title)
        print('img_src: ' + img_src)
        print('video_time: ' + video_time)
        array_src = img_src.split('/')
        print('split_front: ' + array_src[4])
        print('split_author: ' + array_src[5])
        array_time = video_time.split(':')
        count_second = 0
        if len(array_time) == 0:
            continue
        if len(array_time) == 1:
            count_second = int(array_time[0])
        if len(array_time) == 2:
            count_second = int(array_time[0]) * 60 + int(array_time[1])
        if len(array_time) == 3:
            count_second = int(array_time[0]) * 3600 + int(array_time[1]) * 60 + int(array_time[2])
        count_split = int(count_second / 8)
        print('count_second: ' + count_second.__str__())
        print('count_split: ' + count_split.__str__())

        data_list.append(
            {'video_author': twitch_user, 'img_title': img_title, 'img_src': img_src, 'video_time': video_time,
             'split_front': array_src[4], 'split_author': array_src[5], 'count_second': count_second,
             'count_split': count_split})

        if not os.path.exists(twitch_video_path + str(img_title)):
            os.makedirs(twitch_video_path + str(img_title))

        # break

    with open(twitch_user_out_path, "w", encoding='utf-8') as json_list:
        json.dump(data_list, json_list)

    return data_list


if __name__ == '__main__':
    common.clear_files_and_dirs(twitch_video_path)
    data_list = get_author_information()
