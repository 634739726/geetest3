import random
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import cv2
import numpy as np


class Sele:
    def __init__(self):
        opt = webdriver.ChromeOptions()
        opt.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(options=opt)
        self.mapping = ['./origin_img/v1.png', './origin_img/v2.png',
                        './origin_img/v3.png', './origin_img/v4.png',
                        './origin_img/v5.png', './origin_img/v6.png']
        self.error = 0

    def save_screenshot(self):
        WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_class_name('geetest_canvas_bg'))
        # 等待图片完全加载
        time.sleep(2)
        res_geetest3_picture = self.driver.find_element_by_class_name('geetest_canvas_bg').location
        res_slider_button = self.driver.find_element_by_class_name('geetest_slider_button').location
        self.driver.save_screenshot('screen.png')
        x, y = res_geetest3_picture["x"], res_geetest3_picture["y"]
        x2, y2 = res_slider_button["x"], res_slider_button["y"]
        self.error = x - x2
        # print(x, y, x2, y2)
        return self.get_verify_picture(x, y)

    def get_verify_picture(self, x, y):
        img = cv2.imread('screen.png')
        geetest3 = img[y:y + 160, x:x + 260]
        cv2.imwrite('geetest3.png', geetest3)
        return self.recognition('geetest3.png')

    def recognition(self, geetest3):
        """
        识别geetest的缺口
        """
        geetest3_img = cv2.imread(geetest3)
        # 找到相似对在50%以上的母图(因为截图并没有除了缺口就完全按原图来)
        for img in self.mapping:
            parent_img = cv2.imread(img)
            pixel_3_chanel = abs(parent_img - geetest3_img)
            n = pixel_3_chanel.flatten().size
            count = np.sum(abs(parent_img - geetest3_img).flatten() > 10)  # 阙值暂设为10
            if count / n <= 0.5:
                break
        pixel_3_chanel[:, :58] = np.zeros(pixel_3_chanel[:, :58].shape)  # 阙值58：过滤我没有处理的最左边的滑块带来的不同
        img = cv2.cvtColor(pixel_3_chanel, cv2.COLOR_RGB2GRAY)
        img = cv2.inRange(img, np.array([20]), np.array(200))
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=3)
        # cv2.imshow("img", img)
        # cv2.waitKey(0)
        # print(i)
        return self.find_contours(geetest3_img, img)

    def find_contours(self, geetest3_img, img):
        move_x = []
        # 找轮廓
        contours_img, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # 画一下轮廓
        # cv2.drawContours(geetest3_img, contours, -1, (0, 0, 255), 2)
        # cv2.imshow("img", geetest3_img)
        # cv2.waitKey(0)
        # cv2.imwrite('geetest3_contours.png', geetest3_img)
        # print(contours)
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if 35 <= w <= 90 and 35 <= h <= 90:
                # cv2.rectangle(geetest3_img, (x, y), (x + w, y + h), (255, 0, 255), 1)
                # cv2.imshow("img2", geetest3_img)
                # cv2.waitKey(0)
                # cv2.imwrite('geetest3_gap.png', geetest3_img)
                move_x.append(x+1)
        return move_x

    def simulation_track(self, move_x):
        track = []
        current = 0
        t = 0.2
        v = 0
        beyond = random.random() < 1
        print('beyond', beyond)
        while True:
            if current < move_x * 3/4:
                a = 10
            else:
                a = -15
            v0 = v
            v = v0 + a * t
            move = v0 * t + 1 / 2 * a * t * t
            current += round(move)
            track.append(round(move))
            if current > move_x:
                overflow = current - move_x
                track[-1] = track[-1] - overflow
                break
        if beyond:
            beyond_x = random.randint(1, 3)
            track.append(beyond_x)
            track.append(-beyond_x)
        track.sort(reverse=True)
        print('track:', sum(track), track)

        return track

    def move_slider(self, move_x):
        track = self.simulation_track(move_x - self.error)
        move_element = self.driver.find_element_by_class_name('geetest_slider_button')
        action = ActionChains(self.driver)
        action.click_and_hold(move_element).perform()
        time.sleep(0.3)
        for i, x in enumerate(track):
            action.move_by_offset(x, 0).perform()
            if i < 1 / 3 * len(track):
                time.sleep(0.01)
            if i < 1 / 2 * len(track):
                time.sleep(0.02)
            elif i < 3 / 4 * len(track):
                time.sleep(0.04)
            elif i < 5 / 6 * len(track):
                time.sleep(0.08)
            else:
                time.sleep(0.1)
            action = ActionChains(self.driver)

        time.sleep(0.5)
        action.release().perform()
        time.sleep(3)
        try:
            self.driver.find_element_by_class_name('geetest_slider_button')
            return 0
        except:
            return 1

    def main(self):
        self.driver.get('https://passport.zhaopin.com/org/login')
        self.driver.find_element_by_xpath('//*[@id="loginName"]').send_keys('1531027777')
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys('dsf')
        self.driver.find_element_by_xpath('//*[@id="loginbutton"]').click()
        while True:
            move_x = self.save_screenshot()
            if move_x:
                break
            self.driver.find_element_by_class_name('geetest_refresh_1').click()

        print('move_x:', move_x)
        for x in move_x:
            is_success = self.move_slider(x)
            if is_success:
                break
        self.driver.quit()


if __name__ == '__main__':
    Sele().main()
