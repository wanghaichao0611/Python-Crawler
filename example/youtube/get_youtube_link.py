import json
import os
import time
import lib.constant.globals as constant
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv(dotenv_path="../../env/learning.env", override=True)

youtube_user_url = os.environ.get('youtube_user_url')
youtube_out_json = os.environ.get('youtube_out_json')


def write_into_json(data_list):
    with open('../../out/youtube/' + youtube_out_json, "w", encoding='utf-8') as json_list:
        json.dump(data_list, json_list)


# Download
def main():
    print('Start Youtube Download')
    # chrome_options = webdriver.ChromeOptions()
    # prefs = {'profile.managed_default_content_settings.images': 2}
    # chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(youtube_user_url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'contents')))

    time.sleep(1)

    next_count = 0
    while next_count < 5:
        driver.execute_script(constant.PAPERS_SCROLL_JS)
        time.sleep(3)
        next_count += 1

    data_list = []
    try:
        link_list = driver.find_elements(By.ID, 'video-title-link')
        for link in link_list:
            print(link.text)
            print(link.get_attribute('href'))
            data_list.append((link.text, link.get_attribute('href')))

    except:
        # pass
        write_into_json(data_list)

    write_into_json(data_list)


if __name__ == '__main__':
    main()
