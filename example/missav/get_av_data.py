import time
import json
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

load_dotenv(dotenv_path="../../env/learning.env", override=True)

av_fc2_url = os.environ.get('av_fc2_url')
av_video_path = os.environ.get('av_video_path')


# clear files and dirs
def clear_files(folder_path):
    try:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)

        for root, dirs, files in os.walk(folder_path):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                os.rmdir(dir_path)
        print(f"success: {folder_path}")
    except Exception as e:
        print(f"{folder_path} error：{str(e)}")


def main():
    print('out_path:' + str(av_video_path))
    chrome_options = webdriver.ChromeOptions()

    # prohibit images loading
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2,
            # 'javascript': 2
        }
    }
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(av_fc2_url)
    driver.maximize_window()
    time.sleep(2)
    # wait = WebDriverWait(driver, 10)
    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.grid.grid-cols-2.md:grid-cols-3.xl:grid-cols-4.gap-5')))

    data_list = driver.find_elements(By.CSS_SELECTOR, '.thumbnail.group')

    get_json_list = []
    for data in data_list:
        video_content = data.find_element(By.CSS_SELECTOR, '.my-2.text-sm.text-nord4.truncate').find_element(
            By.TAG_NAME, 'a')
        video_text = video_content.text.split(' ')
        video_id = video_text[0].strip()
        video_title = video_text[1]
        video_online_url = video_content.get_attribute('href')
        print('video_id: ' + video_id)
        print('video_title: ' + video_title)
        video_main_id = data.find_element(By.TAG_NAME, 'video').get_attribute('id').strip()[8:]
        print('video_main_id: ' + video_main_id)
        video_time = data.find_element(By.CSS_SELECTOR, '.absolute.bottom-1.right-1.rounded-lg.px-2.py-1.text-xs.'
                                                        'text-nord5.bg-gray-800.bg-opacity-75').text
        print('video_time: ' + video_time)
        print('video_online_url: ' + video_online_url)

        split_time = video_time.split(':')
        count_second = int(split_time[0]) * 3600 + int(split_time[1]) * 60 + int(split_time[2])
        count_split = int(count_second / 4)

        print('count_second: ' + count_second.__str__())
        print('count_split: ' + count_split.__str__())

        if not os.path.exists(av_video_path + str(video_id)):
            os.makedirs(av_video_path + str(video_id))

        get_json_list.append({'video_id': video_id, 'video_title: ': video_title, 'video_main_id: ': video_main_id,
                              'video_next_id: ': 'next', 'video_time: ': video_time,
                              'video_online_url: ': video_online_url,
                              'count_second': count_second, 'count_split': count_split})

    with open('../../out/missav/fc2/fc2.json', "w", encoding='utf-8') as json_list:
        json.dump(get_json_list, json_list)


if __name__ == '__main__':
    clear_files(av_video_path)
    main()
