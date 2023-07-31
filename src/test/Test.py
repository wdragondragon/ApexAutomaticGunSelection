import threading

from pynput.mouse import Controller, Button
from KeyAndMouseListener import *

from src.test.ApexMouseLisenter import *

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

threading.Thread(target=left_click).start()
