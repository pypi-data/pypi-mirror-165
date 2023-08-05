import functools, logging
from typing import Callable, List

from .Exceptions import MakepieException
from .Macro import Macro
from .Caches import FileCache

log = logging.getLogger(__name__)

# Main macro decorator
macros = {}
default_macro = None

def get_macros():
	return macros, default_macro

def _interpret_tag(tag: str, macro: Macro):
	global default_macro

	data = macro.func.makepie_tags.get(tag, None)

	if tag == "default":
		if default_macro is not None:
			raise MakepieException("Default macro already defined")
		
		default_macro = (macro.func.__name__, data["args"], data["kwargs"])
		return

	if tag == "cache":
		macro.cache = data
		return

def macro(func: Callable):
	global macros

	if func.__name__ in macros:
		raise MakepieException(f"Macro '{func.__name__}' already defined")

	# Make macro
	m = Macro(func)
	macros[func.__name__] = m

	# Interpret makepie tags
	if hasattr(func, "makepie_tags"):
		for tag in func.makepie_tags.keys():
			_interpret_tag(tag, m)

	# Decorate the function
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		return m(*args, **kwargs)

	return wrapper

# Decorators
def _setup_tags(func):
	if not hasattr(func, "makepie_tags"):
		func.makepie_tags = {}
	return func

def cache(cache_files: List[str], dependencies: List[str]=[], on_cache: Callable=None):
	def decorator(func):
		func = _setup_tags(func)
		func.makepie_tags["cache"] = FileCache(cache_files, dependencies, on_cache)
		return func
	return decorator

def default(*args, **kwargs):
	def decorator(func):
		func = _setup_tags(func)
		func.makepie_tags["default"] = {"args": args, "kwargs": kwargs}
		return func
	return decorator
