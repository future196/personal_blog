# -*- coding: utf-8 -*-
from tornado.web import RequestHandler
from app.models import Article, Recommend, Tag, Like, Comment, Visitor, Gbook, Visit_Record
from app.sqlalchemy_db import session
from app.painate import paginate
session = session()
import random
import time
from tornado import gen
from tornado.httpclient import AsyncHTTPClient



def public():
    articles = session.query(Article).order_by("-create_time").all()
    type_list = []
    type_id_list = []
    for article in articles:
        if article.type_id not in type_id_list:
            type_id_list.append(article.type_id)
    for type_id in type_id_list:
        type_list.append(session.query(Article).filter_by(type_id=type_id).all())

    recommends = session.query(Recommend).order_by("-create_time").all()
    tags = session.query(Tag).all()
    ranking = session.query(Article).order_by(Article.read.desc()).all()
    content = {
        "type_list": type_list,
        "recommends": recommends,
        "tags": tags,
        "ranking": ranking,
    }
    return content


class Index(RequestHandler):
    def get(self):
        if self.get_cookie("visitor_ip", 0) == 0:
            self.set_cookie("visitor_ip", self.request.remote_ip, expires=time.time()+600)
            visit = Visit_Record(ip=self.request.remote_ip)
            session.add(visit)
            session.commit()
        page = self.get_argument("page", 1)
        remote = self.request.remote_ip
        type_id = int(self.get_argument("type", 0))
        tag = self.get_argument("tag", 0)
        search = self.get_argument("keyboard", 0)
        if session.query(Visitor).filter_by(ip=remote).count() != 1:
            username = ""
            for i in range(8):
                username = username + str(random.randint(0, 9))
            visitor = Visitor(username=username, ip=remote, icon=username[-1:]+".jpg")
            session.add(visitor)
            session.commit()
        content = public()
        content["articles"] = session.query(Article).order_by("-create_time").all()
        if type_id != 0:
            content["articles"] = session.query(Article).filter_by(type_id=type_id).order_by("-create_time").all()
        if tag != 0:
            content["articles"] = session.query(Article).filter(Article.tag.like("%" + tag + "%")).order_by("-create_time").all()
        if search != 0:
            content["articles"] = session.query(Article).filter(Article.title.like("%" + search + "%")).order_by("-create_time").all()
        object = paginate(content["articles"], page=int(page), per_page=10)
        content["length"] = object["length"]
        content["pages"] = object["pages"]
        content["page"] = object["page"]
        content["has_next"] = object["has_next"]
        content["has_pre"] = object["has_pre"]
        content["result"] = object["result"]
        content["type_id"] = type_id
        content["tag_"] = tag
        content["search"] = search
        self.render("home/index.html", **content)


class Detail(RequestHandler):
    def get(self, *args, **kwargs):
        target = self.get_argument("target", 1)
        content = public()
        article = session.query(Article).get(target)
        like = session.query(Like).filter_by(article_id=article.id)
        object = session.query(Article).all()
        # 添加一个阅读量
        article.read = article.read + 1
        session.add(article)
        session.commit()
        target_index = None
        pre_article = ""
        next_article = ""
        for index, obj in enumerate(object):
            if article == obj:
                target_index = index
        if object[-1] != object[target_index]:
            pre_article = object[target_index + 1]
        if object[0] != object[target_index]:
            next_article = object[target_index - 1]
        comments = session.query(Comment).filter_by(article_id=article.id).order_by("-create_time")
        content["tag_list"] = article.tag.split("、")
        content["Article"] = article,
        content["like"] = like.count()
        content["pre_article"] = pre_article
        content["next_article"] = next_article
        content["comments"] = comments
        content["content"] = article.content
        self.render("home/detail.html", **content)


class Gbooks(RequestHandler):
    def get(self, *args, **kwargs):
        content = public()
        content["gbooks"] = session.query(Gbook).order_by("-create_time").all()[:10]
        self.render("home/gbook.html", **content)


class Add_gbook(RequestHandler):
    def get(self, *args, **kwargs):
        pass
    def post(self, *args, **kwargs):
        username = self.get_argument("name")
        email = self.get_argument("email")
        content = self.get_argument("lytext")
        visitor_id = session.query(Visitor).filter_by(ip=self.request.remote_ip)[0].id
        gbook = Gbook(username=username, email=email, content=content, visitor_id=visitor_id)
        session.add(gbook)
        session.commit()
        self.redirect("/gbook")


class Add_comment(RequestHandler):
    def get(self):
        article_id = self.get_argument("target")
        content = self.get_argument("content")
        remote = self.request.remote_ip
        visitor = session.query(Visitor).filter_by(ip=remote)[0]
        comment = Comment(article_id=article_id, visitor_id=visitor.id, content=content)
        session.add(comment)
        session.commit()
        content = {
            "status": "1",
        }
        self.finish(content)


class Add_Like(RequestHandler):
    def get(self, *args, **kwargs):
        article_id = self.get_argument("target")
        remote = self.request.remote_ip
        visitor = session.query(Visitor).filter_by(ip=remote)[0]
        if session.query(Like).filter_by(article_id=article_id, visitor_id=visitor.id).count() == 0:
            like = Like(article_id=article_id, visitor_id=visitor.id)
            session.add(like)
            session.commit()
            content = {
                "status": "1",
            }
            self.finish(content)
        else:
            content = {
                "status": "2",
            }
            self.finish(content)

