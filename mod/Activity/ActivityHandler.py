#coding=utf8
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
			response = {'code':'','activities':[]}
			try:
				activitys = self.db.query(Activity).order_by(Activity.time).all()[::-1]
				for activity in activitys:
					response['activities'].append(
						{
							'id':activity.id,
							'activity':activity.activity,
							'leader':activity.leader,
							'time':activity.time,
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
		#发布活动
		if types == '1':
			try:
				des = self.get_argument('des')
				act = self.get_argument('activity',default=None)
				leader = user.user_name	
				print time.time()
				activity = Activity(
					activity=act,
					leader = leader,
					time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),
					description = des)
				self.db.add(activity)
				self.db.commit()
				response['content']='发布活动成功。赶紧去给好友们分享吧'
				response['code']=200	
			except Exception as e:
				print str(e)
				response['content']='发布活动失败。'
				response['code']=500
			self.write(response)
		#参加活动
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
				response['content']='成功参与活动。'
				response['code']=200
			except Exception as e:
				print str(e)
				response['content']='参与活动失败。'
				response['code']=500
			self.write(response)
		else:
			response['content']='错误的url.'
			response['code']=500
			self.write(response)




