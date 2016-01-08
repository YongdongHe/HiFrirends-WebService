import random
import tornado.web
from sqlalchemy.orm import scoped_session, sessionmaker
from mod.databases.db import engine
from mod.databases.tables import User
from mod.databases.tables import Activity
from mod.databases.tables import Partner

class BaseHandler(tornado.web.RequestHandler):
	@property
	def db(self):
		return self.application.db