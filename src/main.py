import os
from io import BytesIO
from shutil import copyfile

import cv2
import numpy as np
from PIL import ImageGrab
from pynput.keyboard import Controller, Listener
from skimage.metrics import structural_similarity
import configparser

config = configparser.ConfigParser()  # 创建对象
config.read("apex.conf", encoding="utf-8")

lg_file_path = config.get('conf', 'lg_file_path')
refresh_button = config.get('conf', 'refresh_button')

lua_suffix = '.lua'
image_path = lg_file_path + 'images\\'
lua_path = lg_file_path + 'lua\\'
common_file = lua_path + '通用' + lua_suffix
shake_file = lg_file_path + 'shake' + lua_suffix


def copy_file(source_path, target_path):
    op = os.path
    if isinstance(source_path, str):
        if op.exists(source_path):
            copyfile(source_path, target_path)
        else:
            print("源文件不存在")
            return


class CompareImage:
    @staticmethod
    def compare_image(img, path_image):
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        image_a = cv2.imdecode(np.frombuffer(buffer.getvalue(), dtype=np.uint8), cv2.IMREAD_COLOR)
        buffer.close()
        image_b = cv2.imdecode(np.fromfile(path_image, dtype=np.uint8), cv2.IMREAD_COLOR)
        gray_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
        gray_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)
        (score, diff) = structural_similarity(gray_a, gray_b, full=True)
        return score


keyboard = Controller()

compare_image = CompareImage()


# 点击按钮
def on_press(key):
    # print('{0} 被按下'.format(key))
    return


# 释放按钮，按esc按键会退出监听
def on_release(key):
    # print('{0} 被释放'.format(key))
    if not hasattr(key, 'name') and (key.char in refresh_button):
        score_temp = 0.00000000000000000000
        max_gun = ''
        img = ImageGrab.grab(bbox=(2093, 1281, 2275, 1332))
        for fileName in os.listdir(image_path):
            score = compare_image.compare_image(img, image_path + fileName)
            if score > score_temp:
                score_temp = score
                max_gun = fileName.split('.')[0]
        print("枪械: {}, 最大相似度: {}".format(max_gun, score_temp))
        if os.path.exists(lua_path + max_gun + lua_suffix):
            copy_file(lua_path + max_gun + lua_suffix, shake_file)
            print("已切换到: {}".format(max_gun))
        else:
            copy_file(common_file, shake_file)
            print("未找到: {}".format(max_gun))


# 创建监听
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
