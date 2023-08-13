#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FilePath: /PPX/api/db/models.py
Author: 潘高
LastEditors: 潘高
Date: 2023-03-12 20:29:49
LastEditTime: 2023-04-24 13:52:25
Description: 创建数据表
usage: 更新数据表格式后，请按如下操作迁移数据库：
        m=备注更改内容 npm run alembic

        注意：上述命令仅能迁移打包程序自带数据库(Config.staticDir)。在程序运行初始化时，会自动检测并迁移本地电脑中保存的数据库(Config.storageDir)
"""

import json
from sqlalchemy import DateTime, Numeric, Column, Integer, String, text, Boolean
from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()


class BaseModel(Base):
    """基类"""
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(), doc='创建时间', comment='创建时间',
                        server_default=text("(DATETIME(CURRENT_TIMESTAMP, 'localtime'))"))
    updated_at = Column(DateTime(), doc='更新时间', comment='更新时间',
                        server_default=text("(DATETIME(CURRENT_TIMESTAMP, 'localtime'))"),
                        onupdate=text("(DATETIME(CURRENT_TIMESTAMP, 'localtime'))"))

    def _gen_tuple(self):
        # 处理 日期 等无法正常序列化的对象
        def convert_datetime(value):
            if value:
                return value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return ""

        for col in self.__table__.columns:
            try:
                if isinstance(col.type, DateTime):
                    value = convert_datetime(getattr(self, col.name))
                elif isinstance(col.type, Numeric):
                    value = float(getattr(self, col.name))
                else:
                    value = getattr(self, col.name)
                if isinstance(value, bytes):
                    value = value.decode()
                if value is None:
                    value = ""
                yield col.name, value
            except Exception as e:
                print(e)
                pass

    def toDict(self):
        # 转化为 字典
        return dict(self._gen_tuple())

    def toJson(self):
        # 序列化为 JSON
        return json.dumps(self.toDict())


class PPXStorageVar(BaseModel):
    """储存变量"""
    __tablename__ = "ppx_storage_var"
    key = Column(String(), doc='键', nullable=False, index=True)
    val = Column(String(), doc='值', server_default='', nullable=False)
    remark = Column(String(), doc='备注', server_default='', nullable=False)

    def __str__(self):
        return self.key + ' => ' + self.val





class Platform(BaseModel):
    __tablename__ = "platform"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False, unique=True)
    comment = Column(String(255))


class PlatformAlias(BaseModel):
    __tablename__ = "platform_alias"
    id = Column(Integer, primary_key=True, autoincrement=True)
    platform_id = Column(Integer, nullable=False)
    name = Column(String(80), nullable=False)
    comment = Column(String(255))


class User(BaseModel):
    __tablename__ = "user"
    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
    name = Column(String(80), nullable=False)
    password = Column(String(80), nullable=False)
    comment = Column(String(255))
    salt = Column(String(80))
    is_rule = Column(Boolean)
    is_deprecated = Column(Boolean)


class RawPassword(BaseModel):
    __tablename__ = "raw_password"
    id = Column(Integer, primary_key=True, autoincrement=True)
    raw_password = Column(String(80), nullable=False)
    comment = Column(String(255))


class Rule(BaseModel):
    __tablename__ = "rule"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False, unique=True)
    comment = Column(String(255))
    min_length = Column(Integer)
    max_length = Column(Integer)
    lower_count = Column(Integer)
    upper_count = Column(Integer)
    number_count = Column(Integer)
    special_count = Column(Integer)
    is_deprecated = Column(Boolean)
