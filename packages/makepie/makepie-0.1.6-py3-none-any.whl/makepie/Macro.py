import inspect
import logging

from .Caches import FileCache
from .Exceptions import MakepieException

log = logging.getLogger(__name__)

class Macro:
	def __init__(self, func):
		self.func = func
		self.argspec = inspect.getfullargspec(func)
		self.cache: FileCache = None

	def cached(self):
		if not self.cache:
			log.debug(f"No cache, not cached")
			return False
		
		return self.cache.cached()

	def parse_arg(self, arg, arg_name):
		type_class = self.argspec.annotations.get(arg_name, None)

		if not type_class:
			log.debug(f"No type for arg {arg_name}")
			return arg

		if not isinstance(type_class, type):
			log.debug(f"Type for arg {arg_name} is not a type ({type_class.__class__}), unsupported")
			return arg
		
		log.debug(f"Parsing {arg_name}:{arg} as '{type_class.__name__}'")

		try:
			return type_class(arg)
		except Exception as e:
			raise MakepieException(f"Failed to parse arg '{arg_name}' with value '{arg}' as {type_class}") from e
		
	def parse_args(self, *args, **kwargs):
		args = list(args)

		log.debug(f"Parsing args/kwargs")
		log.debug(f"Argspec: {self.argspec}")

		for i in range(len(args)):
			try:
				arg_name = self.argspec.args[i]
			except IndexError as e:
				raise MakepieException(f"Called macro '{self.func.__name__}' with too many arguments") from e

			args[i] = self.parse_arg(args[i], arg_name)

		for k, v in kwargs.items():
			kwargs[k] = self.parse_arg(v, k)

		return args, kwargs

	def __call__(self, *args, **kwargs):
		log.info(f"Macro '{self.func.__name__}' called with args: {args}, kwargs: {kwargs}")

		log.debug(f"Checking cache")
		if self.cached():
			log.info(f"Cached, returning on_cache result")
			return self.cache.get_cached_result(*args, **kwargs)

		# Parse args and kwargs
		args, kwargs = self.parse_args(*args, **kwargs)

		log.debug(f"Calling target function '{self.func.__name__}' with args: {args}, kwargs: {kwargs}")
		return self.func(*args, **kwargs)
