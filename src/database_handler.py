import sqlite3
from settings_file import get_exe_path
import threading
from users_handler import users


class Database_Handler:
	def __init__(self, path):
		self.connection = sqlite3.connect(path, check_same_thread = False)
		self.cursor = self.connection.cursor()

	def check_for_auth(self, login, password):
		if self.cursor.execute("SELECT password FROM users WHERE login=?;", [login]).fetchall():
			true_password = self.cursor.execute("SELECT password FROM users WHERE login=?;", [login]).fetchall()[0][0]
			if password == true_password:
				return True

		return False

	def get_user_info(self, login):
		if self.cursor.execute("SELECT login FROM users WHERE login=?;", [login]).fetchall():
			email = self.cursor.execute("SELECT email FROM users WHERE login=?;", [login]).fetchall()[0][0]
			color = self.cursor.execute("SELECT color FROM users WHERE login=?;", [login]).fetchall()[0][0]
			info = {
				"request": "GET_USER_INFO",
				"login": login,
				"email": email,
				"color": color,
			}
			return info	
			
	def update_user_info(self, request):
		login = request["login"]

		if self.cursor.execute("SELECT login FROM users WHERE login=?;", [login]).fetchall():
			user = users.get_user(login)
			password = request["password"]
			if password:
				print(password)
				self.cursor.execute("UPDATE	users SET password=? WHERE login=?;", (password, login))
				self.connection.commit()

			color = request["color"]
			if color:
				self.cursor.execute("UPDATE	users SET color=? WHERE login=?;", (color, login, ))
				user.color = color

	def set_online_status(self, login, status):
		self.cursor.execute("UPDATE users SET isOnline=? WHERE login=?;", (str(status), login))
		self.connection.commit()

	def set_log_in_status(self, login, status):
		self.cursor.execute("UPDATE users SET isLogIn=? WHERE login=?;", (str(status), login))
		self.connection.commit()		

	def check_exists_user(self, email, login):
		email_exists = self.cursor.execute("SELECT id FROM users WHERE email=?;", [email]).fetchall()
		login_exists = self.cursor.execute("SELECT id FROM users WHERE login=?;", [login]).fetchall()
		return not(not bool(email_exists) and not bool(login_exists))

	def sign_up_user(self, email, login, password):
		columns = ["email", "login", "password"]
		statement = "INSERT INTO {0} ({1}, {2}, {3}) VALUES(?, ?, ?);".format(self.users_table, columns[0], columns[1], columns[2])
		self.cursor.execute(statement, [email, login, password])
		self.connection.commit()

		return True

	def append_message(self, message):
		columns = ["author", "text", "time"]
		statement = "INSERT INTO {0} ({1}, {2}, {3}) VALUES(?, ?, ?);".format("messages", columns[0], columns[1], columns[2])
		self.cursor.execute(statement, [message.login, message.text, message.time])
		self.connection.commit()	

	connection = None
	cursor = None
	users_table = "users"

database = Database_Handler(get_exe_path() + '\\database\\database.db')
