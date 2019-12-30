import socket

from _thread import *
from single_connection import SingleConnection
from users_handler import users
from user import User
import json
from logging_file import log, log_chat
from database_handler import database
from settings_file import settings_file
from admin_command import Admin_Command
from message import Message


class Server:
	def __init__(self, port):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind(('', port))
		self.clients = []
		self.messages = []
		self.port = port
		self.is_paused = False

		log.write_log("Server is started!")
		
	sock = None
	clients = []
	messages = []
	port = 0
	is_paused = False

	def get_client_data(self, client):
		while True:
			try:
				data = client.connection.recv(4096).decode('utf-8').split("}")
				if self.is_paused:
					continue

				for item in data[:-1]:
					item += "}"
					log.write_log("[RECEIVE] " + item)
					item = json.loads(item)

					request = item["request"]
					if request == "INIT": # the first message
						client.os_name = item["os_name"]

					else:
						login = item["login"]
					
						if request == "LOG_IN_USER":
							password = item["password"]
							
							if client.log_in_user(login, password):
								if settings_file.params["is_show_connect_message"]:
									self.send_server_message_to_all(login + " is connected!")
								if settings_file.params["is_show_old_messages"]:
									client.send_messages(self.messages)								

						elif request == "SIGN_UP_USER":
							email = item["email"]
							password = item["password"]
							client.sign_up_user(email, login, password)

						elif request == "CHECK_EXISTS_USER":
							email = item["email"]
							client.check_exists_user(email, login)

						elif request == "SEND_MESSAGE":
							message_text = item["text"]
							self.messages.append(Message(login, message_text))
							database.append_message(Message(login, message_text))
							self.send_message_to_all(client.send_message(Message(login, message_text)))

						elif request == "ADMIN_COMMAND":
							command = item
							
						elif request == "LOG_OUT_USER":
							client.log_out_user(login)

						elif request == "DISCONNECT_USER":
							client.disconnect_user(login)

						elif request == "GET_USER_INFO":
							client.send_data(json.dumps(database.get_user_info(login), separators=(',', ':')))

						elif request == "UPDATE_USER_INFO":
							database.update_user_info(item)
			
			except ConnectionResetError:
				#print("Disconnected " + client.str_data())
				log.write_log("[CONNECT] Disconnected " + client.str_data())
				self.clients.remove(client)
				break

	def send_server_message_to_all(self, text):
		log.write_log("[SERVER_MESSAGE] New server message: text = " + text)
		for client in self.clients:
			client.send_server_message(text)

	def send_message_to_all(self, text):
		for client in self.clients:
			client.send_data(text)

	def send_big_notify_to_all(self, text):
		for client in self.clients:
			client.send_big_notify(text)

	def pause(self, status):
		if status:
			server.send_big_notify_to_all(settings_file.params["server_pause_message"])
		self.is_paused = status

	def start_listening(self):
		self.sock.listen(99) 

		while True:
			self.clients.append(SingleConnection(*self.sock.accept()))
			#print("New connection from " + self.clients[-1].str_data())
			log.write_log("[CONNECT] Connect " + self.clients[-1].str_data())
			if self.is_paused:
				server.send_big_notify_to_all(settings_file.params["server_pause_message"])

			start_new_thread(self.get_client_data, (self.clients[-1],))

server = Server(6666)
