# -*- coding: utf-8 -*-
# @Time    : 2022-08-22 23:05
# @Author  : zbmain

import yaml


def read_yaml(yaml_url: str):
    with open(yaml_url, 'r', encoding='utf-8') as yaml_file:
        __yaml = yaml.load(yaml_file, Loader=yaml.SafeLoader)
    return __yaml
