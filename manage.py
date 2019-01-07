from tornado import httpserver, ioloop, options
from app.urls import Urls


if __name__ == "__main__":
    print(" Server Running...")
    options.parse_command_line()
    http_server = httpserver.HTTPServer(Urls)
    http_server.listen(8888)
    ioloop.IOLoop.instance().start()
