import time

from KeyAndMouseListener import *
from KeyAndMouseController import *


def left_click():
    down_time = -1
    while True:
        time.sleep(0.001)
        if mouse_listener.is_press(Button.left) and mouse_listener.is_press(Button.right):
            press_time = mouse_listener.press_time(Button.left)
            press_time = int(press_time / 100)
            if press_time > down_time:
                down_time = press_time
                if press_time in [1, 2, 3, 4, 5]:
                    set_mouse_position(0, 15)
                elif press_time in [12, 13, 14, 15, 16]:
                    set_mouse_position(0, 5)
                elif press_time in [22, 23, 24, 25, 26]:
                    set_mouse_position(0, 3)
                print("down_time: {}".format(down_time))
        else:
            down_time = 0
