import os, json, logging, sys, shutil, yaml
from os.path import join, dirname, realpath, isfile, isdir, exists
# TODO use Pathlib instead of os.path
from pathlib import Path

from .Config import *
from .Env import *
from .MakepieLogging import applog, logging_load
from .Decorators import *
from .Version import *
from .Caches import *
from .Exceptions import *
from .Utils import *
from .ShellCmd import *
from .Environement import *

log = applog
init_log = logging.getLogger(__name__)

def makepie_load(**config_kw):
	# Load user config
	setconfigkw(**config_kw)

	logging_load()
	
	# Try loading optional config
	try:
		env_load(config("ENV_FILE", ".env"))
	except Exception as e:
		init_log.warning(f"Could not load optional config: {e}")

	init_log.debug(f"Loaded makepie")

# Makepie Facade
__all__ = [
	"makepie_load",
	"config",
	"log",
	"macro",
	"cache",
	"default",
	"Version",
	"MakepieException",
	"FileCache",
	"Environment",
	"DEV",
	"LOC",
	"STA",
	"TES",
	"PRE",
	"PRO",
	"env",
	"setenv",
	"unsetenv",
	"rm",
	"cp",
	"mv",
	"mkdir",
	"join",
	"dirname",
	"realpath",
	"isfile",
	"isdir",
	"exists",
	"rfile",
	"wfile",
	"replace",
	"tplsubst",
	"glob",
	"sh",
	"logging",
	"os",
	"shutil",
	"json",
	"sys",
]
