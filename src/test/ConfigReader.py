import json
import os.path as op
from jsonpath import jsonpath

config_dict = dict()


def load_config(gun_type):
    global config_dict
    config_file_path = 'config\\' + gun_type + '.json'
    if op.exists(config_file_path):
        with open(config_file_path, 'r') as file:
            config_dict[gun_type] = json.load(file)
            print("加载配置文件: {}".format(config_file_path))
    else:
        print("配置文件不存在: {}".format(config_file_path))
        return


def get_config(gun_type, pattern=None):
    global config_dict
    if gun_type not in config_dict:
        load_config(gun_type)
    if pattern is not None:
        value = jsonpath(config_dict[gun_type], pattern)
        if isinstance(value, list) and len(value) == 1:
            return value[0]
        else:
            return value
    else:
        return config_dict[gun_type]


if __name__ == "__main__":
    load_config('平行步枪')
    print(get_config('平行步枪'))
