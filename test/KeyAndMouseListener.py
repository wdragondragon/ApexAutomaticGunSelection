import threading
from Tools import Tools


class KeyListener:

    def __init__(self, select_gun, refresh_button):
        super().__init__()
        self.select_gun = select_gun
        self.refresh_button = refresh_button

    def on_press(self, key):
        pass

    # 释放按钮，按esc按键会退出监听
    def on_release(self, key):
        if not hasattr(key, 'name') and hasattr(key, 'char') and key.char is not None and (
                key.char in self.refresh_button):
            threading.Thread(target=self.select_gun.select_gun).start()


class MouseListener:
    def __init__(self):
        super().__init__()
        self.on_mouse_key_map = dict()

    def on_move(self, x, y):
        pass

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.on_mouse_key_map[button] = Tools.current_milli_time()
            print("左键按下")
        elif not pressed:
            if button not in self.on_mouse_key_map:
                return
            print("左键释放, 持续时间: {}".format(Tools.current_milli_time() - self.on_mouse_key_map[button]))
            self.on_mouse_key_map.pop(button)

    def on_scroll(self, x, y, dx, dy):
        pass

    def watch_release(self):
        pass

    def is_press(self, button):
        return button in self.on_mouse_key_map

    def press_time(self, button):
        if self.is_press(button):
            return Tools.current_milli_time() - self.on_mouse_key_map[button]
        else:
            return 0


mouse_listener = None
key_listener = None


def init(select_gun, refresh_button):
    global mouse_listener, key_listener
    mouse_listener = MouseListener()
    key_listener = KeyListener(select_gun=select_gun, refresh_button=refresh_button)
    return (mouse_listener, key_listener)


def get_mouse_listener():
    return mouse_listener


def get_key_listener():
    return key_listener
