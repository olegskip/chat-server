import os
import json


def get_exe_path():
    return os.path.dirname(os.path.abspath(__file__))

class Settings_File:
	def __init__(self, path):
		self.path = path
		self.update()

	def update(self):
		self.params = json.loads(open(self.path, "r").read())

	params = { }
	path = ""

settings_file = Settings_File(get_exe_path() + '\\settings\\settings.json')