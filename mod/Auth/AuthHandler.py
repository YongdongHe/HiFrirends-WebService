# -*- coding: utf-8 -*- 
from mod.BaseHandler import BaseHandler
from mod.databases.tables import User
from mod.databases.tables import Authcode
from mod.databases.tables import UUUID
import traceback
import uuid
import random
import time
class AuthHandler(BaseHandler):
	def get(self):
		self.write('Register Page')

	def post(self,types):
		if types == 'getcode':
			self.getCode()
		elif types == 'doregister':
			self.doRegister()
		elif types == 'dolog':
			self.doLog()
		else:
			self.writeError(404,"错误的url.")


	def getCode(self):
		#/auth/getcode
		response = {'code':'','content':''}
		"""
		url: 			/auth/getcode
		type:			get
		description:	获得验证码
		param:
		{
			phone:''
		}
		"""
		user_phone = self.get_argument('phone')
		user_code = ''
		for i in range(6):
			user_code += str(random.randint(0,9))
		code_cache = self.db.query(Authcode).filter(Authcode.phone == user_phone).first()
		if code_cache == None or time.time() >= code_cache.create_time + 30:
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
				sendresult = eval(self.auth.sendCode(user_phone,user_code,5))
				print sendresult
				if sendresult['resp']['respCode'] == '000000' :
					response['code']=200
					response['content']='获取验证码成功，请注意查收。'
				elif sendresult['resp']['respCode']=='105122':
					response['code']=403
					response['content']='请求验证码次数过多。'
				else:
					response['code']=403
					response['content']='请输入正确的手机号。'
			except Exception as e:
				traceback.print_exc()
				print str(e)
				self.db.rollback()
				response['code']=500
				response['content']='服务器发生了未知错误。'
		else:
			response['code']=403
			response['content']='请求验证码太过频繁，请稍后再试。'
		self.write(response)


	def doRegister(self):
		#/auth/doregister
		response = {'code':'','content':''}
		user_phone = self.get_argument('phone')
		user_captha = self.get_argument('captha')
		user_psd = self.get_argument('psd')
		user = self.db.query(User).filter(
			User.user_phone == user_phone).first()
		print user
		if user != None:
			response['code']=403
			response['content']='此手机号已被注册。'
			self.write(response)
			return
		cache_code = self.db.query(Authcode).filter(Authcode.phone == user_phone).first()
		if cache_code == None or time.time() >= cache_code.create_time + 60*5:
			response['code']=403
			response['content']='验证码已失效，请重新获取。'
			self.write(response)
			return
		print user_captha
		print cache_code.code
		if user_captha == cache_code.code:
			user = User(user_name=user_phone,user_phone=user_phone,psd=user_psd)
			try:
				self.db.add(user)
				self.db.commit()
				user = self.db.query(User).filter(User.user_phone == user_phone).first()
				user_uuid = str(uuid.uuid4())
				new_uuuid = UUUID(uuuid=user_uuid,user_id=user.id,create_time=time.time())
				self.db.add(new_uuuid)
				self.db.commit()
				response['code']=200
				response['content']='注册成功。'
				response['uuid']=user_uuid
			except Exception as e:
				print str(e)
				self.db.rollback()
				response['code']=500
				response['content']='注册失败，服务器发生了未知错误。'
			self.write(response)
		else:
			response['code']=403
			response['content']='验证码错误，请重新输入。'
			self.write(response)

	def doLog(self):
		response = {'code':'','content':''}
		user_phone = self.get_argument('phone')
		print user_phone
		user_psd = self.get_argument('psd')
		user = self.db.query(User).filter(
			User.user_phone == user_phone).first()
		print user
		if user == None:
			response['code']=403
			response['content']='此手机号未注册，请先注册~'
			self.write(response)
			return
		if user.psd != user_psd:
			response['code']=403
			response['content']='密码错误，请重试'
			self.write(response)
			return
		user_uuid = str(uuid.uuid4())
		old_uuid = self.db.query(UUUID).filter(UUUID.user_id == user.id).first()
		new_uuuid = UUUID(uuuid=user_uuid,user_id=user.id,create_time=time.time())	
		try:
			if old_uuid!= None:
				self.db.delete(old_uuid)
				self.db.commit()
			self.db.add(new_uuuid)
			self.db.commit()
			response['code']=200
			response['content']='登录成功'
			response['uuid']=str(user_uuid)
			self.write(response)
		except Exception as e:
			print str(e)
			self.db.rollback()
			response['code']=500
			response['content']='登录失败，请重试。'
			self.write(response)




