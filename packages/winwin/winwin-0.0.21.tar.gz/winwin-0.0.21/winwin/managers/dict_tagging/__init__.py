# -*- coding: utf-8 -*-
# @Time    : 2022-08-28 00:32
# @Author  : zbmain

import jieba
from jieba import posseg

from .util import *

SEP = ' '

DEFAULT_DICT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dict.txt")
with open(DEFAULT_DICT, 'w', encoding='utf-8') as f:
    f.write('n 1 n')


class Custom_JiebaTokenizer(jieba.Tokenizer):
    def __init__(self, dictionary: str = DEFAULT_DICT, sep=SEP, preload_jieba_default_dictionary: bool = False):
        super(Custom_JiebaTokenizer, self).__init__(None if preload_jieba_default_dictionary else DEFAULT_DICT)
        self.name = ''
        self.load_userdict(dictionary, sep)

    def load_userdict(self, dictionary, sep=SEP):
        userdict_list = []
        if isinstance(dictionary, str):
            with open(dictionary, 'r', encoding='utf-8') as f:
                userdict_list = f.readlines()
        elif isinstance(dictionary, list):
            userdict_list = dictionary
        else:
            raise TypeError('param:custom_dict types must in [list,str]')
        if not len(userdict_list):
            return

        if sep not in userdict_list[0]:
            self.name = get_tokenizer_name(userdict_list[0].strip()) or ''
            userdict_list = userdict_list[1:]

        for line in userdict_list:
            line = list(filter(lambda x: x, line.strip().split(sep)))
            words, tag = line[:-1] if len(line) > 1 else line, line[-1]
            for word in words:
                print('add: ',word,'-',tag)
                self.add_word(word, freq=None, tag=tag)

    def cut(self, sentence, cut_all=False, HMM=True, use_paddle=False):
        return super(Custom_JiebaTokenizer, self).cut(sentence, cut_all=cut_all, HMM=HMM, use_paddle=use_paddle)

    def lcut(self, *args, **kwargs):
        return super(Custom_JiebaTokenizer, self).lcut(*args, **kwargs)


class Custom_POSTokenizer(posseg.POSTokenizer):
    def __init__(self, dictionary: str = DEFAULT_DICT, sep=SEP, preload_jieba_default_dictionary: bool = False):
        self.jieba_tokenizer = Custom_JiebaTokenizer(dictionary, sep, preload_jieba_default_dictionary)
        self.name = self.jieba_tokenizer.name
        print('dict::',dictionary,self.name)
        super(Custom_POSTokenizer, self).__init__(self.jieba_tokenizer)

    def load_userdict(self, dictionary, sep=SEP):
        self.jieba_tokenizer.load_userdict(dictionary, sep)

    def cut(self, sentence, HMM=False):
        return super(Custom_POSTokenizer, self).cut(sentence, HMM=HMM)

    def lcut(self, *args, **kwargs):
        return super(Custom_POSTokenizer, self).lcut(*args, **kwargs)

    def jcut(self, sentence, cut_all=False, HMM=False, use_paddle=False):
        return self.jb_tokenizer.cut(sentence, cut_all=cut_all, HMM=HMM, use_paddle=use_paddle)


class ObjectPool(object):

    def __init__(self, Cls):
        super(ObjectPool, self).__init__()
        self.Cls = Cls
        self.storage = {}

    def _put(self, obj: object, key=None, froce=True):
        key = key or (hasattr(obj, 'name') and obj.__getattribute__('name')) or ''
        if froce or self.storage.get(key) is not None:
            self.storage[key] = obj

    def set(self, key, *args, **kwargs):
        _obj = self.storage.get(key)
        if _obj:
            _obj.load_dictionary(*args, **kwargs)
        else:
            _obj = self.Cls(*args, **kwargs)
            self._put(_obj, key)
        return _obj

    def get(self, key):
        return self.storage.get(key)


class Tagging:
    def __init__(self, dictionary, sep=SEP, suffixes='txt'):
        self.tokenizer_pool = ObjectPool(Custom_POSTokenizer)
        self.add_userdict(dictionary, sep, suffixes)

    def load_dictionarys(self, dictionary, suffixes='txt;tsv'):
        if isinstance(dictionary, dict):
            dictionary = dictionary.items()
        elif isinstance(dictionary, list):
            dictionary = util.parse_list(dictionary)
        elif isinstance(dictionary, str):
            dictionary = util.parse_dir(dictionary, suffixes=suffixes, split_char=';')
        return dictionary

    def add_userdict(self, dictionary, sep=SEP, suffixes='txt;tsv'):
        dictionary = self.load_dictionarys(dictionary, suffixes)
        for token in dictionary:
            for k, v in util.process_tokenizer_dict(token).items():
                self.tokenizer_pool.set(key=k, dictionary=v, sep=sep)

    def get_tokenizer(self, token_name) -> Custom_POSTokenizer:
        return self.tokenizer_pool.get(token_name)
