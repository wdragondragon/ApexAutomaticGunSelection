import os

import pynput
from PIL import ImageGrab
from Tools import Tools
from LogWindow import LogWindow


class KeyListener:

    def __init__(self, refresh_button, bbox, lg_file_path, lua_suffix, resolution_path):
        super().__init__()
        self.on_key_map = dict()
        self.refresh_button = refresh_button
        self.bbox = bbox
        self.lg_file_path = lg_file_path
        self.lua_suffix = lua_suffix
        self.lua_path = lg_file_path + 'lua\\'
        self.common_file = self.lua_path + '通用' + lua_suffix
        self.shake_file = lg_file_path + 'shake' + lua_suffix
        self.image_path = lg_file_path + 'images\\' + resolution_path

    def on_press(self, key):
        if key is None or (hasattr(key, 'char') and key.char is None):
            return
        if hasattr(key, 'name'):
            key_name = key.name
        else:
            key_name = key.char
        if key_name in self.on_key_map:
            return
        self.on_key_map[key_name] = Tools.current_milli_time()
        # LogWindow().print_log('{0} 被按下'.format(key_name))
        return

    # 释放按钮，按esc按键会退出监听
    def on_release(self, key):
        if key is None or (hasattr(key, 'char') and key.char is None):
            return
        if hasattr(key, 'name') and (key.name in self.on_key_map):
            key_name = key.name
        else:
            key_name = key.char
        if key_name in self.on_key_map:
            start_time = self.on_key_map[key_name]
            press_time = Tools.current_milli_time() - start_time
            self.on_key_map.pop(key_name)
            LogWindow().print_log("按键: {}, 按下时间: {}".format(key_name, press_time))

        # LogWindow().print_log('{0} 被释放'.format(key))
        if not hasattr(key, 'name') and (key.char in self.refresh_button):
            score_temp = 0.00000000000000000000
            max_gun = ''
            img = ImageGrab.grab(bbox=self.bbox)
            for fileName in os.listdir(self.image_path):
                score = Tools.compare_image(img, self.image_path + fileName)
                if score > score_temp:
                    score_temp = score
                    max_gun = fileName.split('.')[0]
            LogWindow().print_log("枪械: {}, 最大相似度: {}".format(max_gun, score_temp))
            if os.path.exists(self.lua_path + max_gun + self.lua_suffix):
                LogWindow().print_log("已切换到: {}".format(max_gun))
                Tools.copy_file(self.lua_path + max_gun + self.lua_suffix, self.shake_file)
            else:
                LogWindow().print_log("未找到: {}".format(max_gun))
                Tools.copy_file(self.common_file, self.shake_file)


class MouseListener:
    def __init__(self):
        super().__init__()
        self.on_mouse_key_map = dict()

    def on_move(self, x, y):
        # LogWindow().print_log('Pointer moved to {0}'.format((x, y)))
        pass

    def on_click(self, x, y, button, pressed):
        if button == pynput.mouse.Button.left and pressed:
            self.on_mouse_key_map[button] = Tools.current_milli_time()
            LogWindow().print_log("左键按下")
        elif button == pynput.mouse.Button.left and not pressed:
            if button not in self.on_mouse_key_map:
                return
            press_time = Tools.current_milli_time() - self.on_mouse_key_map[button]
            self.on_mouse_key_map.pop(button)
            LogWindow().print_log("左键释放, 持续时间: {}".format(press_time))
        # LogWindow().print_log('{0} {1} at {2}'.format(
        #     'Pressed' if pressed else 'Released', button, (x, y)))

    def on_scroll(self, x, y, dx, dy):
        # LogWindow().print_log('Scrolled {0} at {1}'.format(
        #     'down' if dy < 0 else 'up',
        #     (x, y)))
        pass
