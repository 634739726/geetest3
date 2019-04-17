import time
from urllib.parse import *
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import numpy as np


class AA:
    def __init__(self):
        opt = webdriver.ChromeOptions()
        opt.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(options=opt)

    def main(self):
        self.driver.get('https://passport.zhaopin.com/org/login')
        self.driver.find_element_by_xpath('//*[@id="loginName"]').send_keys('1531027777')
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys('dsf')
        self.driver.find_element_by_xpath('//*[@id="loginbutton"]').click()
        time.sleep(1)
        res = self.driver.find_element_by_class_name('geetest_canvas_bg')
        print(res.location)
        while True:
            input()
            a = str(time.time())
            filename = "./" + a + '.png'
            self.driver.save_screenshot(filename)

        self.driver.quit()


if __name__ == '__main__':
    AA().main()