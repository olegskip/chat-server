from time import gmtime, strftime


class Message:
	def __init__(self, login, text):
		self.login = login
		self.text = text
		self.time = strftime("%H:%M:%S %d.%m.%Y", gmtime())	

	login = ""
	text = ""
	time = ""
