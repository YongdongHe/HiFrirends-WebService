# HiFrirends-WebService
web service for app 'hifriends'


API列表
----------


## 授权  
####获取注册验证码 

		url: 			/auth/getcode
		type:			post
		description:	//获得验证码
		param:
		{
			phone:''    //用户手机号
		}

####注册用户
		url: 			/auth/doregister
		type:			post
		description:	注册用户
		param:
		{
			phone:	''
			captha：''
			psd:	''
		}


####注册用户
		url: 			/auth/dolog
		type:			post
		description:	登录
		param:
		{
			phone:	''
			psd:	''
		}

## 活动
####获取所有活动的列表
		url:			activity/list
		type:			get
		description:	获取所有活动的列表
		param:			none

####发布活动
		url:			activity/publish
		type:			post
		description:	发布活动
		param:			
		{
			title: 	活动标题
			content:活动内容
			label: 	活动标签
			uuid:	用户uuid	
		}


####参与活动
		url:			activity/join
		type:			post
		description:	参与活动
		param:			
		{
			id:		参与活动的id
			uuid:	用户uuid
		}
