from mod.BaseHandler import BaseHandler
from mod.databases.tables import Activity
from mod.databases.tables import Partner
from mod.databases.tables import User
import time
class ActivityHandler(BaseHandler):
	def get(self,types):
		# get the list of activities
		# user = self.get_current_user()
		# print str(user.id)
		"""
			url:			activity/list
			type:			get
			description:	get all activities
			param:			none
		"""
		if types == 'list':
			response = {'code':'','activitys':[]}
			try:
				activitys = self.db.query(Activity).all()
				for activity in activitys:
					response['activitys'].append(
						{
							'id':activity.id,
							'activity':activity.activity,
							'leader':activity.leader,
							'time':str(activity.time),
							'des':activity.description
						})
				response['code']=200
			except Exception as e:
				response['code']=500
				print str(e)
				self.db.rollback()
			self.write(response)


	def post(self,types):
		response = {'code':'','content':''}
		user = self.get_current_user()
		print str(user.user_phone)
		if types == '1':
			try:
				des = self.get_argument('des')
				act = self.get_argument('activity',default=None)
				leader = user.user_name
				now_time = time.strftime('%Y-%m-%d %X',time.localtime(time.time()))				
				activity = Activity(
					activity=act,
					leader = leader,
					time = now_time,
					description = des)
				self.db.add(activity)
				self.db.commit()
				response['content']='publish activity success'
				response['code']=200	
			except Exception as e:
				print str(e)
				response['content']='publish activity fail'
				response['code']=500
			self.write(response)
		#attend
		elif types == '2':
			try:
				activity_id = self.get_argument('activity_id')
				attender = user.user_name
				partner = Partner(
					activity_id = activity_id,
					user_id = user.id,
					user_name = user.user_name)
				self.db.add(partner)
				self.db.commit()
				response['content']='attend activity success'
				response['code']=200	
			except Exception as e:
				print str(e)
				response['content']='attend activity fail'
				response['code']=500
			self.write(response)
		else:
			response['content']='fail'
			response['code']=500
			self.write(response)




