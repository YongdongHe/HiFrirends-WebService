#coding=utf8
from mod.BaseHandler import BaseHandler
class UserHandler(BaseHandler):
	def get(self,urlparam):
		user = self.get_current_user()
		if urlparam == 'userinfo':
			#获得用户个人信息
			self.write("ok")

