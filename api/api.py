#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: 潘高
LastEditors: 潘高
Date: 2022-03-21 17:01:39
LastEditTime: 2023-05-30 15:41:05
Description: 业务层API，供前端JS调用
usage: 在Javascript中调用window.pywebview.api.<methodname>(<parameters>)
"""
import os

from api.storage import Storage
from api.system import System
from utils.password_generator import generate_password_1
import binascii


class API(System, Storage):
    """业务层API，供前端JS调用"""

    def setWindow(self, window):
        """获取窗口实例"""
        System.window = window


    def search_rule(self, page_num: int, page_size: int, is_deprecated: bool):
        return Storage.search_rule(self, page_num, page_size, is_deprecated)

    def add_rule(self, name: str, min_length: int, max_length: int, lower_count: int, capital_count: int,
                 number_count: int, special_count: int, comment: str, is_deprecated: bool):
        return Storage.add_rule(self, name, min_length, max_length, lower_count, capital_count, number_count,
                                special_count, comment, is_deprecated)

    def deprecate_rule(self, id: int):
        return Storage.deprecate_rule(self, id)

    def del_rule(self, id):
        return Storage.del_rule(self, id)

    def update_rule(self, id, min_length: int, max_length: int, lower_count: int, capital_count: int,
                    number_count: int, special_count: int, comment: str):
        return Storage.update_rule(self, id, min_length, max_length, lower_count, capital_count, number_count,
                                   special_count, comment)

    def enable_rule(self, id):
        return Storage.enable_rule(self, id)

    def add_raw_password(self, raw_password: str, comment: str):
        return Storage.add_raw_password(self, raw_password, comment)

    def delete_raw_password(self, id):
        return Storage.delete_raw_password(self, id)

    def search_raw_password(self, page_num: int, page_size: int):
        return Storage.search_raw_password(self, page_num, page_size)

    def add_platform(self, platform, comment):
        return Storage.add_platform(self, platform, comment)

    def delete_platform(self, id):
        return Storage.delete_platform(self, id)

    def delete_platform_alias(self, id):
        return Storage.delete_platform_alias(self, id)

    def search_platform(self, page_num: int, page_size: int):
        return Storage.search_platform(self, page_num, page_size)

    def search_platform_alias(self, id):
        return Storage.search_platform_alias(self, id)

    def add_platform_alias(self, platform_id, alias):
        return Storage.add_platform_alias(self, platform_id, alias)

    def search_platform_all(self):
        return Storage.search_platform_all(self)

    def search_rule_all(self):
        return Storage.search_rule_all(self)

    def search_raw_password_all(self):
        return Storage.search_raw_password_all(self)

    def add_user(self, name, raw_password, is_rule, rule, comment):
        if not is_rule:
            return Storage.add_user(self, name, raw_password, "", False, False, comment)
        else:
            salt = os.urandom(16)
            password = generate_password_1(salt, raw_password, rule['min_length'], rule['max_length'],
                                           rule['lower_count'], rule['upper_count'], rule['number_count'],rule['special_count'])
            return Storage.add_user(self, name, password, salt, True, False, comment)

    def search_user(self, current_page, records_per_page,is_deprecated, name, comment,is_rule=None):
        return Storage.search_user(self, current_page, records_per_page, is_rule, is_deprecated, name, comment)

    def deprecate_user(self, id):
        return Storage.deprecate_user(self, id)

    def enable_user(self, id):
        return Storage.enable_user(self, id)

    def delete_user(self, id):
        return Storage.delete_user(self, id)

    def update_user(self, id, name, raw_password,comment):
        return Storage.update_user(self, id, name, raw_password,comment)
