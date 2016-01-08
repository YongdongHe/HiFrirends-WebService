import random
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from sqlalchemy.orm import scoped_session, sessionmaker
from mod.databases.db import engine
from mod.RegisterHandler import RegisterHandler
from mod.ActivityHandler import ActivityHandler
from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
        (r"/", IndexHandler),
        (r"/register",RegisterHandler),
        (r"/activity/(\w+)",ActivityHandler),
        ]
        settings = dict(
            debug=True,
            cookie_secret="365B3932BBBA6182B2D899B494468874",
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = scoped_session(sessionmaker(bind=engine,
                                              autocommit=False, autoflush=True,
                                              expire_on_commit=False))

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hi!Friends!")


if __name__ == '__main__':
    tornado.options.parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
