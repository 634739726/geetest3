import cv2
import numpy as np
from PIL import Image


def a():
    """
    识别geetest的缺口
    """
    r = cv2.imread('33.png')
    d = cv2.imread('ii2.png')
    i = r - d
    i = cv2.cvtColor(i, cv2.COLOR_RGB2GRAY)
    i = cv2.inRange(i, np.array([20]), np.array(200))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    i = cv2.morphologyEx(i, cv2.MORPH_OPEN, kernel, iterations=2)
    print(i)
    cv2.imwrite('1.png', i)


def b():
    """
    获取浏览器里面的图片
    """
    j1 = cv2.imread('1555140674.5230615.png')
    j2 = j1[329:329 + 160, 830:830 + 260]
    cv2.imwrite('n1.png', j2)


def c():
    """
    上下：把2张图片拼成完整的一张图
    """
    u1 = cv2.imread('n1.png')
    u1 = u1[:80, :]
    cv2.imwrite('u1.png', u1)
    u2 = cv2.imread('n2.png')
    u2 = u2[80:160, :]
    cv2.imwrite('u2.png', u2)
    i = Image.open('u2.png')
    j = Image.open('u1.png')
    i1 = Image.new(i.mode, (260, 160))
    i1.paste(j)
    i1.paste(i, (0, 80))
    i1.save('v5.png')


def d():
    """
    左右：把2张图片拼成完整的一张图
    """
    u1 = cv2.imread('n1.png')
    u1 = u1[:, :130]
    cv2.imwrite('u1.png', u1)
    u2 = cv2.imread('n2.png')
    u2 = u2[:, 130:]
    cv2.imwrite('u2.png', u2)
    j = Image.open('u1.png')
    i = Image.open('u2.png')
    i1 = Image.new(i.mode, (260, 160))
    i1.paste(j)
    i1.paste(i, (130, 0))
    i1.save('v6.png')


# d()
