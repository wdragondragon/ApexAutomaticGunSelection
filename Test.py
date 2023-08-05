import sys

import pynput
from PyQt5.QtWidgets import QApplication

from LogWindow import LogWindow
from Tools import Tools
import threading

import test.KeyAndMouseListener as KeyAndMouseListener
from test import ConfigReader, ScreenUtil
from test.ApexMouseLisenter import left_click

if __name__ == "__main__":
    app = QApplication(sys.argv)
    log_window = LogWindow()
    # log_window.setWindowFlags(Qt.WindowStaysOnTopHint)
    log_window.show()
    base_file_path = ConfigReader.get_global_config('base_file_path')
    refresh_button = ConfigReader.get_global_config('refresh_button')
    (x, y) = Tools.get_resolution()
    bbox = ConfigReader.get_screenshot_resolution((x, y))
    resolution_path = '{}x{}\\'.format(x, y)
    select_gun = ScreenUtil.SelectGun(bbox=bbox,
                                      base_file_path=base_file_path,
                                      resolution_path=resolution_path)

    (mouse_listener, key_listener) = KeyAndMouseListener.init(select_gun=select_gun, refresh_button=refresh_button)

    g_mouse_listener = pynput.mouse.Listener(
        on_move=mouse_listener.on_move,
        on_click=mouse_listener.on_click,
        on_scroll=mouse_listener.on_scroll)

    g_keyboard_listener = pynput.keyboard.Listener(on_press=key_listener.on_press,
                                                   on_release=key_listener.on_release)

    mouse_listener_thread = threading.Thread(target=g_mouse_listener.start)
    keyboard_listener_thread = threading.Thread(target=g_keyboard_listener.start)

    mouse_listener_thread.start()
    keyboard_listener_thread.start()

    threading.Thread(target=left_click, args={select_gun}).start()
    sys.exit(app.exec_())
