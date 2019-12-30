from _thread import *
from users_handler import users
import os
import sys
from logging_file import log
from settings_file import settings_file
from server_class import server


class ConsoleCommand:
	def __init__(self):
		start_new_thread(self.check_for_command, ())
		self.commands_function = { 
			"/online": self.print_online,
			"/cmd": self.cmd,
			"/upset": self.update_settings,
			"/pause": self.pause_server,
			"/unpause": self.unpause_server,
			"/bnot": self.big_notify,
			"/exit": self.exit
		}

	def check_for_command(self):
		while True:
			command = input("")
			solo_command = command.split(" ")[0].strip()
			if solo_command in self.commands_function:
				log.write_log("[CONSOLE] " + command)
				self.commands_function[solo_command](command)
			else:
				print(">> Error command \"" + command + "\"")
				log.write_log("[CONSOLE] ERROR " + command)

	def print_online(self, command):
		print(">> Online count = ", len(users.users))
		for user in users.users:
			print("   ", user.login)

	def cmd(self, command):
		cmd_command = str(input(">> ---CMD---\n"))
		log.write_log("[CONSOLE_CMD] " + cmd_command)
		os.system(cmd_command)

	def update_settings(self, command):
		print(">> Settings is updated")
		settings_file.update()

	def pause_server(self, command):
		if server.is_paused:
			print(">> The server is paused already")
		else: 
			print(">> The server is paused")
			server.pause(True)

	def unpause_server(self, command):
		if not server.is_paused:
			print(">> The server is paused already")
		else:	
			print(">> The server is unpaused")
			server.pause(False)

	def big_notify(self, command):
		text = command.split(" ")
		text.pop(0)
		server.send_big_notify_to_all(' '.join(text))

	def exit(self, command):
		print(">> Exit...")
		log.write_log("Server is stopped")
		os._exit(0)


	commands_function = { }
