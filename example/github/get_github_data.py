import time
import json
import os
import urllib
from urllib import parse
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

load_dotenv(dotenv_path="../../env/learning.env", override=True)

github_select_list = os.environ.get('github_select_list')
github_most_star_link = os.environ.get('github_most_star_link')
github_select_page_index = os.environ.get('github_select_page_index')


def convert_links():
    url_list = []
    for select in github_select_list.split(','):
        page_index = 1
        while page_index <= int(github_select_page_index):
            url_list.append(github_most_star_link + urllib.parse.quote(select) + '&p=' + page_index.__str__())
            page_index += 1
    return url_list


def main(url_list):
    print('start github:')
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
    driver.maximize_window()
    time.sleep(1)
    data_list = []
    for url in url_list:
        print('button url: ' + url)
        driver.get(url)
        time.sleep(2)
        title_link = driver.find_elements(By.CSS_SELECTOR, '.Box-sc-g0xbh4-0.bBwPjs.search-title')
        for link in title_link:
            title = link.find_element(By.TAG_NAME, 'a').get_attribute('href')
            title_link = link.find_element(By.TAG_NAME, 'span').text
            print('title: ' + title)
            print('title_link: ' + title_link)
            data_list.append((url, title, title_link))

    with open('../../out/github/github_select.json', "w", encoding='utf-8') as json_list:
        json.dump(data_list, json_list)


if __name__ == '__main__':
    main(convert_links())
