# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base


HOSTNAME = 'localhost'
PORT = '3306'
DATABASE = 'personal_blog'
USERNAME = 'root'
PASSWORD = 'root'

url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    USERNAME,
    PASSWORD,
    HOSTNAME,
    PORT,
    DATABASE,
)

engine = create_engine(url)
session = sessionmaker(engine)      # 创建会话， 用于对数据的执行操作
# Base = declarative_base(url)       # 创建基类，用于创建模型映射使用
#  创建表
migrate = Base.metadata.create_all(engine)

# # 连接数据库
# conection = engine.connect()
# # 执行数据库语言
# result = conection.execute('select * from user')
# print(result.fetchone())


