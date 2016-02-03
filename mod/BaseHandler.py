#coding=utf8
import random
import tornado.web
from sqlalchemy.orm import scoped_session, sessionmaker
from mod.databases.db import engine
from mod.databases.tables import User
from mod.databases.tables import Activity
from mod.databases.tables import Partner
from mod.databases.tables import UUUID

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		_uuid = self.get_argument('uuid',default=None)
		uuid = self.db.query(UUUID).filter(UUUID.uuuid == _uuid).first()
		if uuid == None:
			response = {'code':401,'content':'认证信息错误或者已经过期，请重新登录。'}
			self.write(response)
			self.finish()
		else:
			return self.db.query(User).filter(User.id == uuid.user_id).first()
	@property
	def db(self):
		return self.application.db

	@property
	def auth(self):
		return self.application.auth
	def on_finish(self):
		self.db.close()


	def writeError(self,code,msg):
		response = {'code':code,'content':msg}
		self.write(response)

