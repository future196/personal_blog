# -*- coding: utf-8 -*-
from tornado.web import RequestHandler
import hashlib
from app.models import Personal, Article, Comment, Login_log, Gbook, Article_type, Tag, Recommend, Like, Read, Visit_Record
from app.sqlalchemy_db import session
import time
import os
from app.settings import settings
session = session()



class Login(RequestHandler):
    def get(self):
        content = {
            "status": 1,
            "username": "",
            "password": "",
        }
        self.render("admin/index.html", **content)

    def post(self):
        account = self.get_argument("username")
        password = self.get_argument("userpwd")
        content = {
            "username": account,
            "password": password,
        }
        m = hashlib.md5()
        m.update(bytes(password, encoding="utf-8"))
        password = m.hexdigest()
        if session.query(Personal).filter_by(account=account, password=password).count() == 1:
            log = Login_log(ip=self.request.remote_ip, admin=account)
            session.add(log)
            session.commit()
            self.set_cookie("admin", account)
            self.redirect("/admin/index")
        else:
            content["status"] = 2
        self.render("admin/index.html", **content)



class Index(RequestHandler):
    def get(self):
        if self.get_cookie("admin"):
            pass
        else:
            self.redirect("/admin")
        article_number = session.query(Article).filter().count()
        comment_number = session.query(Comment).filter().count()
        login_number = session.query(Login_log).filter().count()
        last_login = session.query(Login_log).filter()[login_number-2]
        content = {
            "article_number": article_number,
            "comment_number": comment_number,
            "username": self.get_cookie("admin"),
            "login_number": login_number,
            "last_login": last_login,
            "is_index": 1,
            "is_article": 0,
            "is_comment": 0,
            "is_gbook": 0,
            "is_loginlog": 0,
            "is_visit_record": 0,
        }
        self.render("admin/main.html", **content)


class Articles(RequestHandler):

    def get(self, *args, **kwargs):
        if self.get_cookie("admin"):
            pass
        else:
            self.redirect("/admin")
        articles = session.query(Article).filter().order_by("-create_time")
        content = {
            "username": self.get_cookie("admin"),
            "articles": articles,
            "is_index": 0,
            "is_article": 1,
            "is_comment": 0,
            "is_gbook": 0,
            "is_loginlog": 0,
            "is_visit_record": 0,
        }
        self.render("admin/article.html", **content)


class Add_article(RequestHandler):
    def get(self, *args, **kwargs):
        if self.get_cookie("admin"):
            pass
        else:
            self.redirect("/admin")
        article_type = session.query(Article_type).filter()
        tags = session.query(Tag).filter()
        content = {
            "username": self.get_cookie("admin"),
            "article_type": article_type,
            "is_index": 0,
            "is_article": 1,
            "is_comment": 0,
            "is_gbook": 0,
            "is_loginlog": 0,
            "is_visit_record": 0,
            "tags": tags,
        }
        self.render("admin/add-article.html", **content)
    def post(self, *args, **kwargs):
        if self.get_cookie("admin"):
            pass
        else:
            self.redirect("/admin")
        content = self.get_argument("content")
        title = self.get_argument("title")
        intro = self.get_argument("describe")
        keyboards = self.get_argument("keywords")
        type = self.get_argument("category")
        tagss = self.get_arguments("article_tag")
        author = self.get_argument("author")
        face_exist = self.request.files.get("face", None)
        if session.query(Article).filter_by(title=title).count() == 0:
            tag_list = keyboards
            if keyboards:
                if "，" in keyboards:
                    key_list = keyboards.split("，")
                    for k in key_list:
                        tag = Tag(name=k)
                        session.add(tag)
                        session.commit()
                else:
                   tag = Tag(name=keyboards)
                   session.add(tag)
                   session.commit()
            for t in tagss:
                ta = session.query(Tag).get(t).name
                tag_list = tag_list + ta + "、"
            # 存储文章图片
            for i in range(5):
                try:
                    img = self.request.files["img%s" % str(i + 1)]
                    for meta in img:
                        filename = str(i+1) + title + "." + meta['filename'].split(".")[-1]
                        filepath = os.path.join(settings["article_img_path"], filename)
                        with open(filepath, 'wb') as up:  # 有些文件需要已二进制的形式存储，实际中可以更改
                            up.write(meta['body'])
                except:
                    pass
                finally:
                    pass

            # 存储文章封面
            if face_exist:
                face = self.request.files["face"]
                for meta in face:
                    filename = title + "." + meta['filename'].split(".")[-1]
                    filepath = os.path.join(settings["article_face_path"], filename)
                    with open(filepath, 'wb') as up:
                        up.write(meta['body'])
                        article = Article(title=title, intro=intro, content=content, author=author, read=0, type_id=type, tag=tag_list[:-1], face_img=filename)
                        session.add(article)
                        session.commit()
                        self.redirect("/admin/article")
            else:
                article = Article(title=title, intro=intro, content=content, author=author, read=0, type_id=type, tag=tag_list[:-1])
                session.add(article)
                session.commit()
                self.redirect("/admin/article")
        else:
            article_type = session.query(Article_type).filter()
            tags = session.query(Tag).filter()
            content = {
                "username": self.get_cookie("admin"),
                "article_type": article_type,
                "is_index": 0,
                "is_article": 1,
                "is_comment": 0,
                "is_gbook": 0,
                "is_loginlog": 0,
                "is_visit_record": 0,
                "tags": tags,
            }
            self.render("admin/add-article.html", **content)




