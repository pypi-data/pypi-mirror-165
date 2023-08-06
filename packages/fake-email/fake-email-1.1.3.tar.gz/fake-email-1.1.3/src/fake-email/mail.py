import requests,json,random,time


class Email:
	def __init__(self,session=None):
		self.session = session			
		self.request = requests.session()		
		
	def Mail(self):
		self.Buildsession =user = str("".join(random.choice("qwertyuiopasdfghjklzxcvbnm0987654321")for i in range(26)))		
		email = self.request.get(f"https://10minutemail.net/address.api.php?new=1&sessionid={self.Buildsession}&_=1661770438359").json()
		
		datajson={"mail":email["permalink"]["mail"],"session":email["session_id"]}		
		return datajson
	def inbox(self,loop=False):
		time.sleep(0.20) 		
		if self.session : 
			sessinbox = self.session	
		elif self.session ==None :
			sessinbox = self.Buildsession
		data = self.request.get(f"https://10minutemail.net/address.api.php?sessionid={sessinbox}&_=1661770438359").json()
		
		if len(data["mail_list"]) !=1:				 
			address =data["mail_list"][0]["subject"]
			id=data["mail_list"][0]["mail_id"]
			box = self.request.get(f"https://10minutemail.net//mail.api.php?mailid={id}&sessionid={sessinbox}").json()
			plain =box["plain_link"]
			datetime=["datetime"]
			to =box["to"]
			name=box["header_decode"]["replylist"][0]["name"]
			amli=box["header_decode"]["replylist"][0]["address"]
			datainbox ={"topic":address,"name":name,"from":amli,"to":to,"message":plain[0],"datetime":datetime}	
			return datainbox
										

