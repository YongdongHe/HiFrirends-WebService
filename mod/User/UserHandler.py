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

	def post(self,urlparam):
		user = self.get_current_user()
		if urlparam == 'info':
			#修改个人信息
			self.changeInfo(user)

	def getInfo(self,user):
		if user == None:
			return
		response = {'code':'','content':{}}
		response['code']=200
		response['content']['phone']=user.user_phone
		response['content']['name']=user.user_name
		self.write(response)

	def changeInfo(self,user):
		if user == None:
			return
		response = {'code':'','content':''}
		name = self.get_argument('name')
		user.user_name = name
		try:
			self.db.add(user)
			self.db.commit()
			response['code']=200
			response['content']='修改成功。'
		except Exception as e:
			print str(e)
			response['code']=500
			response['content']='服务器发生了未知错误。'
		self.write(response)