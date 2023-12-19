# Edge Example
import time
import os
import lib.constant.globals as constant
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

load_dotenv(dotenv_path="../../env/study.env", override=True)

edge_main_url = os.environ.get('edge_main_url')

"""
  You can click F12 from pages,that can get require element-id class and css (first floor element)
  Then: Imitate human operation of web pages
  """


def main():
    print(constant.MAIN_START)
    # Start driver: max_screen
    driver = webdriver.Edge()
    driver.get(edge_main_url)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'wrapper')))

    baidu_input = driver.find_element(By.ID, 'kw')

    # Keys are keyboard's contributions like Ctrl C/V/A/X/Z
    baidu_input.send_keys("test button")
    baidu_input.send_keys(Keys.SPACE)
    time.sleep(1)
    baidu_input.send_keys(Keys.CONTROL, 'a')
    time.sleep(1)
    baidu_input.send_keys(Keys.CONTROL, 'x')
    time.sleep(1)
    baidu_input.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)
    baidu_input.send_keys(Keys.ENTER)

    print(constant.MAIN_END)
    driver.quit()


if __name__ == '__main__':
    main()
