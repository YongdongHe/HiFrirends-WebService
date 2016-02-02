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
							'title':activity.title,
							'label':activity.label,
							'leader':activity.leader,
							'time':time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(activity.time)),
							'content':activity.content
						})
				response['code']=200
			except Exception as e:
				response['code']=500
				print str(e)
				self.db.rollback()
			self.write(response)
		elif types == 'status':
			#根据activity id 获得某个id的具体情况
			activity_id = self.get_argument('activity_id')
			activity = self.db.query(Activity).filter(Activity.id == activity_id).first()
			response = {}
			if activity == None:
				response['code']=404
				response['content']='该活动不存在或者已被删除。'
				self.write(response)
				return
			response = {'code':'','content':{
				'activity_id':activity_id,
				'title':activity.title,
				'label':activity.label,
				'leader':activity.leader,
				'time':time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(activity.time)),
				'content':activity.content,
				'partners':[]
			}}
			partners = self.db.query(Partner).filter(Partner.activity_id == activity_id)
			for each_partner in partners:
				response['content']['partners'].append({
					'id':each_partner.user_id,
					'name':each_partner.user_name,
					'phone':each_partner.user_phone
				})
			response['code']=200
			self.write(response)

	def post(self,types):
		response = {'code':'','content':''}
		user = self.get_current_user()
		print str(user.user_phone)
		#发布活动
		if types == 'publish':
			try:
				title = self.get_argument('title')
				content = self.get_argument('content',default=None)
				label = self.get_argument('label')
				leader = user.user_name
				activity = Activity(
					title = title,
					label = label,
					leader = leader,
					time = time.time(),
					content = content)
				print activity.time
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
		elif types == 'join':
			try:
				activity_id = self.get_argument('activity_id')
				attender = user.user_name
				partner = Partner(
					activity_id = activity_id,
					user_id = user.id,
					user_name = user.user_name,
					user_phone = user.user_phone)
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




