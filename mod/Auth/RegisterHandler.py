# -*- coding: utf-8 -*- 
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
		valid_time = code_cache.create_time + 30
		if code_cache == None or time.time() >= valid_time:
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
				#print self.auth.sendCode(user_phone,user_code,5)
				response['code']=200
				response['content']='获取验证码成功。'
			except Exception as e:
				print str(e)
				self.rollback()
				response['code']=500
				response['content']='服务器发生了未知错误。'
		else:
			response['code']=403
			response['content']='请求验证码太过频繁，请稍后再试。'
		self.write(response)


	def doRegister(self):
		#/register/doregister
		user_name = self.get_argument('name')
		user_phone = self.get_argument('phone')
		user_captha = self.get_argument('captha')
		user = self.db.query(User).filter(
			User.user_name == user_name,
			User.user_phone == user_phone).first()
		if user != None:
			response['code']=403
			response['content']='此手机号已被注册。'
			self.write(response)
			self.finish()
		cache_code = self.db.query(Authcode).filter(Authcode.phone == user_phone).first()
		valid_time = cache_code.create_time + 60*5;
		if cache_code == None or time.time() >= valid_time:
			response['code']=403
			response['content']='验证码已失效，请重新获取。'
			self.write(response)
			self.finish()
		if user_captha == cache_code.code:
			user_uuid = str(uuid.uuid3(user_phone))
			user = User(user_name=user_name,user_phone=user_phone,uuid=user_uuid)
			try:
				self.db.add(user)
				self.db.commit()
				response['code']=200
				response['content']=user_uuid
			except Exception as e:
				print str(e)
				self.db.rollback()
				response['code']=500
				response['content']='注册失败，服务器发生了未知错误。'
			self.write(response)


