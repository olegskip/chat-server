from logging_file import log
from database_handler import database
from users_handler import users
from user import User
import json
from message import Message


class SingleConnection():
	def __init__(self, connection, addr):
		self.connection = connection
		self.addr = addr
		self.ip = addr[0]

	def send_data(self, data):
		self.connection.send(data.encode())
		log.write_log("[SEND] " + data + " to " + self.str_data())

	def str_data(self):
		return "[ " + self.ip + " " + self.os_name + " ]"

	def log_in_user(self, login, password):
		auth_result = database.check_for_auth(login, password)
		if auth_result:
			users.append(User(login))
			database.set_online_status(login, 1)
			database.set_log_in_status(login, 1)

		response = {
			"request": "LOG_IN_USER",
			"login": login,
			"result": auth_result
		}

		log.write_log("[NEW USER] Attempt to add the new user = \"" + login + ":" + password + "\" result = " + str(auth_result) + ", from " + self.str_data())

		# return the result appending the user
		self.send_data(json.dumps(response, separators=(',', ':')))
		return auth_result

	def check_exists_user(self, email, login):
		is_exist = database.check_exists_user(email, login)
		response = {
			"request": "CHECK_EXISTS_USER",
			"login": login,
			"result": is_exist
		}

		self.send_data(json.dumps(response, separators=(',', ':')))
		return is_exist

	def sign_up_user(self, email, login, password):
		result = False
		if not database.check_exists_user(email, login):
			result = True
			database.sign_up_user(email, login, password)

		response = {
			"request": "SIGN_UP_USER",
			"login": login,
			"result": result
		}
		return response		

	def log_out_user(self, login):
		users.delete_by_name(login)
		database.set_online_status(login, 0)
		database.set_log_in_status(login, 0)
		response = {
			"request": "LOG_OUT_USER",
			"name": login,
			"result": str(1)
		}

		log.write_log("[NEW USER] Log out the user = \"" + login + "\" result = " + str(1) + ", from " + self.str_data())
		self.send_data(json.dumps(response, separators=(',', ':')))		

	def disconnect_user(self, login):
		users.delete_by_name(login)
		database.set_online_status(login, 0)
		response = {
			"request": "DISCONNECT_USER",
			"name": login,
			"result": str(1)
		}

		log.write_log("[NEW USER] Log out the user = \"" + login + "\" result = " + str(1) + ", from " + self.str_data())
		self.send_data(json.dumps(response, separators=(',', ':')))

	def send_message(self, message):
		user = users.get_user(message.login)
		#user.messages.append(Message(login, message))

		log.write_log("[MESSAGE] New message, login = \"" + message.login + "\"" + " , text = " + message.text + ", from " + self.str_data())
		response = {
			"request": "UPDATE_MESSAGES",
			"author": message.login,
			"message": message.text,
			"color": user.color
		}
		
		return json.dumps(response, separators=(',', ':'))

	def send_messages(self, messages):
		output = ""
		for message in messages:
			user = users.get_user(message.login)
			if user:
				response = {
					"request": "UPDATE_MESSAGES",
					"author": message.login,
					"message": message.text,
					"color": user.color
				}
				
				output += json.dumps(response, separators=(',', ':'))
			
		self.send_data(output)
		return output

	def send_server_message(self, message):
		response = {
			"request": "UPDATE_MESSAGES",
			"author": "Server",
			"message": message,
			"color": "#ed0c0c"
		}
		self.send_data(json.dumps(response, separators=(',', ':')))

	def send_big_notify(self, text):
		response = {
			"request": "BIG_NOTIFY",
			"title": "Server information",
			"text": text
		}
		self.send_data(json.dumps(response, separators=(',', ':')))		

	def kick(self):
		print("KICK KICK KICK!")

	connection = None
	addr = None
	ip = ""
	init_ip = ""
	os_name = "None"
