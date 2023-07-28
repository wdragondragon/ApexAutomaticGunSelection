import configparser
import threading

import pynput
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

import ApexListener
from Tools import Tools
from LogWindow import LogWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    log_window = LogWindow()
    # log_window.setWindowFlags(Qt.WindowStaysOnTopHint)
    log_window.show()

    config = configparser.ConfigParser()  # 创建对象
    config.read("apex.conf", encoding="utf-8")

    lg_file_path = config.get('conf', 'lg_file_path')
    refresh_button = config.get('conf', 'refresh_button')

    lua_suffix = '.lua'
    lua_path = lg_file_path + 'lua\\'
    common_file = lua_path + '通用' + lua_suffix
    shake_file = lg_file_path + 'shake' + lua_suffix

    screenshot_resolution = {
        (1920, 1080): (1542, 959, 1695, 996),
        (2560, 1440): (2093, 1281, 2275, 1332),
        (3440, 1440): (2093, 1281, 2275, 1332)
    }

    keyboard = pynput.keyboard.Controller()

    (x, y) = Tools.get_resolution()

    resolution_path = '{}x{}\\'.format(x, y)

    image_path = lg_file_path + 'images\\' + resolution_path

    bbox = screenshot_resolution[(x, y)]

    log_window.print_log("分辨率: {}x{}".format(x, y))

    log_window.print_log("截图区域: {}".format(bbox))

    apex_key_listener = ApexListener.KeyListener(refresh_button=refresh_button,
                                                 bbox=bbox,
                                                 lg_file_path=lg_file_path,
                                                 lua_suffix=lua_suffix,
                                                 resolution_path=resolution_path)

    apex_mouser_listener = ApexListener.MouseListener()

    # Collect events until released
    mouse_listener = pynput.mouse.Listener(
        on_move=apex_mouser_listener.on_move,
        on_click=apex_mouser_listener.on_click,
        on_scroll=apex_mouser_listener.on_scroll)

    keyboard_listener = pynput.keyboard.Listener(on_press=apex_key_listener.on_press,
                                                 on_release=apex_key_listener.on_release)

    mouse_listener_thread = threading.Thread(target=mouse_listener.start)
    keyboard_listener_thread = threading.Thread(target=keyboard_listener.start)

    mouse_listener_thread.start()
    keyboard_listener_thread.start()

    key_release_thread = threading.Thread(target=apex_mouser_listener.watch_release)
    key_release_thread.start()

    sys.exit(app.exec_())
