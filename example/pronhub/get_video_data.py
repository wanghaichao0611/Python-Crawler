import time
import json
import requests
from dotenv import load_dotenv
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

load_dotenv(dotenv_path="../../env/learning.env", override=True)


def main():
    driver = webdriver.Chrome()
    driver.get('https://cn.pornhub.com/view_video.php?viewkey=654b113fcd1e5')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    thu = soup.findAll('script', {'type': 'text/javascript'})[17]
    print(thu)
    filtered_scripts = [s.string for s in thu if "mediaDefinitions" in s.string]
    text = filtered_scripts.__str__().split('= ')[1]
    text_json = text[text.index('{'):text.rindex('}') + 1].replace('\\', '')
    data = text_json[text_json.find('"mediaDefinitions":') + 19:text_json.find('"isVertical":') - 1]
    print(data)
    url = json.loads(data)[4]
    video_url = str(url['videoUrl']).replace('master.m3u8', 'seg-140-f1-v1-a1.ts')
    print(video_url)
    response = requests.get(video_url)
    if response.status_code == 200:
        with open('140.ts', 'wb') as r:
            r.write(response.content)


if __name__ == '__main__':
    main()
