import logging
import traceback, sys
from .Config import config
from .MakepieLogging import applog
from .Exceptions import MakepieException

log = logging.getLogger(__name__)

def parse_argv(argv, macros, default_macro):
	# Ignoring first argument (script name)
	args = argv[1:]
	log.debug(f"Parsing args: {args}")

	# If default macro called
	if len(args) < 1:
		if default_macro is None:
			raise MakepieException("No macro called and no default macro set")
		
		log.debug(f"Calling default macro")
		return default_macro

	# Parsing args
	macro_name = args[0]
	macro_args = []
	macro_kwargs = {}
	for arg in args[1:]:
		if "=" in arg:
			key, value = arg.split("=", 1)
			macro_kwargs[key] = value
		else:
			macro_args.append(arg)

	# Macro existance postcondition
	if macro_name not in macros:
		raise MakepieException(f"Macro '{macro_name}' not found")

	return (macro_name, tuple(macro_args), macro_kwargs)

def main(macros, default_macro, argv=sys.argv):
	try:
		(macro_name, macro_args, macro_kwargs) = parse_argv(argv, macros, default_macro)

		log.debug(f"Executing macro: '{macro_name}' with args: {macro_args}, kwargs: {macro_kwargs}")
		result = macros[macro_name](*macro_args, **macro_kwargs)

		if result is not None:
			applog(f"Macro returned: {result}")

	except Exception as exc:
		if isinstance(exc, MakepieException) and not config("DEBUG", False):
			applog(f"Makepie error: {exc}")
		else:
			traceback.print_exception(exc)
		result = 1

	return result

log.debug("Loaded makepie, loading user config...")
