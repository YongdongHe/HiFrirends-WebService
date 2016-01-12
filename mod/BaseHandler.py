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
		_uuid = self.get_argument('uuid')
		uuid = self.db.query(UUUID).filter(UUUID.uuid == _uuid).first()
		if uuid == None:
			response = {'code':401,'content':'Unauthorized.'}
			self.wirte(response)
			self.finish()
		else:
			return self.db.query(User).filter(User.id == uuid.user_id).first()
	@property
	def db(self):
		return self.application.db