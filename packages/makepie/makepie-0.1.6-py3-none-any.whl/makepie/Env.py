import logging, os, re
from .Exceptions import MakepieException

log = logging.getLogger(__name__)

def env(key=None, default=None, throws=False):
	if key is None:
		return os.environ

	try:
		return os.environ[key]
	except KeyError as e:
		if throws:
			raise MakepieException(f"Environment variable {key} not found") from e

		log.info(f"Environment variable '{key}' not found, using default '{default}'")
		return default

def _setenv(key, value):
	os.environ[key] = value

def setenv(**kwargs):
	for key, value in kwargs.items():
		_setenv(key, value)

def unsetenv(*args):
	for key in args:
		del os.environ[key]
	
key_val_reg = re.compile(r"^(?P<key>\w+)=(?P<value>.*)\b", re.M)
def env_file_parse(file:str):
	result = {}
	with open(file, 'r') as f:
		for match in key_val_reg.finditer(f.read()):
			result[match.group("key")] = match.group("value")
	return result

# Load env from file with key=value format
def env_load(file):
	dict = env_file_parse(file)
	setenv(**dict)
