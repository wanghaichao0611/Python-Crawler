# Google learning
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

google_main_url = os.environ.get('google_main_url')


# Start Twitch
def main():
    print('Start Twitch')
    chrome_options = webdriver.ChromeOptions()
    prefs = {'profile.managed_default_content_settings.images': 2}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get(google_main_url)
    time.sleep(3)
    driver.execute_script(constant.PAPERS_SCROLL_JS)
    time.sleep(3)
    category_list = driver.find_elements(By.CSS_SELECTOR, '.ScCoreLink-sc-16kq0mq-0.eFqEFL.game-card__link.tw-link')

    url_list = set()
    for category in category_list:
        url_list.add(category.get_attribute('href'))

    print(len(category_list))
    pd_url = []
    pd_category = []
    pd_author_name = []
    pd_author_avatar_url = []
    pd_author_videos = []
    pd_split_category = []
    pd_online_url = []
    pd_title = []
    pd_save_screen = []
    pd_peoples = []
    for url in url_list:
        print(url)
        time.sleep(1)
        driver.get(url + '?sort=VIEWER_COUNT')
        time.sleep(3)
        driver.execute_script(constant.PAPERS_SCROLL_JS)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.Layout-sc-1xcs6mc-0.jivRFd')))
        article_list = driver.find_elements(By.CSS_SELECTOR, '.Layout-sc-1xcs6mc-0.jivRFd')
        for index in range(len(article_list)):
            if index > 3:
                pd_url.append(url)
                pd_category.append(url.split('/')[-1])
                print('index: ' + index.__str__())
                room = article_list[index].find_element(By.CSS_SELECTOR, '.Layout-sc-1xcs6mc-0.jnMKgW')
                author_link = room.find_element(By.CSS_SELECTOR,
                                                '.InjectLayout-sc-1i43xsx-0.cXFDOs.tw-image.tw-image-avatar')
                author_name = author_link.get_attribute('alt')
                author_url = author_link.get_attribute('src')
                room_category_list = room.find_elements(By.CSS_SELECTOR, '.ScTruncateText-sc-i3kjgq-0.ickTbV')
                split_category = ''
                for category_video in room_category_list:
                    split_category = split_category + category_video.text + ','

                print(
                    'author_name: ' + author_name + ' | author_url | ' + author_url + ' | split_category | ' + split_category)

                content = article_list[index].find_element(By.CSS_SELECTOR, '.ScTransformWrapper-sc-1wvuch4-1.iXjpwc')
                video_link = content.find_element(
                    By.CSS_SELECTOR, '.ScCoreLink-sc-16kq0mq-0.eFqEFL.preview-card-image-link.tw-link')
                online_url = video_link.get_attribute('href')
                video_user = video_link.find_element(By.CSS_SELECTOR, '.ScAspectRatio-sc-18km980-1.doeqbO.tw-aspect')
                img = video_user.find_element(By.CLASS_NAME, 'tw-image')
                title = img.get_attribute('alt')
                save_screen = img.get_attribute('src')
                peoples = video_link.find_element(By.CSS_SELECTOR, '.ScMediaCardStatWrapper-sc-anph5i-0'
                                                                   '.jRUNHm.tw-media-card-stat').text.split(' ')[0]
                print('online_url: ' + online_url + ' | title | ' + title
                      + '| save_screen | ' + save_screen + ' | peoples | ' + peoples)

                pd_author_name.append(author_name)
                pd_author_avatar_url.append(author_url)
                pd_author_videos.append('https://www.twitch.tv/' + author_name + '/videos')
                pd_split_category.append(split_category)
                pd_online_url.append(online_url)
                pd_title.append(title)
                pd_save_screen.append(save_screen)
                if peoples.endswith('万'):
                    pd_peoples.append(float(peoples.replace('万', '').strip()) * 10000)
                else:
                    pd_peoples.append(float(peoples.replace(',', '').strip()))

    excel = pd.DataFrame({
        'category_url': pd_url,
        'category': pd_category,
        'author_name': pd_author_name,
        'author_avatar_url': pd_author_avatar_url,
        'author_videos': pd_author_videos,
        'split_category': pd_split_category,
        'online_url': pd_online_url,
        'title': pd_title,
        'save_screen': pd_save_screen,
        'peoples': pd_peoples
    })
    # 写入excel
    excel.to_excel(r'F:\GitHubProject\Python-Crawler\out\google\Twitch.xlsx', index=True, header=True)


if __name__ == '__main__':
    main()
