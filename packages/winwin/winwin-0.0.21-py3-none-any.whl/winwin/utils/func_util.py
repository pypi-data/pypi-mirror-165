# -*- coding: utf-8 -*-
# @Time    : 2022-07-22 18:20
# @Author  : zbmain

__all__ = ['view_df', 'warning_ignored', 'set_seed', 'delay']

import time

import pandas


def delay(second: int):
    time.sleep(second)

    def wrapper(func):
        def inner(*args, **kwargs):
            ret = func(*args, **kwargs)
            return ret

        return inner

    return wrapper


def view_df(df: pandas.DataFrame, head_num: int = 5, tail_num: int = 5, comment: str = 'DataFrame'):
    print('%s row_size:%d' % (comment, len(df.index)))
    return df.head(head_num).append(df.tail(tail_num))


def pandas_set(max_row: int = 0, max_col: int = 0, max_col_w: int = 0, max_char_size: int = 0,
               float_precision: int = 0):
    """
    @param max_row: 显示最大行数
    @param max_col: 显示最大列数
    @max_col_w: 显示列长度
    @max_char_size: 显示横向最多字符数
    @float_precision: 显示浮点数最多位数
    """
    max_row and pandas.set_option('display.max_rows', max_row)
    max_col and pandas.set_option('display.max_columns', max_col)
    max_col_w and pandas.set_option('display.max_colwidth', max_col_w)
    max_char_size and pandas.set_option('display.width', max_char_size)
    float_precision and pandas.set_option('precision', float_precision)


import warnings


def warning_ignored():
    """关闭一些警告(不推荐)"""
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=ResourceWarning)
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=UserWarning)


def set_seed(seed: int = 1990):
    import numpy, random
    random.seed(seed)
    numpy.random.seed(seed)
    try:
        import tensorflow
        tensorflow.random.set_seed(seed)
        tensorflow.set_random_seed(seed)
    except:
        pass

    try:
        import torch
        torch.manual_seed(seed)  # cpu
        torch.cuda.manual_seed(seed)  # gpu
        torch.cuda.manual_seed_all(seed)  # all gpu
    except:
        pass
