from database_handler import database


class Admin_Command:
	def __init__(self, request):
		if int(database.get_user_info(request["login"])): # if really is a admin
			command = request["command"].split(" ")
			#if command[0] == "/kick"