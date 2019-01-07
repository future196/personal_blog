import os

options = {
    'port': 8000,
}

settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'cookie_secret': '0Q1AKOKTQHqaa+N80XhYW7KCGskOUE2snCW06UIxXgI=',
    'xsrf_cookies': False,
    'login_url': '/login',
    'debug': True,
    'article_face_path': os.path.join(os.path.dirname(__file__), 'static/img/article_face'),
    'article_img_path': os.path.join(os.path.dirname(__file__), 'static/img/article_img'),
}
