# Reddit Genshin impact
import os
import time
import json
import lib.constant.globals as constant
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv(dotenv_path="../../env/learning.env", override=True)

reddit_genshin_impact_url = os.environ.get('reddit_genshin_impact_url')
reddit_into_file = os.environ.get('reddit_into_file')
scroll_index = os.environ.get('scroll_index')


# Start
def main():
    print('Start Reddit')
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
    driver.get(reddit_genshin_impact_url)
    time.sleep(1)

    next_count = 0
    while next_count < int(scroll_index):
        driver.execute_script(constant.PAPERS_SCROLL_JS)
        time.sleep(3.5)
        next_count += 1

    article_list = driver.find_elements(By.XPATH, "//article[@class='m-0']")
    print(len(article_list))

    data_list = []
    for article in article_list:
        a = article.find_element(By.CSS_SELECTOR, '.absolute.inset-0')
        data_list.append({'title_url': a.get_attribute('href'), 'title': a.get_attribute('aria-label')})

    for url in data_list:
        print('Downloading: ', url['title_url'])
        driver.get(url['title_url'])
        time.sleep(1.5)
        try:
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.md.text-14')))
            url['content'] = driver.find_element(By.CSS_SELECTOR, '.md.text-14').find_element(By.TAG_NAME, 'p').text
            print(url['content'])
        except:
            # pass
            with open('../../out/reddit/' + reddit_into_file, "w", encoding='utf-8') as json_list:
                json.dump(data_list, json_list)

    return data_list


# main
if __name__ == '__main__':
    print(reddit_genshin_impact_url)
    print(reddit_into_file)
    print(scroll_index)
    data_list = main()
    if len(data_list) > 0:
        with open('../../out/reddit/' + reddit_into_file, "w", encoding='utf-8') as json_list:
            json.dump(data_list, json_list)
