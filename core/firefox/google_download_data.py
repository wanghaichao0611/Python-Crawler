import os
import time
import zipfile
import requests
import pymysql
import pdfkit
import lib.function.common as common
import lib.constant.globals as constant
from model.entity import PageCard
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

WKHTMLTOPDF_PATH = '../../bin/wkhtmltopdf.exe'
load_dotenv(dotenv_path="../../env/study.env", override=True)

firefox_output_folder = os.environ.get('firefox_output_folder')
github_master_download_end_url = os.environ.get('github_master_download_end_url')


# get data from mysql
def get_data_from_db():
    conn = common.get_mysql_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    data_list = []
    try:
        cursor.execute(constant.SELECT_PAPERS_WINT_CODE_SQL)
        data_list = PageCard.db_json_list_to_entity(cursor.fetchall())
        return data_list
    except Exception as err:
        print(err)
    finally:
        cursor.close()
        conn.close()
        return data_list


# download pdf and github-zip-codes
def get_download_pdf_github(data_list):
    print('Download Start: ---------')
    # only google can open pdf outside
    down_load_dir = os.path.abspath("../../out/firefox")
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    prefs = {
        "download.default_directory": down_load_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    }
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    try:
        for data in data_list:
            catalog = str(data.title).split(':')[0].strip()
            zip_file_path = firefox_output_folder + catalog
            print(zip_file_path)
            if not os.path.exists(zip_file_path):
                os.makedirs(zip_file_path)
            driver.get(data.pdf_url)
            time.sleep(2)
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'paper-abstract')))
            pdf_link = driver.find_element(By.CSS_SELECTOR, '.badge.badge-light ')
            pdf_url = pdf_link.get_attribute('href')
            print(pdf_url)
            # change real pdf url for selecting repository
            data.pdf_url = pdf_url
            driver.get(pdf_url)
            # response_pdf = requests.get(pdf_url)
            # print(response_pdf)
            # driver.get(pdf_url)
            # try:
            #     soup = BeautifulSoup(driver.page_source, 'html.parser')
            #     modified_html = f"""
            #            <html>
            #            <head>
            #                <style>
            #                    font-family: Arial, sans-serif;
            #                    {common.getStyleCss()}
            #                </style>
            #            </head>
            #            <body>
            #                {str(soup)}
            #            </body>
            #            </html>
            #        """
            #
            #     path_wkhtmltopdf = WKHTMLTOPDF_PATH
            #     pdfkit.from_string(modified_html, zip_file_path + '/' + catalog + '.pdf',
            #                        configuration=pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf),
            #                        options={'encoding': 'utf-8'})
            # except:
            #     print('Download papers pdf failed')
            print(data.github_url + github_master_download_end_url)
            print('Download github-master-zip loading ......')
            response_github = requests.get(data.github_url + github_master_download_end_url)
            if response_github.status_code == 200:
                print('decompressed ZIP file loading ......')
                temp_filename = 'master.zip'
                try:
                    with open(temp_filename, 'wb') as file:
                        file.write(response_github.content)
                    with zipfile.ZipFile(temp_filename, 'r') as zip_ref:
                        zip_ref.extractall(zip_file_path)
                    print("Successfully decompressed ZIP file")
                except Exception as e:
                    print("An error occurred during the decompression process: ", str(e))
            else:
                print("Unable to connect to server or request failed")
    except Exception as err:
        print(err)
    finally:
        driver.quit()


if __name__ == '__main__':
    common.clear_files(firefox_output_folder)
    common.remove_dir(firefox_output_folder)
    data_list = get_data_from_db()
    if len(data_list) > 0:
        get_download_pdf_github(data_list)
        common.truncate_and_insert_info_mysql(data_list)