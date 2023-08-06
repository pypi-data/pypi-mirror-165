# -*- coding: utf-8 -*-
# @Time    : 2022-08-28 20:14
# @Author  : zbmain
import os
import re
from os.path import join
from os.path import split
from os.path import splitext

from winwin.utils.str_util import strip


TOKENIZER_NAME_RE = re.compile('##(.*)##')


def get_tokenizer_name(x):
    match = re.match(TOKENIZER_NAME_RE, x)
    return match.group(1) or '' if match else None

def process_tokenizer_dict(dictionary) -> tuple:
    """
    解析词典，获取分词器名称 和 实体词列表

    :param dictionary: 词典
    :return:
    """
    token_name, dictionary = dictionary
    print('@-@', token_name, dictionary)
    result = {}
    tagwords_list = []
    if type(dictionary) is str:
        if os.path.exists(dictionary):
            with open(dictionary) as f:
                token_tagwords_list = []
                for line in f.readlines():
                    _token_name = get_tokenizer_name(line.strip())
                    if _token_name is not None:
                        # 遇到类目标签前，先归类已包含的词
                        if len(token_tagwords_list) and token_name:
                            result[token_name] = token_tagwords_list
                        token_name = _token_name
                        token_tagwords_list = result.get(token_name, [])
                        continue
                    token_tagwords_list.append(line.strip())
                # 结束归类
                result[token_name] = token_tagwords_list

        return result
    elif type(dictionary) is list:
        tagwords_list = list(remove_invalid_words(dictionary))
    else:
        pass
    return {token_name: tagwords_list}


def remove_invalid_words(x: str):
    return filter(lambda y: y.strip(), map(lambda z: z.strip(), x))


def parse_list(dict_list):
    return [(splitext(split(path)[1])[0], path) for path in dict_list]


def str2list(text: str, split_char: str = ';', starts_char: str = '', ends_char: str = ''):
    return [starts_char + char + ends_char for char in strip(text, split_char).split(split_char)]


def parse_dir(dir_path, suffixes: str = 'txt;', split_char: str = ';'):
    suffixes = str2list(suffixes, split_char, starts_char='.')
    return [(splitext(split(p)[1])[0], join(dir_path, p)) for p in os.listdir(dir_path) if splitext(p)[1] in suffixes]
