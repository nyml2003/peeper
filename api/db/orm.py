#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: 潘高
LastEditors: 潘高
Date: 2023-03-12 20:08:30
LastEditTime: 2023-04-12 20:50:53
Description: 操作数据库类
usage:
    from api.db.orm import ORM

    orm = ORM()    # 操作数据库类
    author = self.orm.getStorageVar('author')    # 获取储存变量
    print('author', author)
"""
import sqlite3

import sqlalchemy
import pinyin
from api.db.models import PPXStorageVar, Rule, Platform, PlatformAlias, RawPassword, User
from pyapp.db.db import DB
from sqlalchemy import select, update, insert, func, delete


class ORM:
    """操作数据库类"""

    def getStorageVar(self, key):
        """获取储存变量"""
        resVal = ''
        dbSession = DB.session()
        with dbSession.begin():
            stmt = select(PPXStorageVar.value).where(PPXStorageVar.key == key)
            result = dbSession.execute(stmt)
            result = result.one_or_none()
            if result is None:
                # 新建
                stmt = insert(PPXStorageVar).values(key=key)
                dbSession.execute(stmt)
            else:
                resVal = result[0]
        dbSession.close()
        return resVal

    def setStorageVar(self, key, val):
        """更新储存变量"""
        dbSession = DB.session()
        with dbSession.begin():
            stmt = update(PPXStorageVar).where(PPXStorageVar.key == key).values(value=val)
            dbSession.execute(stmt)
        dbSession.close()




    def addRule(self, name, min_length, max_length, lower_count, upper_count, number_count, special_count, comment,
                is_deprecated=False):
        dbSession = DB.session()
        try:
            with dbSession.begin():
                dbSession.add(Rule(name=name, min_length=min_length, max_length=max_length, lower_count=lower_count,
                                   upper_count=upper_count, number_count=number_count, special_count=special_count,
                                   comment=comment, is_deprecated=is_deprecated))
            dbSession.close()
            return {
                'message': 'ok',
                'code': 0
            }
        except sqlalchemy.exc.IntegrityError as e:
            return {
                'message': '规则名称不能重复',
                'code': 1
            }

    def searchRule(self, page_num=1, page_size=10, is_deprecated=False):
        dbSession = DB.session()
        with dbSession.begin():
            query = select(Rule).where(Rule.is_deprecated == is_deprecated)
            total = dbSession.execute(select(func.count()).select_from(query.subquery())).scalar()
            result = [row[0].toJson() for row in
                      dbSession.execute(query.limit(page_size).offset((page_num - 1) * page_size)).all()]
        dbSession.close()
        return {
            'data': result,
            'recordsOnPage': len(result),
            'total': total
        }

    def deprecateRule(self, id: int):
        dbSession = DB.session()
        with dbSession.begin():
            stmt = update(Rule).where(Rule.id == id).values(is_deprecated=True)
            dbSession.execute(stmt)
        dbSession.close()
        return {
            'message': 'ok',
            'code': 0
        }

    def enableRule(self, id: int):
        dbSession = DB.session()
        with dbSession.begin():
            stmt = update(Rule).where(Rule.id == id).values(is_deprecated=False)
            dbSession.execute(stmt)
        dbSession.close()
        return {
            'message': 'ok',
            'code': 0
        }

    def updateRule(self, id: int, min_length, max_length, lower_count, upper_count, number_count, special_count,
                   comment):
        dbSession = DB.session()
        with dbSession.begin():
            stmt = update(Rule).where(Rule.id == id).values(min_length=min_length, max_length=max_length,
                                                            lower_count=lower_count,
                                                            upper_count=upper_count, number_count=number_count,
                                                            special_count=special_count,
                                                            comment=comment)
            dbSession.execute(stmt)
        dbSession.close()
        return {
            'message': 'ok',
            'code': 0
        }

    def deleteRule(self, id: int):
        dbSession = DB.session()
        with dbSession.begin():
            stmt = delete(Rule).where(Rule.id == id)
            dbSession.execute(stmt)
        dbSession.close()
        return {
            'message': 'ok',
            'code': 0
        }

    def addPlatform(self, name, comment):
        try:
            dbSession = DB.session()
            with dbSession.begin():
                platform = Platform(name=name, comment=comment)
                dbSession.add(platform)
                dbSession.flush()
                platform_alias = PlatformAlias(name=pinyin.get(name, format="strip", delimiter=""),
                                               platform_id=platform.id, comment='拼音')
                dbSession.add(platform_alias)
            dbSession.commit()
            return {
                'message': 'ok',
                'code': 0
            }
        except sqlalchemy.exc.IntegrityError as e:
            return {
                'message': '平台名称不能重复',
                'code': 1
            }

    def addPlatformAlias(self, platform_id, name):
        dbSession = DB.session()
        with dbSession.begin():
            platform_alias = PlatformAlias(name=name, platform_id=platform_id, comment='alias')
            dbSession.add(platform_alias)
        dbSession.commit()
        return {
            'message': 'ok',
            'code': 0
        }

    def searchPlatform(self, page_num=1, page_size=10, name=""):
        dbSession = DB.session()
        with dbSession.begin():
            query = select(Platform).where(Platform.name.like("%" + name + "%"))
            total = dbSession.execute(select(func.count()).select_from(query.subquery())).scalar()
            result = [row[0].toJson() for row in
                      dbSession.execute(query.limit(page_size).offset((page_num - 1) * page_size)).all()]
        dbSession.close()
        return {
            'data': result,
            'recordsOnPage': len(result),
            'total': total
        }

    def deletePlatform(self, id):
        dbSession = DB.session()
        with dbSession.begin():
            dbSession.execute(delete(PlatformAlias).where(PlatformAlias.platform_id == id))
            dbSession.execute(delete(Platform).where(Platform.id == id))
        dbSession.close()
        return {
            'message': 'ok',
            'code': 0
        }

    def deletePlatformAlias(self, id):
        dbSession = DB.session()
        with dbSession.begin():
            stmt = delete(PlatformAlias).where(PlatformAlias.id == id)
            dbSession.execute(stmt)
        dbSession.close()
        return {
            'message': 'ok',
            'code': 0
        }

    def searchPlatformAlias(self, id):
        dbSession = DB.session()
        with dbSession.begin():
            query = select(PlatformAlias).where(PlatformAlias.platform_id == id)
            result = [row[0].toJson() for row in
                      dbSession.execute(query).all()]
        dbSession.close()
        return {
            'data': result
        }

    def addRawPassword(self, raw_password, comment):
        dbSession = DB.session()
        with dbSession.begin():
            raw_password = RawPassword(raw_password=raw_password, comment=comment)
            dbSession.add(raw_password)
        dbSession.commit()
        return {
            'message': 'ok',
            'code': 0
        }

    def deleteRawPassword(self, id):
        dbSession = DB.session()
        with dbSession.begin():
            stmt = delete(RawPassword).where(RawPassword.id == id)
            dbSession.execute(stmt)
        dbSession.close()
        return {
            'message': 'ok',
            'code': 0
        }

    def searchRawPassword(self, page_num=1, page_size=10):
        dbSession = DB.session()
        with dbSession.begin():
            query = select(RawPassword)
            total = dbSession.execute(select(func.count()).select_from(query.subquery())).scalar()
            result = [row[0].toJson() for row in
                      dbSession.execute(query.limit(page_size).offset((page_num - 1) * page_size)).all()]
        dbSession.close()
        return {
            'data': result,
            'recordsOnPage': len(result),
            'total': total
        }

    def searchPlatformAll(self):
        dbSession = DB.session()
        with dbSession.begin():
            query = select(Platform)
            result = [{
                'id': row[0].id,
                'name': row[0].name
            }
                for row in dbSession.execute(query).all()]
        return {
            'data': result
        }

    def searchRuleById(self, id):
        dbSession = DB.session()
        with dbSession.begin():
            query = select(Rule).where(Rule.id == id)
            result = [row[0].toDict() for row in dbSession.execute(query).all()]
        return {
            'data': result
        }

    def searchPlatformById(self, id):
        dbSession = DB.session()
        with dbSession.begin():
            query = select(Platform).where(Platform.id == id)
            result = [row[0].toDict() for row in dbSession.execute(query).all()]
        return {
            'data': result
        }

    def searchRawPasswordById(self, id):
        dbSession = DB.session()
        with dbSession.begin():
            query = select(RawPassword).where(RawPassword.id == id)
            result = [row[0].toDict() for row in dbSession.execute(query).all()]
        return {
            'data': result
        }

    def searchRuleAll(self):
        dbSession = DB.session()
        with dbSession.begin():
            query = select(Rule).where(Rule.is_deprecated == False)
            result = [{
                'id': row[0].id,
                'name': row[0].name,
                'rule': {
                    'min_length': row[0].min_length,
                    'max_length': row[0].max_length,
                    'lower_count': row[0].lower_count,
                    'upper_count': row[0].upper_count,
                    'number_count': row[0].number_count,
                    'special_count': row[0].special_count
                }
            }
                for row in dbSession.execute(query).all()]
        return {
            'data': result
        }

    def searchRawPasswordAll(self):
        dbSession = DB.session()
        with dbSession.begin():
            query = select(RawPassword)
            result = [{
                'id': row[0].id,
                'raw_password': row[0].raw_password
            }
                for row in dbSession.execute(query).all()]
        return {
            'data': result
        }

    @staticmethod
    def check_user_rule(user_id):
        db_session = DB.session()
        with db_session.begin():
            res = db_session.execute(select(User).where(User.id == user_id)).all()[0].is_rule
        return res

    @staticmethod
    def add_user(name: str, password: str, salt: str, is_rule: bool, is_deprecated: bool, comment: str):
        db_session = DB.session()
        try:
            with db_session.begin():
                user = User(name=name, password=password, salt=salt, is_rule=is_rule, is_deprecated=is_deprecated,
                            comment=comment)
                db_session.add(user)
            db_session.commit()
            return {
                'message': 'ok',
                'code': 0
            }
        except Exception as e:
            return {
                'message': str(e),
                'code': 1
            }

    @staticmethod
    def search_user(current_page: int, records_per_page: int, is_rule: bool, is_deprecated: bool, name: str,
                    comment: str):
        db_session = DB.session()
        with db_session.begin():
            if is_rule is None:
                query = select(User).where(User.is_deprecated == is_deprecated,
                                           User.name.like("%" + name + "%"), User.comment.like("%" + comment + "%"))
            else:
                query = select(User).where(User.is_rule == is_rule, User.is_deprecated == is_deprecated,
                                           User.name.like("%" + name + "%"), User.comment.like("%" + comment + "%"))
            total = db_session.execute(select(func.count()).select_from(query.subquery())).scalar()
            result = [row[0].toDict() for row in
                      db_session.execute(
                          query.limit(records_per_page).offset((current_page - 1) * records_per_page)).all()]
        return {
            'data': result,
            'recordsOnPage': len(result),
            'total': total
        }

    @staticmethod
    def deprecate_user(id: int):
        db_session = DB.session()
        with db_session.begin():
            stmt = update(User).where(User.id == id).values(is_deprecated=True)
            db_session.execute(stmt)
        db_session.close()
        return {
            'message': 'ok',
            'code': 0
        }

    @staticmethod
    def enable_user(id: int):
        db_session = DB.session()
        with db_session.begin():
            stmt = update(User).where(User.id == id).values(is_deprecated=False)
            db_session.execute(stmt)
        db_session.close()
        return {
            'message': 'ok',
            'code': 0
        }

    @staticmethod
    def delete_user(id: str):
        db_session = DB.session()
        with db_session.begin():
            stmt = delete(User).where(User.id == id)
            db_session.execute(stmt)
        db_session.close()
        return {
            'message': 'ok',
            'code': 0
        }

    @staticmethod
    def update_user(id: int, name: str, password: str, comment: str):
        db_session = DB.session()
        with db_session.begin():
            stmt = update(User).where(User.id == id).values(name=name, password=password, salt="", is_rule=False,
                                                            comment=comment)
            db_session.execute(stmt)
        db_session.close()
        return {
            'message': 'ok',
            'code': 0
        }
