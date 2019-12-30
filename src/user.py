from message import Message
from database_handler import database


class User:
	def __init__(self, login, is_online=True):
		self.login = login
		self.is_online = is_online

		user_info = database.get_user_info(login)
		self.email = user_info["email"]
		self.color = user_info["color"]
	