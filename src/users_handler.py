from message import Message


class UsersHandler:
	def __init__(self):
		self.users = []
		self.messages = []

	def append(self, new_user):
		for user in self.users:
			if new_user.login == user.login:
				return False

		self.users.append(new_user)
		return True

	def get_user(self, login):
		for user in self.users:
			if user.login == login:
				return user

	def kick(self, login):
		self.get_user(login).is_auth = False

	def delete_by_name(self, login):
		for user in self.users:
			if user.login == login:
				self.users.remove(user)
				break
		
	users = []
	messages = []

users = UsersHandler()
