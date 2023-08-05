# -*- coding: utf-8 -*-
# @Time    : 2022-07-22 18:04
# @Author  : zbmain

import json
import logging
import time

from ..utils import support

__all__ = ['Client', 'print_resp']


class Client:
    def __init__(self, nebula_connect=None):
        self.client = nebula_connect or support.nebula_connect()
        self.space = str(self.client.__getattribute__('space'))
        self.comment = str(self.client.__getattribute__('comment'))
        self.heart_beat = int(self.client.__getattribute__('heart_beat'))
        self.vid_str_fixed_size = int(self.client.__getattribute__('vid_str_fixed_size'))

    def exec_query(self, query: str, heart_beat: int = 0):
        resp = self.client.execute(query)
        time.sleep(heart_beat)
        assert resp.is_succeeded(), resp.error_msg()
        return resp

    def test(self, ):
        resp_json = self.client.execute_json("yield 1")
        json_obj = json.loads(resp_json)
        return json.dumps(json_obj, indent=1, sort_keys=True)

    def create_space(self, space: str = '', comment: str = '', vid_str_fixed_size: int = 50):
        space = space or self.space
        comment = comment or self.comment
        vid_str_fixed_size = vid_str_fixed_size or self.vid_str_fixed_size
        assert space
        nGQL = 'CREATE SPACE IF NOT EXISTS %s(vid_type=FIXED_STRING(%d)) comment="%s";USE %s;' % (
            space, vid_str_fixed_size, comment, space)
        logging.info('please wait for create space:"%s"\tnGQL:%s' % (space, nGQL))
        return self.exec_query(nGQL, self.heart_beat)

    def use_space(self, space: str = ''):
        space = space or self.space
        assert space
        return self.exec_query('USE %s;' % space)

    def drop_space(self, space: str = '', drop: bool = False):
        """谨慎操作。参数必须再设置[drop=True]才有效. drop默认:False"""
        space = space or self.space
        assert space
        return drop and self.exec_query('DROP SPACE IF EXISTS %s;' % space)

    def del_all_tags(self, space: str = '', drop: bool = False):
        """谨慎操作。参数必须再设置[drop=True]才有效. drop默认:False"""
        space = space or self.space
        assert space
        return drop and self.exec_query('DELETE TAG * FROM "%s";' % space)

    def submit_stats(self, space: str = ''):
        self.use_space(space)
        return self.exec_query('SUBMIT JOB STATS;', self.heart_beat)

    def show_stats(self, space: str = ''):
        self.submit_stats(space)
        return self.exec_query('SHOW STATS;')

    def show_indexs(self, space: str = ''):
        self.use_space(space)
        return self.exec_query('SHOW TAG INDEXES;')

    def show_spaces(self):
        return self.exec_query('SHOW SPACES;')

    def show_job(self, space: str = ''):
        self.use_space(space)
        return self.exec_query('SUBMIT JOB COMPACT;')

    def release(self):
        if self.client is not None:
            self.client.release()

    def create_index(self, query: str):
        self.use_space()
        self.exec_query(query, self.heart_beat << 1)

    def rebuild_index(self, query: str):
        self.use_space()
        self.exec_query(query, self.heart_beat)


import prettytable


def print_resp(resp):
    assert resp.is_succeeded()
    output_table = prettytable.PrettyTable()
    output_table.field_names = resp.keys()
    for recode in resp:
        value_list = []
        for col in recode:
            if col.is_empty():
                value_list.append('__EMPTY__')
            elif col.is_null():
                value_list.append('__NULL__')
            elif col.is_bool():
                value_list.append(col.as_bool())
            elif col.is_int():
                value_list.append(col.as_int())
            elif col.is_double():
                value_list.append(col.as_double())
            elif col.is_string():
                value_list.append(col.as_string())
            elif col.is_time():
                value_list.append(col.as_time())
            elif col.is_date():
                value_list.append(col.as_date())
            elif col.is_datetime():
                value_list.append(col.as_datetime())
            elif col.is_list():
                value_list.append(col.as_list())
            elif col.is_set():
                value_list.append(col.as_set())
            elif col.is_map():
                value_list.append(col.as_map())
            elif col.is_vertex():
                value_list.append(col.as_node())
            elif col.is_edge():
                value_list.append(col.as_relationship())
            elif col.is_path():
                value_list.append(col.as_path())
            elif col.is_geography():
                value_list.append(col.as_geography())
            else:
                print('ERROR: Type unsupported')
                return
        output_table.add_row(value_list)
    print(output_table)
