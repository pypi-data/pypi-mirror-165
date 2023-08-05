from .Exceptions import MakepieException

config_dict = {}

def config(key=None, default=None, throws=False):
	if key is None:
		return config_dict

	try:
		return config_dict[key]
	except KeyError as e:
		if throws:
			raise MakepieException(f"Config '{key}' not found") from e

		return default

# Should not be used by the user
def setconfig(key, value):
	config_dict[key] = value

def setconfigkw(**kwargs):
	for key, value in kwargs.items():
		setconfig(key, value)
