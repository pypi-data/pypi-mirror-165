import logging
from .Config import config

class AppLog(logging.Logger):
	# Shortcut
	def __call__(self, *args, **kwds):
		return super().info(*args, **kwds)

applog = AppLog("app")

def logging_load():
	# Basic config
	fallback_level = logging.INFO if config("DEBUG", False) else logging.WARNING
	logging.basicConfig(
		level=config("MAKEPIELOG_LEVEL", fallback_level),
		format=config("MAKEPIELOG_FORMAT", "[%(levelname)s]-%(name)s: %(message)s"),
	)

	# App log
	applog.propagate = False # Prevent propagation to default handlers
	hdlr = logging.StreamHandler()
	hdlr.setFormatter(logging.Formatter(config("LOG_FORMAT", "{message}"), style="{"))
	applog.addHandler(hdlr)
	applog.setLevel(config("LOG_LEVEL", logging.DEBUG))

	logging.debug("Logging loaded")
