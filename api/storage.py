#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: 潘高
LastEditors: 潘高
Date: 2023-03-25 19:39:03
LastEditTime: 2023-03-25 20:11:10
Description: 操作存储在数据库中的数据
usage: 调用window.pywebview.api.storage.<methodname>(<parameters>)从Javascript执行
"""

from api.db.orm import ORM


class Storage:
    """存储类"""

    orm = ORM()  # 操作数据库类

    def storage_get(self, key):
        """获取关键词的值"""
        return self.orm.getStorageVar(key)

    def storage_set(self, key, val):
        """设置关键词的值"""
        self.orm.setStorageVar(key, val)


    def search_rule(self, page_num, page_size, is_deprecated):
        """搜索密码"""
        return self.orm.searchRule(page_num, page_size, is_deprecated)

    def add_rule(self, name, min_length, max_length, lower_count, capital_count, number_count, special_count, comment,
                 is_deprecated):
        """添加密码"""
        return self.orm.addRule(name, min_length, max_length, lower_count, capital_count, number_count, special_count,
                                comment, is_deprecated)

    def deprecate_rule(self, id):
        """废弃密码"""
        return self.orm.deprecateRule(id)

    def del_rule(self, id):
        """删除密码"""
        return self.orm.deleteRule(id)

    def update_rule(self, id, min_length, max_length, lower_count, capital_count, number_count, special_count, comment):
        """更新密码"""
        return self.orm.updateRule(id, min_length, max_length, lower_count, capital_count, number_count, special_count,
                                   comment)

    def enable_rule(self, id):
        """启用密码"""
        return self.orm.enableRule(id)

    def add_raw_password(self, raw_password, comment):
        """添加原始密码"""
        return self.orm.addRawPassword(raw_password, comment)

    def delete_raw_password(self, id):
        """删除原始密码"""
        return self.orm.deleteRawPassword(id)

    def search_raw_password(self, page_num, page_size):
        """搜索原始密码"""
        return self.orm.searchRawPassword(page_num, page_size)

    def search_platform(self, page_num, page_size):
        """搜索平台"""
        return self.orm.searchPlatform(page_num, page_size)

    def add_platform(self, platform, comment):
        """添加平台"""
        return self.orm.addPlatform(platform, comment)

    def delete_platform(self, id):
        """删除平台"""
        return self.orm.deletePlatform(id)

    def delete_platform_alias(self, id):
        """删除平台别名"""
        return self.orm.deletePlatformAlias(id)

    def search_platform_alias(self, id):
        """搜索平台别名"""
        return self.orm.searchPlatformAlias(id)

    def add_platform_alias(self, platform_id, alias):
        """添加平台别名"""
        return self.orm.addPlatformAlias(platform_id, alias)

    def search_platform_all(self):
        """搜索平台"""
        return self.orm.searchPlatformAll()

    def search_rule_all(self):
        """搜索规则"""
        return self.orm.searchRuleAll()

    def search_raw_password_all(self):
        """搜索原始密码"""
        return self.orm.searchRawPasswordAll()

    def add_user(self, name, password, salt, is_rule, is_deprecated, comment):
        """添加用户"""
        return self.orm.add_user(name, password, salt, is_rule, is_deprecated, comment)

    def search_user(self, current_page, records_per_page, is_rule, is_deprecated, name, comment):
        return self.orm.search_user(current_page, records_per_page, is_rule, is_deprecated, name, comment)

    def search_rule_by_id(self, id):
        """根据id搜索规则"""
        return self.orm.searchRuleById(id)

    def search_platform_by_id(self, id):
        """根据id搜索平台"""
        return self.orm.searchPlatformById(id)

    def search_raw_password_by_id(self, id):
        """根据id搜索原始密码"""
        return self.orm.searchRawPasswordById(id)

    def check_user_rule(self, user_id):
        return self.orm.check_user_rule(user_id)

    def deprecate_user(self, id):
        return self.orm.deprecate_user(id)

    def enable_user(self, id):
        return self.orm.enable_user(id)

    def delete_user(self, id):
        return self.orm.delete_user(id)
    def update_user(self, id, name, password,comment):
        return self.orm.update_user(id, name, password, comment)