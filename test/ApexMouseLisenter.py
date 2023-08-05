import time

from pynput.mouse import Button

from test.KeyAndMouseController import set_mouse_position
from test.KeyAndMouseListener import get_mouse_listener


def left_click(select_gun):
    down_time = -1
    while True:
        time.sleep(0.0005)
        mouse_listener = get_mouse_listener()
        if mouse_listener.is_press(Button.left) and mouse_listener.is_press(Button.right):
            current_gun_config = select_gun.get_current_gun_config()
            fire_rate = current_gun_config["fire_rate"]
            fixed_interval = current_gun_config["fixed_interval"]
            interval = 60.0 / fire_rate
            if fixed_interval:
                time.sleep(interval)
            mouse_move = current_gun_config["mouse_move"]
            press_time = mouse_listener.press_time(Button.left)
            press_time = int(press_time / (interval * 1000))
            print("press_time {} ,down_time:{} len_mouse_move:{}".format(press_time, down_time, len(mouse_move)))
            if press_time > down_time and press_time + 1 < len(mouse_move):
                down_time = press_time
                move_x_y = mouse_move[press_time]
                set_mouse_position(move_x_y["x"], move_x_y["y"])
                print("down_time: {}".format(down_time))
        else:
            down_time = 0
