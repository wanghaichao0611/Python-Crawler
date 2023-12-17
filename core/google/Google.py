# Google Example
import time
from selenium import webdriver


# Start
def main():
    print('start ')
    # 1. Start driver
    drive = webdriver.Chrome()
    drive.get('https://www.baidu.com/')
    """
    2. You can click F12 from pages,that can get require element-id class and css. Then: Imitate human operation of web pages
    """

    time.sleep(3)
    drive.quit()


if __name__ == '__main__':
    main()
