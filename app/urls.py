from tornado.web import Application
from app import settings
from app.home import IndexHandler as home
from app.admin import IndexHandler as admin

Urls = Application(
    [
        (r"/", home.Index),
        (r"/article", home.Detail),
        (r"/gbook", home.Gbooks),
        (r"/add_comment", home.Add_comment),
        (r"/add_like", home.Add_Like),
        (r"/add_gbook", home.Add_gbook),

        (r"/admin", admin.Login),
        (r"/admin/login", admin.Login),
        (r"/admin/index", admin.Index),
        (r"/admin/article", admin.Articles),
        (r"/admin/comment", admin.Comments),
        (r"/admin/gbook", admin.Gbooks),
        (r"/admin/add_article", admin.Add_article),
        (r"/admin/article_modify", admin.article_modify),
        (r"/admin/delete_article", admin.Delete_article),
        (r"/admin/gbook_reply", admin.Gbook_reply),
        (r"/admin/loginlog", admin.Login_logs),
        (r"/admin/visitor_record", admin.Visit_record),
        (r"/admin/logout", admin.Logout),
    ],
    static_path=settings.settings["static_path"],
    template_path=settings.settings["template_path"],
)
