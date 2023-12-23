# FieFox learning
import os
import time
import lib.constant.globals as constant
import lib.function.common as common
from model.entity import PageCard
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv(dotenv_path="../../env/learning.env", override=True)

firefox_main_url = os.environ.get('firefox_main_url')


# get data list from page url
def get_data_list_from_page():
    driver = webdriver.Firefox()
    card_list = []
    try:
        print(constant.MAIN_START)
        # 1. Start driver
        driver.get(firefox_main_url)
        driver.maximize_window()
        next_count = 0
        while next_count < 10:
            driver.execute_script(constant.PAPERS_SCROLL_JS)
            time.sleep(3)
            next_count += 1

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'home-page')))
        cards = driver.find_elements(By.CSS_SELECTOR, '.col-lg-9.item-col')

        # Get card-element from page
        for page in cards:
            card_left = page.find_element(By.CSS_SELECTOR, '.col-lg-9.item-content')
            card_right = page.find_element(By.CSS_SELECTOR, '.col-lg-3.item-interact.text-center')
            title = card_left.find_element(By.TAG_NAME, 'a')
            print('title: ' + title.text)
            pdf_link = card_right.find_element(By.CSS_SELECTOR, '.badge.badge-light ')
            paper_url = pdf_link.get_attribute('href')
            content = card_left.find_element(By.CLASS_NAME, 'item-strip-abstract').text
            star = card_right.find_element(By.CSS_SELECTOR, '.badge.badge-secondary').text
            print('paper_url: ' + paper_url)
            author = card_left.find_element(By.CLASS_NAME, 'author-section')
            github_link = author.find_element(By.CLASS_NAME, 'item-github-link').find_element(By.TAG_NAME, 'a')
            github_url = github_link.get_attribute('href')
            print('github_url:' + github_url)
            date_ec = author.find_elements(By.CSS_SELECTOR, '.author-name-text.item-date-pub')
            if len(date_ec) != 0:
                date = date_ec[0].text
            else:
                date = author.find_element(By.CLASS_NAME, 'item-conference-link').find_element(By.TAG_NAME, 'a').text

            card_list.append(
                PageCard(common.gen_uuid(), title.text, content, star, paper_url, None, github_url, date,
                         constant.NOW_TIME))
    except Exception as err:
        print(err)
    finally:
        driver.quit()
        print(constant.MAIN_END)
        return card_list


if __name__ == '__main__':
    print('start: get data from page url')
    data_list = get_data_list_from_page()
    # Insert into mysql
    if len(data_list) > 0:
        print('start: INSET_PAPERS_WINT_CODE_SQL')
        common.truncate_and_insert_info_mysql(data_list)