class Comments(RequestHandler):
    def get(self, *args, **kwargs):
        if self.get_cookie("admin"):
            pass
        else:
            self.redirect("/admin")
        comments = session.query(Comment).filter().order_by("-create_time")
        content = {
            "username": self.get_cookie("admin"),
            "comments": comments,
            "is_index": 0,
            "is_article": 0,
            "is_comment": 1,
            "is_gbook": 0,
            "is_loginlog": 0,
            "is_visit_record": 0,
        }
        self.render("admin/comment.html", **content)


class Gbooks(RequestHandler):
    def get(self, *args, **kwargs):
        if self.get_cookie("admin"):
            pass
        else:
            self.redirect("/admin")
        gbooks = session.query(Gbook).filter().order_by("-create_time")
        content = {
            "username": self.get_cookie("admin"),
            "gbooks": gbooks,
            "is_index": 0,
            "is_article": 0,
            "is_comment": 0,
            "is_gbook": 1,
            "is_loginlog": 0,
            "is_visit_record": 0,
        }
        self.render("admin/gbook.html", **content)



class article_modify(RequestHandler):
    def get(self, *args, **kwargs):
        if self.get_cookie("admin"):
            pass
        else:
            self.redirect("/admin")
        target = self.get_argument("target")
        article_type = session.query(Article_type).filter()
        tags = session.query(Tag).filter()
        article = session.query(Article).get(target)
        content = {
            "username": self.get_cookie("admin"),
            "article_type": article_type,
            "article": article,
            "is_index": 0,
            "is_article": 1,
            "is_comment": 0,
            "is_gbook": 0,
            "is_loginlog": 0,
            "is_visit_record": 0,
            "tags": tags,
        }
        self.render("admin/article_modify.html", **content)

    def post(self, *args, **kwargs):
        if self.get_cookie("admin"):
            pass
        else:
            self.redirect("/admin")
        target = self.get_argument('target')
        article = session.query(Article).get(target)
        content = self.get_argument("content")
        title = self.get_argument("title")
        intro = self.get_argument("describe")
        # keyboards = self.get_argument("keywords")
        type = self.get_argument("category")
        tagss = self.get_arguments("article_tag")
        author = self.get_argument("author")
        # face_exist = self.request.files.get("face", None)
        # if session.query(Article).filter_by(title=title).count() == 0:
        #     tag_list = keyboards
        #     if keyboards:
        #         if "，" in keyboards:
        #             key_list = keyboards.split("，")
        #             for k in key_list:
        #                 tag = Tag(name=k)
        #                 session.add(tag)
        #                 session.commit()
        #         else:
        #             tag = Tag(name=keyboards)
        #             session.add(tag)
        #             session.commit()
        #     for t in tagss:
        #         ta = session.query(Tag).get(t).name
        #         tag_list = tag_list + "、" + ta
            # 存储文章图片
        for i in range(5):
            try:
                img = self.request.files["img%s" % str(i + 1)]
                for meta in img:
                    filename = str(i + 1) + title + "." + meta['filename'].split(".")[-1]
                    filepath = os.path.join(settings["article_img_path"], filename)
                    with open(filepath, 'wb') as up:  # 有些文件需要已二进制的形式存储，实际中可以更改
                        up.write(meta['body'])
            except:
                pass
            finally:
                pass


        tags = ""
        for tag in tagss:
            tags = tags + session.query(Tag).get(tag).name + "、"

        article.content = content
        article.author = author
        article.title = title
        article.intro = intro
        article.type_id = type
        article.tag = tags[:-1]
        face_exist = self.request.files.get("face", None)
        if face_exist:
            # 存储文章封面
            try:
                face = self.request.files["face"]
                for meta in face:
                    filename = title + "." + meta['filename'].split(".")[-1]
                    filepath = os.path.join(settings["article_face_path"], filename)
                    with open(filepath, 'wb') as up:
                        up.write(meta['body'])
                        article.face_img = filename
                        session.add(article)
                        session.commit()
            except:
                pass
            finally:
                pass
        else:
            session.add(article)
            session.commit()
        self.redirect("/admin/article")


