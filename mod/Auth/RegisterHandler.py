from mod.BaseHandler import BaseHandler
from mod.databases.tables import User
from mod.databases.tables import Authcode
import uuid
import random
import time
class RegisterHandler(BaseHandler):
	def get(self):
		self.write('Register Page')

	def post(self,types):
		if types == 'getcode':
			self.getCode()
		elif types == 'doregister':
			self.doRegister()	


	def getCode(self):
		#/register/getcode
		response = {'code':'','content':''}
		"""
		url: 			/register/getcode
		type:			get
		description:	get all activities
		param:
		{
			phone:'',
		}
		"""
		user_phone = self.get_argument('phone')
		user_code = ''
		for i in range(6):
			user_code += str(random.randint(0,9))
		code_cache = self.db.query(Authcode).filter(Authcode.phone == user_phone).first()
		if code_cache == None or time.time() >= (code_cache.create_time + 30*1000):
			#have not get code || next code is enable
			authcode = Authcode(
				phone = user_phone,
				code = user_code,
				create_time = int(time.time())
				)
			if code_cache != None:
				self.db.delete(code_cache)
			try:
				self.db.add(authcode)
				self.db.commit()
				print self.auth.sendCode(user_phone,user_code,5)
				response['code']=200
				response['content']='Get code successfully.'
			except Exception as e:
				print str(e)
				self.rollback()
				response['code']=500
				response['content']='Failed to get auth code.'
		else:
			response['code']=403
			response['content']='Too frequent requests'
		self.write(response)


	def doRegister(self):
		#/register/doregister
		user_name = self.get_argument('name')
		user_phone = self.get_argument('phone')
		user_captha = self.get_argument('captha')
		user = self.db.query(User).filter(
			User.user_name == user_name,
			User.user_phone == user_phone).first()
		if user == None:
			user_uuid = str(uuid.uuid4())
			user = User(user_name=user_name,user_phone=user_phone,uuid=user_uuid)
			try:
				self.db.add(user)
				self.db.commit()
				response['code']=200
				response['content']='Register success.'
			except Exception as e:
				print str(e)
				self.db.rollback()
				response['code']=501
				response['content']='Register failed.'
		else:
			response['code']=403
			response['content']='Existed phone number.'
		self.write(response)


