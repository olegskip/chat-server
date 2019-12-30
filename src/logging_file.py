from datetime import datetime
import os

class Logging:
	def __init__(self, path=""):
		if path:
			self.file = open(path, 'a', encoding="utf-8")

			self.file.write("\n\n\n")
			self.file.flush()


	def get_current_time(self):
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		return current_time

	def write_log(self, data):
		self.file.write(self.get_current_time() + "\t" + data + "\n")
		self.file.flush()

	def get_exe_path(self):
		return os.path.dirname(os.path.abspath(__file__)) + "\\"

	file = None

log = Logging(Logging().get_exe_path() + "logs\\connections" + ".txt")
log_chat = Logging(Logging().get_exe_path() + "logs\\chat" + ".txt")