class Delete_article(RequestHandler):
    def get(self):
        if self.get_cookie("admin"):
            pass
        else:
            self.redirect("/admin")
        target = self.get_argument("target")
        article = session.query(Article).get(target)
        if session.query(Recommend).filter_by(article_id=target).count() != 0:
            for recomend in session.query(Recommend).filter_by(article_id=target):
                session.delete(recomend)
                session.commit()
        if session.query(Like).filter_by(article_id=target).count() == 1:
            for like in session.query(Like).filter_by(article_id=target):
                session.delete(like)
                session.commit()
        if session.query(Read).filter_by(article_id=target).count() != 0:
            for read in session.query(Read).filter_by(article_id=target):
                session.delete(read)
                session.commit()
        if session.query(Comment).filter_by(article_id=target).count() != 0:
            for comment in session.query(Comment).filter_by(article_id=target):
                session.delete(comment)
                session.commit()
        session.delete(article)
        session.commit()
        content = {
            "status": 1,
        }
        self.finish(content)


class Gbook_reply(RequestHandler):
    def post(self, *args, **kwargs):
        if self.get_cookie("admin"):
            pass
        else:
            self.redirect("/admin")
        content = self.get_argument("reply_content")
        target = self.get_argument("target")
        gbook = session.query(Gbook).get(target)
        gbook.reply = content
        session.add(gbook)
        session.commit()
        self.redirect("/admin/gbook")

class Login_logs(RequestHandler):
    def get(self, *args, **kwargs):
        if self.get_cookie("admin"):
            pass
        else:
            self.redirect("/admin")
        logs = session.query(Login_log).filter().order_by("-create_time")
        content = {
            "username": self.get_cookie("admin"),
            "logs": logs,
            "is_index": 0,
            "is_article": 0,
            "is_comment": 0,
            "is_gbook": 0,
            "is_loginlog": 1,
            "is_visit_record": 0,
        }
        self.render("admin/loginlog.html", **content)


class Visit_record(RequestHandler):
    def get(self, *args, **kwargs):
        if self.get_cookie("admin"):
            pass
        else:
            self.redirect("/admin")
        records = session.query(Visit_Record).filter().order_by("-create_time")
        print(records)
        content = {
            "username": self.get_cookie("admin"),
            "records": records,
            "is_index": 0,
            "is_article": 0,
            "is_comment": 0,
            "is_gbook": 0,
            "is_loginlog": 0,
            "is_visit_record": 1,
        }
        self.render("admin/visitor_record.html", **content)


class Logout(RequestHandler):
    def get(self):
        self.set_cookie("admin", "", expires=time.time() + 1)
        self.redirect("/admin")

