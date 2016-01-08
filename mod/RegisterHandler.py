from BaseHandler import BaseHandler
from mod.databases.tables import User
import uuid
class RegisterHandler(BaseHandler):
	def get(self):
		self.write('Register Page')

	def post(self):
		response = {'code':'','content':''}
		user_name = self.get_argument('name')
		user_phone = self.get_argument('phone')
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
				response['code']=304
				response['content']='Register failed.'
		else:
			response['code']=304
			response['content']='Register failed.'
		self.write(response)
