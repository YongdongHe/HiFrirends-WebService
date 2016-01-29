#coding=utf8
from mod.BaseHandler import BaseHandler
class UserHandler(BaseHandler):
	def get(self,urlparam):
		user = self.get_current_user()
		if urlparam == 'info':
			#获得用户个人信息
			self.getInfo(user)
		else:
			self.writeError(404,"错误的url.")

	def getInfo(user):
		if user == None:
			return
		response = {'code':'','content':''}
		response['code']=200
		response['content']['phone']=user.user_phone
		response['content']['name']=user.user_name
		self.write(response)