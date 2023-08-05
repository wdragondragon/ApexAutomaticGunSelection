import json
import os.path as op
from jsonpath import jsonpath

screenshot_resolution = {
    (1920, 1080): (1542, 959, 1695, 996),
    (2560, 1440): (2093, 1281, 2275, 1332),
    (3440, 1440): (2093, 1281, 2275, 1332)
}
config_dict = dict()
global_config = dict()
global_config_path = 'config\\global_config.json'
if op.exists(global_config_path):
    with open(global_config_path, 'r') as global_file:
        global_config = json.load(global_file)


def get_screenshot_resolution(resolution):
    return screenshot_resolution[resolution]

def get_global_config(pattern=None):
    global global_config
    return get_config(global_config, pattern)


def load_gun_config(gun_type):
    global config_dict
    config_file_path = 'config\\' + gun_type + '.json'
    if op.exists(config_file_path):
        with open(config_file_path, 'r') as file:
            config_dict[gun_type] = json.load(file)
            print("加载配置文件: {}".format(config_file_path))
    else:
        print("配置文件不存在: {}".format(config_file_path))
        return


def get_gun_config(gun_type, pattern=None):
    global config_dict
    if gun_type not in config_dict:
        load_gun_config(gun_type)
    return get_config(config_dict[gun_type], pattern)


def get_config(config, pattern=None):
    if pattern is not None:
        value = jsonpath(config, pattern)
        if isinstance(value, list) and len(value) == 1:
            return value[0]
        else:
            return value
    else:
        return config
