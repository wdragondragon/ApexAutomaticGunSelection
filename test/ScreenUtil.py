import os

from PIL import ImageGrab

from LogWindow import LogWindow
from test import ConfigReader


class SelectGun:
    def __init__(self, bbox, base_file_path, resolution_path):
        super().__init__()
        self.on_key_map = dict()
        self.bbox = bbox
        self.image_path = base_file_path + 'images\\' + resolution_path
        self.select_gun_sign = False
        self.current_gun = ''
        self.current_gun_config = dict()

    def select_gun(self):
        if self.select_gun_sign:
            return
        self.select_gun_sign = True
        score_temp = 0.00000000000000000000
        img = ImageGrab.grab(bbox=self.bbox)
        gun_temp = ''
        for fileName in os.listdir(self.image_path):
            from Tools import Tools
            score = Tools.compare_image(img, self.image_path + fileName)
            if score > score_temp:
                score_temp = score
                gun_temp = fileName.split('.')[0]
            if score_temp > 0.9:
                break
        if gun_temp == self.current_gun:
            LogWindow().print_log("当前枪械已经是: {}".format(self.current_gun))
            self.select_gun_sign = False
            return
        self.current_gun = gun_temp
        self.current_gun_config = ConfigReader.get_gun_config(self.current_gun)
        LogWindow().print_log("枪械: {}, 最大相似度: {}".format(self.current_gun, score_temp))
        self.select_gun_sign = False

    def get_current_gun_config(self):
        return self.current_gun_config
