import hmac
import hashlib
import base64
import datetime
import sys

#JSON格式注意区分大小写
#使用命令： python createtoken.py client_id client_pwd acc_id acc_token expire_time
#client_id client账号
#client_pwd client的密码
#acc_id 主账号
#acc_token 主账号的token
#expire_time UTC时间 比北京时间晚8个小时，格式：20140605184430
def create(client_id,client_pwd,acc_id,acc_token,expire_time=None):
	#超时时间格式：20140605184430。不设置该参数的话默认从现在开始有效期两天
	if expire_time == None:
		expire_time = (datetime.datetime.utcnow() + datetime.timedelta(days =2)).strftime("%Y%m%d%H%S%M")
	head = '{"Alg":"HS256","Accid":"%s","Cnumber":"%s","Expiretime":"%s"}'%\
	       (acc_id,client_id,expire_time)
	#print("head:",head)
	body = '{"Accid":"%s","AccToken":"%s","Cnumber":"%s","Cpwd":"%s","Expiretime":"%s"}'%\
	       (acc_id,acc_token,client_id,client_pwd,expire_time)
	#print("body:",body)
	#HMAC+SHA256 认证方式。key为主账号的token
	body_bytes = hmac.new(acc_token.encode('utf-8'),body.encode('utf-8'),hashlib.sha256)
	#print(body_bytes.digest())
	#base64编码
	body_bytes = base64.b64encode(body_bytes.digest())
	head = base64.b64encode(head.encode('utf-8'))
	print(head+b"."+body_bytes)
	return head+b"."+body_bytes

def main():
	length = len(sys.argv)
	if length == 5:
		create(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
	if length == 6:
		create(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
	

if __name__ == "__main__":
	main()