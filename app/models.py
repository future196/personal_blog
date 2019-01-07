# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Text, DateTime, BIGINT, ForeignKey
import datetime
Base = declarative_base()


class Personal(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    account = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    content = Column(String(500))
    icon = Column(String(255))


class Visitor(Base):
    __tablename__ = "visitor"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    ip = Column(String(255), nullable=False)
    icon = Column(String(255))
    create_time = Column(DateTime, default=datetime.datetime.now)


class Visit_Record(Base):
    __tablename__ = "visitor_record"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(255), nullable=False)
    create_time = Column(DateTime, default=datetime.datetime.now)


class Article(Base):
    __tablename__ = "article"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    intro = Column(Text)
    content = Column(Text)
    author = Column(String(50), nullable=False)
    create_time = Column(DateTime, default=datetime.datetime.now)
    read = Column(BIGINT)
    face_img = Column(String(255))
    type_id = Column(Integer, ForeignKey("article_type.id"))
    tag = Column(String(255))
    type = relationship("Article_type", backref="article", lazy="select")



class Gbook(Base):
    __tablename__ = "gbook"
    id = Column(Integer, primary_key=True, autoincrement=True)
    visitor_id = Column(Integer, ForeignKey("visitor.id"))
    content = Column(Text)
    username = Column(String(255))
    email = Column(String(255))
    reply = Column(Text)
    create_time = Column(DateTime, default=datetime.datetime.now)


class Read(Base):
    __tablename__ = "read"
    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(Integer, ForeignKey("article.id"))
    visitor_id = Column(Integer, ForeignKey("visitor.id"))
    create_time = Column(DateTime, default=datetime.datetime.now)


class Like(Base):
    __tablename__ = "like"
    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(Integer, ForeignKey("article.id"))
    visitor_id = Column(Integer, ForeignKey("visitor.id"))
    create_time = Column(DateTime, default=datetime.datetime.now)


class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(Integer, ForeignKey("article.id"))
    visitor_id = Column(Integer, ForeignKey("visitor.id"))
    content = Column(Text)
    reply = Column(Text)
    create_time = Column(DateTime, default=datetime.datetime.now)
    visitor = relationship("Visitor", backref="comment", lazy="select")


class Article_type(Base):
    __tablename__ = "article_type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)



class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)


class Recommend(Base):
    __tablename__ = "recommend"
    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(Integer, ForeignKey("article.id"))
    create_time = Column(DateTime, default=datetime.datetime.now)
    article = relationship("Article", backref="recommend", lazy="select")


class Login_log(Base):
    __tablename__ = "login_log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(255))
    admin = Column(String(255))
    create_time = Column(DateTime, default=datetime.datetime.now)