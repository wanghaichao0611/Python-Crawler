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

# start_number需要人为指定当天可选择的天数,截取字符串去出0，走load_dotenv
start_number = '16'
last_nummer = '29'


def main():
    print('start flyway:')
    chrome_options = webdriver.ChromeOptions()

    # prohibit images loading
    prefs = {
        'profile.default_content_setting_values': {
            # 'images': 2,
            # 'javascript': 2
        }
    }
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get('https://www.flyadeal.com/')

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'router-container')))

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'idShowDepartureAirport')))

    time_click = driver.find_element(By.CLASS_NAME, 'calender_icon.ng-tns-c112-2')
    time_click.click()

    time_list = driver.find_elements(By.XPATH, "//div[@role='gridcell']")
    for date in time_list:
        span = date.find_elements(By.TAG_NAME, 'span')
        if len(span) > 0:
            index = span[0].text
            print('day_date: ' + index)
            if index == start_number:
                span[0].click()
                continue
            if index == last_nummer:
                span[0].click()
                break

    price_list = driver.find_elements(By.CLASS_NAME, 'increase_count')
    for price in price_list:
        price.click()
    select = driver.find_element(By.ID, 'idShowDepartureAirport')
    select.click()
    time.sleep(2)
    list_size = driver.find_elements(By.CLASS_NAME, 'mat-option-text')[1:]
    k = 0
    while k < len(list_size):
        data = driver.find_elements(By.CLASS_NAME, 'mat-option-text')[1:][k]
        print('from: ' + data.find_element(By.CLASS_NAME, 'station-name').text)
        print('fromDx: ' + data.find_element(By.CLASS_NAME, 'state_code_auto').text)
        time.sleep(1)
        data.click()
        inner_list = driver.find_elements(By.CLASS_NAME, 'mat-option-text')[1:]
        for inner in inner_list:
            print('to: ' + inner.find_element(By.CLASS_NAME, 'station-name').text)
            print('toXx: ' + inner.find_element(By.CLASS_NAME, 'state_code_auto').text)
        select.click()
        time.sleep(1)
        k += 1

    search_button = driver.find_element(By.CLASS_NAME, 'col-md-3.lets_fly_button_updated').find_element(By.TAG_NAME,
                                                                                                        'button')
    print(search_button.text)
    search_button.click()
    time.sleep(3)


if __name__ == '__main__':
    main()
