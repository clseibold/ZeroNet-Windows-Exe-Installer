import os, json

def recursiveDir(obj, prefix=""):
	result = []
	for name in obj:
		absolute = "%s.%s" % (prefix, name) if prefix != "" else name
		if isinstance(obj[name], dict):
			result += recursiveDir(obj[name], absolute)
		else:
			result.append(absolute)
	return result

class Config(object):
	class AttributeError(AttributeError):
		pass

	def __init__(self, path):
		self.__dict__["path"] = path

	# Read single value
	def __getattr__(self, name):
		try:
			with open(self.path, "r") as f:
				config = json.loads(f.read())
				return config[name]
		except (KeyError, AttributeError):
			raise Config.AttributeError("No '%s' config variable" % name)
		except IOError:
			raise Config.AttributeError("No config file and therefore no '%s' attribute" % name)
	def __getitem__(self, name):
		return self.__getattr__(name)

	# Read value recursively
	def get(self, name, default=None):
		name = name.split(".")

		try:
			val = self[name[0]]
			for part in name[1:]:
				val = val[part]

			return val
		except (KeyError, AttributeError, Config.AttributeError):
			return default

	# Write single value
	def __setattr__(self, name, value):
		try:
			with open(self.path, "r") as f:
				config = json.loads(f.read())
		except IOError:
			config = dict()

		config[name] = value

		with open(self.path, "w") as f:
			f.write(json.dumps(config))
	def __setitem__(self, name, value):
		self.__setattr__(name, value)

	# Write value recursively
	def set(self, name, value):
		try:
			with open(self.path, "r") as f:
				config = json.loads(f.read())
		except IOError:
			config = dict()

		current = config
		for part in name.split(".")[:-1]:
			try:
				current = current[part]
			except KeyError:
				current[part] = dict()
				current = current[part]

		current[name.split(".")[-1]] = value

		with open(self.path, "w") as f:
			f.write(json.dumps(config))

	# Delete variable
	def __delattr__(self, name):
		try:
			with open(self.path, "r") as f:
				config = json.loads(f.read())
		except IOError:
			config = dict()

		del config[name]

		with open(self.path, "w") as f:
			f.write(json.dumps(config))
	def __delitem__(self, name, value):
		self.__delattr__(name, value)

	# Delete variable recursively
	def remove(self, name):
		try:
			with open(self.path, "r") as f:
				config = json.loads(f.read())
		except IOError:
			config = dict()

		current = config
		for part in name.split(".")[:-1]:
			try:
				current = current[part]
			except KeyError:
				current[part] = dict()
				current = current[part]

		del current[name.split(".")[-1]]

		with open(self.path, "w") as f:
			f.write(json.dumps(config))

	# Get data list
	def __dir__(self):
		try:
			with open(self.path, "r") as f:
				config = json.loads(f.read())
			return dir(config)
		except IOError:
			return []

	# Get data list recursively
	def list(self):
		try:
			with open(self.path, "r") as f:
				config = json.loads(f.read())
		except IOError:
			return []

		return recursiveDir(config)

current_dir = os.path.dirname(os.path.abspath(__file__))
config_json = os.path.abspath(os.path.join(current_dir, "../config.json"))
config = Config(config_json)